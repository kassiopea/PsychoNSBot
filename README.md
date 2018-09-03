# PsychoNSBot
## telegram bot
---
## Технические данные

### Язык программирования и фреймворк
* Python 3.6
* Flask

### API
[API Яндек Диск](https://tech.yandex.ru/disk/api/concepts/about-docpage/ "документация по API Яндекс Диск")

[telegram bot API](https://core.telegram.org/bots/api "документация по API telegram bot")

### Библиотеки
* Flask request
* Flask jsonify
* requests
* json
* re
* random

### Модуль
main.py

### Подмодули
* parser.py
* variables.py
* constants.py
* answer.json

main.py - основной код для реализации бота  
parser.py - содержит функции парсинга ключевой фразы и запросы к Яндекс Диску
variables.py - набор переменных
* кастомные кнопки
* инлайн кнопки
* словарь со списками для поиска соответствий
* ответы бота
constants.py - токены к API и ссылки на прокси. В репозитории отсутствуют в связи с конфиденциальностью данных.
answer.json - отладочный файл для чтения запросов и ответов в удобном виде. В репозитории отсутствует. Создается с помощью вызова функции в модуле main.py

Сторонние библиотеки для ботов telegram api не использовались

---

Краткую инструкцию пользователя можно посмотреть в wiki
