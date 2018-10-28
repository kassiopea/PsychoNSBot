from flask import Flask
from flask import request
from flask import jsonify
from flask_sslify import SSLify
import requests
import json
import re
import random
import constants
import variables

app = Flask(__name__)
sslify = SSLify(app)

URL = f"https://api.telegram.org/bot{constants.tokenTelBot}/"

urlYa = 'https://cloud-api.yandex.net/v1/disk/resources/public'

#временная функция для записи post запросов в файл json
def writeJson(data, filename='answer.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# функция распознования ключевой фразы про бота
def parsText(text):
    pattern = r"(?i)(\b)bot(\b)\s\w+[-]*[\d]*"

    try:
        resAnswer = re.search(pattern, text).group()
    except AttributeError:
        resAnswer = re.match(pattern, text)

    if resAnswer:
        val = resAnswer[4:].lower()

        for key, value in variables.patterKeywords.items():
            if val in value:
                return(key)

    return False

# функция по получению ссылки на видео
def getURLs(nameVideo):
    if nameVideo != False:
        result = requests.get(urlYa, params=constants.currentUpdateParams, headers=constants.headers)
        ans = result.json()
        allUrls = []

        if nameVideo == 'all':
            for i in ans['items']:
                allUrls.append(i['public_url'])
        else:
            for i in ans['items']:
                if nameVideo in i['name']:
                    allUrls.append(i['public_url'])

        randomURL = random.choice(allUrls)
        return f"Приятного просмотра!\n{randomURL}"

    else:
        return 'Извините, в нашей базе нет таких видео. Попробуйте снова.'


#функция отправки сообщений
def sendMessage(chatId, text, replyMessageId, replyMarkup = None):
    url = URL + 'sendMessage'

    if replyMarkup == None:
        answer = {'chat_id': chatId,
                  'text': text,
                  'reply_to_message_id': replyMessageId}

    elif replyMarkup == 'keyboardDel':
        keyboardDel = {'remove_keyboard': True}
        answer = {'chat_id': chatId,
                  'text': text,
                  'reply_to_message_id': replyMessageId,
                  'reply_markup': keyboardDel}

    elif replyMessageId == None:
        answer = {'chat_id': chatId,
                  'text': text}

    r = requests.post(url, json = answer)
    return r.json()

#функция для пересылки кастомной клавиатуры
def sendKeyboard(chatId, text, userName, replyMessageId):
    url = URL + 'sendMessage'

    ReplyKeyboardMarkup = {
        'keyboard': variables.keyboardButton,
        'resize_keyboard': True,
        'one_time_keyboard': True
    }

    answer = {'chat_id': chatId,
              'text': f"Приветствую тебя, мой повелитель, {userName}!\n{variables.commandStart}",
              'reply_to_message_id': replyMessageId,
              'reply_markup': ReplyKeyboardMarkup
              }

    r = requests.post(url, json = answer)
    return r.json()

# функция инлайн клавиатуры
def sendInlineKeyboard(chatId, text):
    url = URL + 'sendMessage'

    reply_markup = {'inline_keyboard': variables.keyboardInline}
    answer = {'chat_id': chatId,
              'text': text,
              'reply_markup': reply_markup
              }

    r = requests.post(url, json = answer)
    return r.json()

# функция определения, есть ли в ответе отредактированные сообщения
def varMess(r):
    vars = "message"
    if "edited_message" in r:
        vars = "edited_message"

    return vars

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        #действия при наличии collback по нажатию на инлайн клавиатуру
        if 'callback_query' in r:
            chatId = r['callback_query']['message']['chat']['id']
            message = r['callback_query']['data']
            replyMessageId = r['callback_query']['message']['message_id']
            mes = getURLs(message)
            category = variables.videoCategory[message]

            sendMessage(chatId, f'Из категории {category}. {mes}', replyMessageId=None)

        # действия при наличии сообщения от пользователя
        elif "message" in r or "edited_message" in r:
            vars = varMess(r)
            if "text" in r[vars]:
                chatId = r[vars]['chat']['id']
                message = r[vars]['text']
                userName = r[vars]['from']['first_name']
                replyMessageId = r[vars]['message_id']

                pattern = r"(?i)(\b)bot(\b)\s"

                # отлов сообщений с текстом бот и дальнейшая обработка с api запросом к яндексу
                if re.search(pattern, message):
                    mes = getURLs(parsText(message))
                    sendMessage(chatId, mes, replyMessageId)

                # действия на команду старт
                elif "/start" in message:
                    sendKeyboard(chatId, variables.commandStart, userName, replyMessageId)

                # действия на команду помощь
                elif '/help' in message or message == 'как тобой управлять?':
                    sendMessage(chatId, variables.commandHelp, replyMessageId, replyMarkup = 'keyboardDel')

                # действия на команду выбора
                elif '/choice' in message or message == 'выбрать категорию видео':
                    sendInlineKeyboard(chatId, 'Каравай, каравай, кого хочешь - выбирай')

                # действия на команду отмены
                elif message == 'ничего не хочу':
                    sendMessage(chatId, f"{userName}, буду нужен - вызывай!", replyMessageId, replyMarkup = 'keyboardDel')

                # инструкции для команды по отлавливанию ключевых слов
                elif message == 'хочу видео без категорий':
                    sendMessage(chatId, variables.sendVideoRules, replyMessageId,replyMarkup = 'keyboardDel')


            # действия при наличии вновь прибывшего в чате
            elif 'new_chat_member' in r['message']:
                chatId = r['message']['chat']['id']
                userName = r['message']['new_chat_member']['first_name']

                sendMessage(chatId, f'{userName}, {variables.welcomeMessage}', replyMessageId=None)

        return jsonify(r)

    return '<h1>Welcome! I`m bot PsychoNS!</h1>'

if __name__ == '__main__':
    app.run()
