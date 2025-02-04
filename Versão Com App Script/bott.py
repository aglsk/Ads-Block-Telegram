import telebot
import requests

# Substitua pelo seu bot token
BOT_TOKEN = "BOT_TOKEN"

# URL do seu Google Apps Script (substitua com o URL gerado)
URL_GOOGLE_APPS_SCRIPT = "https://script.google.com/macros/s/ID_APP_SCRIPT_GOOGLE/exec"

# Função para pegar palavras suspeitas do Google Apps Script
def obter_palavras_suspeitas():
    resposta = requests.get(URL_GOOGLE_APPS_SCRIPT)
    if resposta.status_code == 200:
        dados_json = resposta.json()
        return dados_json.get("PALAVRAS_SUSPEITAS", [])  # Alterado para corresponder à chave correta no JSON
    else:
        print("Erro ao obter dados")
        return []

# Lista de palavras suspeitas
PALAVRAS_SUSPEITAS = obter_palavras_suspeitas()

# Inicializa o bot com o token
bot = telebot.TeleBot(BOT_TOKEN)

# Dicionário para armazenar as advertências dos usuários (em memória)
advertencias = {}

# Função para verificar mensagens
@bot.message_handler(func=lambda message: True)
def verificar_mensagem(message):
    # Verifica se a mensagem é encaminhada
    mensagem = message.text.lower() if message.text else ""
    if message.forward_from:  # Se a mensagem for encaminhada, usa o texto da mensagem original
        mensagem = message.forward_from.text.lower() if message.forward_from.text else ""

    # Verifica se a mensagem contém alguma palavra suspeita
    if any(palavra.lower() in mensagem for palavra in PALAVRAS_SUSPEITAS):
        # Dados do usuário
        nome_usuario = message.from_user.first_name
        username_usuario = message.from_user.username if message.from_user.username else "Não possui username"
        user_id = message.from_user.id
        chat_id = message.chat.id

        # Atualiza a contagem de advertências
        if user_id not in advertencias:
            advertencias[user_id] = 0
        advertencias[user_id] += 1

        # Apagar a mensagem
        bot.delete_message(message.chat.id, message.message_id)

        # Opcional: Avisar o usuário
        try:
            bot.send_message(message.chat.id, "Essa mensagem foi removida porque pode ser um anúncio suspeito.")
        except Exception as e:
            print(f"Erro ao enviar mensagem de aviso: {e}")

        # Verifica se o usuário atingiu 4 advertências
        if advertencias[user_id] >= 4:
            # Bane o usuário
            bot.kick_chat_member(chat_id, user_id)

            # Envia mensagem informando que o usuário foi banido
            bot.send_message(chat_id, f"⚠️ <b>{nome_usuario}</b> (@{username_usuario}) - ID: {user_id} foi banido do grupo "
                                     "por violar as regras repetidamente. Ele tentou postar anúncios 4 vezes.", parse_mode="HTML")

            # Reseta o contador de advertências para o usuário
            advertencias[user_id] = 0
        else:
            # Envia mensagem de advertência
            aviso = (f"⚠️ <b>{nome_usuario}</b> (@{username_usuario}) - ID: {user_id} foi advertido. "
                     f"Você tem {4 - advertencias[user_id]} advertências restantes antes de ser banido.\n\n"
                     "Motivo: A mensagem foi identificada como um possível anúncio ou spam.")
            bot.send_message(chat_id, aviso, parse_mode="HTML")

        # Enviar aviso no grupo sobre o usuário
        try:
            bot.send_message(chat_id, f"Atenção: o usuário {message.from_user.username} ({message.from_user.id}) tentou enviar um anúncio suspeito!")
        except Exception as e:
            print(f"Erro ao enviar mensagem de alerta: {e}")

# Inicia o bot
bot.polling(none_stop=True)
