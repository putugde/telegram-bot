from dotenv import load_dotenv
import os
load_dotenv()

from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters

updater = Updater(token=os.getenv("TELEGRAM_BOT_TOKEN"), use_context=True)
dispatcher = updater.dispatcher

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Tes Teeeeess")

def echo(update, context):
    if context.args:
        text = context.args[0]
    else:
        text = 'Mau echo ape broo'
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

def main():
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    echo_handler = CommandHandler('echo', echo)
    dispatcher.add_handler(echo_handler)

    caps_handler = CommandHandler('caps', caps)
    dispatcher.add_handler(caps_handler)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()


