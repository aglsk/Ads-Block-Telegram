import telebot
import requests
from collections import defaultdict

# Configuração do bot
BOT_TOKEN = "BOT_TOKEN"
URL_GOOGLE_APPS_SCRIPT = "https://script.google.com/macros/s/ID_SCRIPT_GOOGLE/exec"

# Inicializa o bot
bot = telebot.TeleBot(BOT_TOKEN)
modo_treino = False  # Variável global para ativar/desativar o modo treino
palavras_suspeitas_temp = defaultdict(int)  # Dicionário para contar palavras suspeitas temporárias

# Função para verificar se o usuário é administrador
def is_admin(chat_id, user_id):
    try:
        chat_admins = bot.get_chat_administrators(chat_id)
        return any(admin.user.id == user_id for admin in chat_admins)
    except Exception as e:
        print(f"Erro ao verificar admin: {e}")
        return False

# Comando para ativar/desativar o modo treino (apenas administradores)
@bot.message_handler(commands=['treino'])
def toggle_treino(message):
    global modo_treino
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    if is_admin(chat_id, user_id):
        modo_treino = not modo_treino
        status = "ativado" if modo_treino else "desativado"
        bot.send_message(chat_id, f"🔧 Modo treino {status} com sucesso!")
    else:
        bot.send_message(chat_id, "⚠️ Apenas administradores podem usar esse comando.")

# Função para registrar palavras suspeitas no Google Sheets
def salvar_palavra_suspeita(palavra):
    dados = {"palavras": [palavra]}
    try:
        requests.post(URL_GOOGLE_APPS_SCRIPT, json=dados)
    except Exception as e:
        print(f"Erro ao enviar dados para o Google Sheets: {e}")

# Comando para confirmar manualmente uma palavra suspeita
@bot.message_handler(commands=['confirmar_palavra'])
def confirmar_palavra(message):
    global palavras_suspeitas_temp
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    if not is_admin(chat_id, user_id):
        bot.send_message(chat_id, "⚠️ Apenas administradores podem confirmar palavras suspeitas.")
        return
    
    palavra = message.text.split(maxsplit=1)
    if len(palavra) < 2:
        bot.send_message(chat_id, "⚠️ Use: /confirmar_palavra <palavra>")
        return
    
    palavra = palavra[1].lower()
    if palavra in palavras_suspeitas_temp:
        salvar_palavra_suspeita(palavra)
        del palavras_suspeitas_temp[palavra]
        bot.send_message(chat_id, f"✅ Palavra '{palavra}' confirmada e enviada para a planilha.")
    else:
        bot.send_message(chat_id, "⚠️ Essa palavra não está na lista de suspeitas recentes.")

# Comando para confirmar todas as palavras suspeitas de uma vez
@bot.message_handler(commands=['confirmar_todas'])
def confirmar_todas(message):
    global palavras_suspeitas_temp
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    if not is_admin(chat_id, user_id):
        bot.send_message(chat_id, "⚠️ Apenas administradores podem confirmar palavras suspeitas.")
        return
    
    if not palavras_suspeitas_temp:
        bot.send_message(chat_id, "⚠️ Nenhuma palavra suspeita para confirmar.")
        return
    
    for palavra in list(palavras_suspeitas_temp.keys()):
        salvar_palavra_suspeita(palavra)
        del palavras_suspeitas_temp[palavra]
    
    bot.send_message(chat_id, "✅ Todas as palavras suspeitas foram confirmadas e enviadas para a planilha.")

# Captura todas as mensagens no modo treino e filtra palavras suspeitas
@bot.message_handler(func=lambda message: True)
def capturar_mensagem(message):
    global modo_treino
    if modo_treino:
        mensagem = message.text.lower() if message.text else ""
        palavras = mensagem.split()
        
        for palavra in palavras:
            palavras_suspeitas_temp[palavra] += 1
            
            if palavras_suspeitas_temp[palavra] >= 3:  # Palavra suspeita detectada 3 vezes
                salvar_palavra_suspeita(palavra)
                del palavras_suspeitas_temp[palavra]  # Remove da lista temporária
                bot.send_message(message.chat.id, f"🚨 Palavra '{palavra}' foi identificada como suspeita e enviada para a planilha!")
            else:
                bot.send_message(message.chat.id, f"🔍 Palavra '{palavra}' detectada, aguardando confirmação...")

# Inicia o bot
bot.polling(none_stop=True)
