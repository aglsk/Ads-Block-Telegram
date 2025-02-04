# Bot Telegram de Moderação com Modo Treino e Filtro de Palavras Suspeitas

Este bot do Telegram monitora mensagens em grupos, detecta palavras suspeitas e oferece um modo treino para capturar novas palavras suspeitas antes de adicioná-las à lista definitiva. Ele também permite que administradores confirmem manualmente palavras suspeitas e as enviem para um Google Apps Script para armazenamento.

## Funcionalidades
- **Modo Treino**: Detecta palavras suspeitas e aguarda confirmação antes de adicioná-las ao filtro.
- **Remoção Automática**: Apaga mensagens com palavras já confirmadas como suspeitas.
- **Advertências**: Registra advertências para usuários reincidentes.
- **Banimento Automático**: Bane um usuário após 4 advertências.
- **Confirmação de Palavras**: Admins podem confirmar palavras manualmente ou em lote.
- **Integração com Google Sheets**: Envia palavras suspeitas para uma planilha no Google Sheets via Google Apps Script.

## Requisitos
- Python 3
- Bibliotecas necessárias:
  ```sh
  pip install pyTelegramBotAPI requests
  ```

## Instalação
1. Substitua `BOT_TOKEN` pelo token do seu bot do Telegram.
2. Substitua `URL_GOOGLE_APPS_SCRIPT` pela URL do seu Google Apps Script.
3. Execute o script:
   ```sh
   python bot.py
   ```

## Comandos Disponíveis
- `/treino` - Ativa ou desativa o modo treino (somente admins).
- `/confirmar_palavra <palavra>` - Confirma manualmente uma palavra suspeita.
- `/confirmar_todas` - Confirma todas as palavras suspeitas detectadas no modo treino.

## Como Funciona
1. **Modo Treino Ativado:** O bot identifica palavras repetidas e solicita confirmação manual.
2. **Modo Treino Desativado:** O bot bloqueia automaticamente mensagens com palavras suspeitas.
3. **Confirmação Manual:** Admins podem adicionar palavras suspeitas ao filtro via comandos.
4. **Banimento Automático:** Se um usuário reincidir 4 vezes, ele será removido do grupo.

## Personalização
Para modificar a lista de palavras suspeitas sem alterar o código, basta atualizar a planilha vinculada ao seu Google Apps Script.

## Autor
Desenvolvido para melhorar a segurança e a moderação em grupos do Telegram.

