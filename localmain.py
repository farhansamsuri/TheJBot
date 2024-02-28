import os
import json
import requests
# from config import types
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN: Final = os.environ.get('TOKEN')
BOT_USERNAME = os.environ.get('BOT_USERNAME') 

    # Lambda Caller
def lambda_handler(event, context):
    #TODO implement
    
    #update = types.Update.de_json(json.loads(event['body']))
    #bot.process_new_updates([update])
    
    #send_text = 'https://api.telegram.org/bot' + TOKEN + '/sendMes\'&parse_mode=HTML&text=' + bot_message
    #response = requests.get(send_text)
    #print(response)
    #test workflow with a simple change here
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

# Commands

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Psst! Act normal! We must not let her know... What do you want?')
    
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Okay, so you need help.. here we go')
    
async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('custom command - multiple available.')
  
  # Responses
    
def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'hello' in processed:
        return 'Hey there!'
    
    if 'how are you' in processed:
        return 'I am good!'
    
    return 'I do not understand you buddy'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type #inform us whether group OR private chat
    text: str = update.message.text #Incoming, the one that we can process

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    # Check if the message is in a group chat and if it mentions the bot then bot will respond
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text) 

    print('Bot:', response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Commands (add handlers)
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))   
    
    # Error
    app.add_error_handler(error)

    # Checking for updates/messages every 3 seconds
    print('Polling...')
    app.run_polling(poll_interval=3)
