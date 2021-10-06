import openai
from dotenv import load_dotenv
import os

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger('open-ai')

load_dotenv()

openai.api_key = os.getenv("OPEN_AI__BETA_TOKEN")

DEFAULT_PROMPT = 'The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, very smart, and very friendly.'

class OpenAIChatbot():
    def openChat(self, message, chatId):
        logging.info('Chat bot with message ' + message)
        prevMessage = ''

        try:
            with open(f'{chatId}.txt') as f:
                prevMessage = f.read()
        except:
            with open(f'{chatId}.txt', 'w+') as f:
                f.write(DEFAULT_PROMPT)

        messagePool = prevMessage + '\nHuman:' + message + '\nAI:'

        response = openai.Completion.create(
            engine="davinci",
            prompt=messagePool,
            temperature=0.7,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            stop=["\n", " Human:", " AI:"]
        )

        messageResponse = response.choices[0].text
        logging.info('Replied with ' + messageResponse)

        messagePool += messageResponse

        with open(f'{chatId}.txt', 'w+') as f:
            f.write(messagePool)
        
        return messageResponse
    
    def reset(self, chatId):
        with open(f'{chatId}.txt', 'w+') as f:
            f.write(DEFAULT_PROMPT)

