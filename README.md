# Bot Telegram de Moderação com Filtro de Palavras Suspeitas

Este bot do Telegram monitora mensagens em grupos e remove automaticamente aquelas que contêm palavras suspeitas, além de emitir advertências e banir usuários reincidentes. O bot utiliza um Google Apps Script para armazenar e atualizar dinamicamente a lista de palavras suspeitas.

## Funcionalidades
- Monitoramento de mensagens em grupos do Telegram.
- Remoção automática de mensagens que contêm palavras suspeitas.
- Emissão de advertências para usuários que tentam enviar mensagens com conteúdo suspeito.
- Banimento automático de usuários após 4 advertências.
- Integração com um Google Apps Script para obter dinamicamente palavras suspeitas.

## Requisitos
- Python 3
- Biblioteca `telebot` para interagir com a API do Telegram.
- Biblioteca `requests` para se comunicar com o Google Apps Script.

## Instalação
1. Instale as dependências necessárias:
   ```sh
   pip install pyTelegramBotAPI requests
   ```
2. Substitua `BOT_TOKEN` pelo token do seu bot do Telegram.
3. Substitua `URL_GOOGLE_APPS_SCRIPT` pela URL do seu Google Apps Script.
4. Execute o script:
   ```sh
   python bot.py
   ```

## Configuração do Google Apps Script
O bot utiliza um Google Apps Script para armazenar e recuperar palavras suspeitas. Certifique-se de configurar um script no Google Apps Script que retorne um JSON com a chave `PALAVRAS_SUSPEITAS` contendo a lista de palavras a serem filtradas.

## Funcionamento
- O bot verifica todas as mensagens enviadas no grupo.
- Se uma mensagem contiver uma palavra da lista de palavras suspeitas, ela é apagada automaticamente.
- O usuário recebe uma advertência.
- Após 4 advertências, o usuário é banido do grupo.

## Exemplo de Uso
1. Um membro do grupo envia uma mensagem com uma palavra suspeita.
2. O bot apaga a mensagem e emite uma advertência.
3. Se o usuário continuar enviando mensagens suspeitas, ele receberá advertências adicionais.
4. Na quarta ocorrência, o usuário é banido automaticamente.

## Personalização
Se desejar modificar a lista de palavras suspeitas sem precisar alterar o código, basta atualizar a planilha vinculada ao seu Google Apps Script.

## Autor
Desenvolvido para moderação de grupos no Telegram, garantindo segurança contra mensagens de spam e conteúdo suspeito.

