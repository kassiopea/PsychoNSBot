import requests
import json
import random
import re
import constants
import variables

# все для запроса к яндекс диску
urlYa = 'https://cloud-api.yandex.net/v1/disk/resources/public'
tokenYaD = constants.tokenYaD

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'OAuth ' + tokenYaD
}

currentUpdateParams = {
    'limit': '250',
    'type': 'file',
    'fields': 'items.name, items.public_url'
}

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
        result = requests.get(urlYa, params=currentUpdateParams, headers=headers)
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

def main():
    getURLs(parsText(message))

if __name__ == '__main__':
    main()
