import json
import os
import requests
from typing import Final
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
# from config import TELEGRAM_TOKEN

print('main.py is running')
app = Flask(__name__)
TELEGRAM_TOKEN: Final = '6721148638:AAHwpUUxRot21GEx35UweWFhwKD8kfvmYLo'
BOT_USERNAME = '@JessBetBot' 

# Lambda Caller
def lambda_handler(event, context):
    print("event", event)
    print("event's body", event['body'])
    
    # Extract the JSON-formatted string from the 'body' field
    body_str = event['body']

    # json module test
    json_str = '{"key": "value"}'
    data = json.loads(json_str)
    print('json_str test =', data)

    # Check if the body is empty
    if not body_str:
        print("Empty body received.")
        # Handle empty body as needed
        response = {
            "statusCode": 404,
            "body": "Empty Body"
        }
    else:
        try:
            body_dict = json.loads(body_str)
            # Continue with processing the JSON data
            print("body_dict =", body_dict)
            response = {
                "statusCode": 200,
                "body": "success in body_dict"
            }
            if 'message' in body_dict and 'text' in body_dict['message']:
                text = body_dict['message']['text'].lower()
                if text.startswith('/start'):
                    # Handle /start command
                    response_text = 'Psst! Act normal! We must not let her know... What do you want?'
                elif text.startswith('/help'):
                    # Handle /help command
                    response_text = 'Okay, so you need help.. or is she the one?... Here we go'
                elif text.startswith('/custom'):
                    response_text = 'In progress...'
                elif text == 'hello':
                    response_text = 'Hey there!'
                else:
                    # Handle other commands
                    response_text = 'Unknown command'            
            chat_id = body_dict.get('message', {}).get('chat', {}).get('id')
            print("Chat ID:", chat_id)
            print("Chat ID type:", type(chat_id))
            bot_message = "Hello, this is a bot message."
            url = 'https://api.telegram.org/bot' + TELEGRAM_TOKEN + '/sendMessage'
            params = {
                'chat_id': chat_id,
                'text': response_text
            }
            
            requests.post(url, params=params)
            print("url", url)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            # Handle JSON decoding error as needed
            response = {
                "statusCode": 400,
                "body": f"JSON Decode Error: {str(e)}"
            }

    # Parse the JSON string into a Python dictionary
    # body_dict = json.loads(body_str)

    # Extract the 'chat' object and get the 'id' field
    # chat_id = body_dict.get('message', {}).get('chat', {}).get('id')

    # Print or use the chat_id as needed
    # print("Chat ID:", chat_id)

    bot_message = "Hello, this is a bot message."   
    # send_text = 'https://api.telegram.org/bot' + TELEGRAM_TOKEN + 'sendMessage?chat_id=' + chat_id + '&text=' + bot_message
    # requests.post(send_text)

    return response


        # else:
            #  return {"statusCode": 400, "body": "Unsupported method"}

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
    message_type: str = update.message.chat.type  # inform us whether group OR private chat
    text: str = update.message.text  # Incoming, the one that we can process

    

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
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Commands (add handlers)
    app.add_handler
