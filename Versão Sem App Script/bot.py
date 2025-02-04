import telebot

# Substitua pelo seu bot token
BOT_TOKEN = "BOT_TOKEN"

# Lista de palavras-chave suspeitas
PALAVRAS_SUSPEITAS = [
    "pagando Crypto", "convida 5 amigos", "Trust Wallet", "Metamask", "carteira",
    "Link https://t.me/", "ganhe dinheiro rápido", "lucro garantido", "invista agora",
    "dinheiro fácil", "sem risco", "multiplique seu dinheiro", "renda passiva",
    "criptomoeda grátis", "airdrop", "Binance Giveaway", "Crypto Airdrop", "USDT grátis",
    "nova plataforma de investimento", "bit.ly/", "getcrypto", "walletconnect", "freecrypto",
    "bitcoin grátis", "lucros instantâneos", "clique aqui para ganhar", "investimento garantido",
    "oferta limitada", "oferta imperdível", "invista em tokens", "ganhe em minutos", 
    "multiplicador de dinheiro", "tome o risco", "grátis para sempre", "depósito inicial baixo",
    "dinheiro sem sair de casa", "sem investimentos", "plano de riqueza", "saque rápido", 
    "programa de afiliados", "plano de afiliados", "bônus de cadastro", "plano de pirâmide", 
    "sem custo algum", "bônus de investimento", "plano de renda passiva", "negócio de sucesso rápido",
    "criar conta grátis", "link privado", "oferta exclusiva", "link de afiliado", "promessa de retorno rápido",
    "lucro sem risco", "sistema de pagamento rápido", "plano de enriquecimento rápido", "ganho de cripto",
    "compre criptomoeda", "sistema de criptomoeda", "dinheiro na hora", "recupere seu dinheiro",
    "compra segura", "invista seu dinheiro", "cartão pré-pago", "suporte 24h", "segurança garantida",
    "investimentos de baixo risco", "ganhe em dólares", "recupere seu investimento", "investimento alto retorno",
    "plano financeiro", "plano digital", "criar conta agora", "ganhe grátis", "dinheiro no ato", 
    "ganhe agora", "comprar com criptomoeda", "sem investimento inicial", "início imediato",
    "renda extra fácil", "receba em USDT", "agora ou nunca", "apenas hoje", "não perca essa oportunidade",
    "oferta especial", "garantia de retorno", "entrar em contato agora", "temos o que você precisa",
    "fique rico rápido", "plano de sucesso", "planos de crescimento", "futuro garantido", "invista em você",
    "dinheiro rápido sem risco", "ganhe com cripto", "investir e lucrar", "ganhe dinheiro fácil",
    "depósito rápido", "ganhe hoje", "plano de negócio digital", "renda passiva automática", "plano lucrativo",
    "enriquecer com pouco", "conta bancária grátis", "recebimento imediato", "suporte ao investidor",
    "venda de tokens", "faça seu dinheiro crescer", "invista sem medo", "comece hoje", "recompensa garantida",
    "plano de investimento de baixo custo", "crescimento rápido", "oferta relâmpago", "investimento digital",
    "site de investimento", "invista em cripto agora", "sistema de retorno financeiro", "renda de cripto",
    "plano de negócios cripto", "retorno financeiro imediato", "garantia de lucro", "mude sua vida financeira",
    "não perca a chance", "oferta de criptomoeda", "você pode ganhar", "conquiste sua liberdade financeira",
    "plano de oportunidade única", "ganhe com investimentos", "suporte 24/7", "invista com segurança",
    "plano de enriquecimento", "plano de sucesso imediato", "retorno rápido", "cripto garantido", "oferta exclusiva"
]

# Dicionário para armazenar o número de advertências por usuário (ID)
advertencias = {}

# Inicializa o bot com o token
bot = telebot.TeleBot(BOT_TOKEN)

# Função para verificar mensagens
@bot.message_handler(func=lambda message: True)
def verificar_mensagem(message):
    mensagem = message.text.lower()

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

# Inicia o bot
bot.polling(none_stop=True)
