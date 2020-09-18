import requests
import time
import json
import os
import ystockquote

class Telegrambot:

    def __init__(self):
        #get the bot token and the api url
        token = '1395347480:AAFC16wv3tQ8Zbg4P0QJj8-7TEMpYM0Wj_0'
        self.url_base = f'https://api.telegram.org/bot{token}/'

    def start(self):
        #start the bot
        update_id = None
        while True:
            atualization = self.get_messages(update_id)
            messages = atualization['result']
            if messages:
                for message in messages:
                    update_id = message['update_id']
                    chat_id = message['message']['from']['id']
                    first_message = message['message']['message_id'] == 1
                    answer = self.create_answer(message, first_message)
                    self.answer(answer, chat_id)

    def get_messages(self, update_id):
        # get the messages from the chat
        link_requisition = f'{self.url_base}getUpdates?timeout=10'
        if update_id:
            link_requisition = f'{link_requisition}&offset={update_id + 1}'
        result = requests.get(link_requisition)
        return json.loads(result.content)

    def create_answer(self, message, first_message):
        # create the answer
        message = message['message']['text']
        if first_message or message.lower() == 'menu':
            return f'''Hi friend. What do you want to know?
{os.linesep}1 - Date and time{os.linesep}2 - Dolar quotation{os.linesep}3 - Euro quotation{os.linesep}4 - Pound quotation{os.linesep}5 - Yuan quotation'''
        if message == '1':
            return time.strftime("Date: %Y-%m-%d %H:%M", time.localtime())
        if message == '2':
            return self.dolar_quotation()
        if message == '3':
            return self.euro_quotation()
        if message == '4':
            return self.pound_quotation()
        if message == '5':
            return self.yuan_quotation()
        if message.lower() == 'thank you':
            return 'You are welcome'
        if message.lower() == 'hi':
            return f"""Hello!{os.linesep}Use 'Menu' to see my options"""
        else:
            return f"""Sorry, i couldn't understand{os.linesep}Type 'Menu' to see my options"""

    def answer(self,answer, chat_id):
        # send the answer to the chat
        send_link = f'{self.url_base}sendMessage?chat_id={chat_id}&text={answer}'
        requests.get(send_link)

    def dolar_quotation(self):
        #Inspired by https://medium.com/@douglasbragaw/construindo-uma-aplicação-em-python-que-mostra-cotação-de-moeda-consumindo-api-387376b25876
        #Returns dolar price in reais
        requesition = requests.get('https://economia.awesomeapi.com.br/all/USD-BRL')
        quotation = requesition.json()
        return 'R$: ' + quotation['USD']['bid']

    def euro_quotation(self):
        #Inspired by https://medium.com/@douglasbragaw/construindo-uma-aplicação-em-python-que-mostra-cotação-de-moeda-consumindo-api-387376b25876
        #Returns euro price in reais
        requesition = requests.get('https://economia.awesomeapi.com.br/all/EUR-BRL')
        quotation = requesition.json()
        return 'R$: ' + quotation['EUR']['bid']

    def pound_quotation(self):
        #Returns pound price in reais
        requesition = requests.get('https://economia.awesomeapi.com.br/all/GBP-BRL')
        quotation = requesition.json()
        return 'R$: ' + quotation['GBP']['bid']

    def yuan_quotation(self):
        #Returns yuan price in reais
        requesition = requests.get('https://economia.awesomeapi.com.br/all/CNY-BRL')
        quotation = requesition.json()
        return 'R$: ' + quotation['CNY']['bid']

bot = Telegrambot()
bot.start()