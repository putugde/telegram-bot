from dotenv import load_dotenv
import os
load_dotenv()

# from sln import Selenium

from open_ai import OpenAIChatbot

from numpy import random

import requests

from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters

updater = Updater(token=os.getenv("TELEGRAM_BOT_TOKEN"), use_context=True)
dispatcher = updater.dispatcher

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger('vito-bot')

# browser = Selenium()
# browser.start()

chatbot = OpenAIChatbot()

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Tes Teeeeess")

def echo(update, context):
    if context.args:
        text = ' '.join(context.args)
    else:
        text = 'Mau echo ape broo'
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

# def get_google_pic(update, context):
#     # Argument Validation
#     if len(context.args) == 0:
#         error_text = 'wrong arguments, try /gimg <keyword> <index>'
#         context.bot.send_message(chat_id=update.effective_chat.id, text=error_text)
#     else:
#         args = context.args

#         if len(args) >1:
#             try:
#                 int(args[-1])
#                 index = int(args.pop())
#             except ValueError:
#                 index = random.randint(10)
#                 index += 1
#         else:
#             index = random.randint(10)
#             index += 1
            
#         keyword = ' '.join(args)

#         if int(index) > 400:
#             error_text = 'maximum index is 400'
#             context.bot.send_message(chat_id=update.effective_chat.id, text=error_text)
#         else:
#             # Handle google image related search, every 25 div
#             index_int = int(index)
#             if index_int % 25 == 0:
#                 index_int += 1
#                 index = str(index_int)

#             imgurl = browser.search_gimg(keyword, index)
#             if imgurl:
#                 context.bot.send_photo(chat_id=update.effective_chat.id, photo=imgurl)
#             else:
#                 error_text = 'image not found'
#                 context.bot.send_message(chat_id=update.effective_chat.id, text=error_text)

def get_bing_pic(update, context):
    if len(context.args) == 0:
        error_text = 'wrong arguments, try /bimg <keyword> <index>'
        context.bot.send_message(chat_id=update.effective_chat.id, text=error_text)
    else:    
        url = "https://bing-image-search1.p.rapidapi.com/images/search"

        # Getting keyword and index
        args = context.args

        if len(args) >1:
            try:
                int(args[-1])
                index = int(args.pop())
            except ValueError:
                index = random.randint(10)
                index += 1
        else:
            index = random.randint(10)
            index += 1
            
        keyword = ' '.join(args)

        querystring = {"safeSearch":"Off","q":keyword}

        headers = {
            'x-rapidapi-host': "bing-image-search1.p.rapidapi.com",
            'x-rapidapi-key': os.getenv("RAPID_API_TOKEN")
            }

        logger.info(f"BingImage : {keyword} -- {index}")
        response = requests.request("GET", url, headers=headers, params=querystring)
        
        res = response.json()

        try:
            img = res["value"][index]

            img_caption = img["name"]
            imgurl = img["contentUrl"]
            text = img_caption
            context.bot.send_message(chat_id=update.effective_chat.id, text=text)
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=imgurl)
        except IndexError:
            error_text = 'image not found'
            context.bot.send_message(chat_id=update.effective_chat.id, text=error_text)
        except KeyError:
            error_text = 'api error'
            context.bot.send_message(chat_id=update.effective_chat.id, text=error_text)

def chat(update, context):
    if context.args:
        text = ' '.join(context.args)
    else:
        text = 'Mau echo ape broo'
    text = update.message.text
    userChatId = str(update.message.chat.id)
    response = chatbot.openChat(text, userChatId)
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)

def chatWithCommand(update, context):
    if context.args:
        text = ' '.join(context.args)
        userChatId = str(update.message.chat.id)
        response = chatbot.openChat(text, userChatId)
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)
    else:
        text = 'Please provide a message'
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    

def reset_context(update, context):
    text = 'Reset Context!'
    logger.info(text)
    userChatId = str(update.message.chat.id)
    chatbot.reset(userChatId)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

def main():
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    echo_handler = CommandHandler('echo', echo)
    dispatcher.add_handler(echo_handler)

    caps_handler = CommandHandler('caps', caps)
    dispatcher.add_handler(caps_handler)

    # gimg_handler = CommandHandler('gimg', get_google_pic)
    # dispatcher.add_handler(gimg_handler)

    bimg_handler = CommandHandler('bimg', get_bing_pic)
    dispatcher.add_handler(bimg_handler)

    # Handler for Open AI GPT3 Chatbot
    chat_handler = MessageHandler(Filters.text & (~Filters.command), chat)
    dispatcher.add_handler(chat_handler)

    # Handle Chat via Command
    chat_reset_handler = CommandHandler('chat', chatWithCommand)
    dispatcher.add_handler(chat_reset_handler)

    # Handle Reset Text File
    chat_reset_handler = CommandHandler('reset', reset_context)
    dispatcher.add_handler(chat_reset_handler)

    logger.info('Start Pooling..')
    updater.start_polling()
    logger.info('Pool Started..!')
    updater.idle()
    # browser.close()
    logger.info('Closed!')

if __name__ == "__main__":
    main()


