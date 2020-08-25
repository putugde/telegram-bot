from dotenv import load_dotenv
import os
load_dotenv()

from sln import Selenium

from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters

updater = Updater(token=os.getenv("TELEGRAM_BOT_TOKEN"), use_context=True)
dispatcher = updater.dispatcher

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger('vito-bot')

browser = Selenium()
browser.start()

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

def get_google_pic(update, context):
    try:
        if len(context.args) > 1:
            index = context.args[1]
            int(index)
        else:
            index = 1
        keyword = context.args[0]
        keyword = keyword.replace("-"," ")
        imgurl = browser.search_gimg(keyword, index)
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=imgurl)
    except IndexError:
        error_text = 'wrong arguments, try /gimg <keyword> <index>'
        context.bot.send_message(chat_id=update.effective_chat.id, text=error_text)
    except ValueError:
        error_text = 'index must be a number'
        context.bot.send_message(chat_id=update.effective_chat.id, text=error_text)

def main():
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    echo_handler = CommandHandler('echo', echo)
    dispatcher.add_handler(echo_handler)

    caps_handler = CommandHandler('caps', caps)
    dispatcher.add_handler(caps_handler)

    gimg_handler = CommandHandler('gimg', get_google_pic)
    dispatcher.add_handler(gimg_handler)

    logger.info('Start Pooling..')
    updater.start_polling()
    logger.info('Pool Started..!')
    updater.idle()
    browser.close()
    logger.info('Closed!')

if __name__ == "__main__":
    main()


