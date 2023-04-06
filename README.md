# transfer-sheets-to-db

Проект для переноса заказов из гугл-таблицы в базу данных.

## ТЗ:

Разработать скрипт на языке Python 3, который будет выполнять следующие функции:

1. Получать данные с документа при помощи Google API, сделанного в [Google Sheets](https://docs.google.com/spreadsheets/d/1f-qZEX1k_3nj5cahOzntYAnvO4ignbyesVO7yuBdv_g/edit) (необходимо копировать в свой Google аккаунт и выдать самому себе права).
2. Данные должны добавляться в БД, в том же виде, что и в файле –источнике, с добавлением колонки «стоимость в руб.»
    
    a. Необходимо создать DB самостоятельно, СУБД на основе PostgreSQL.
    
    b. Данные для перевода $ в рубли необходимо получать по курсу [ЦБ РФ](https://www.cbr.ru/development/SXML/).
    
3. Скрипт работает постоянно для обеспечения обновления данных в онлайн режиме (необходимо учитывать, что строки в Google Sheets таблицу могут удаляться, добавляться и изменяться).

4. a. Упаковать решение в docker-контейнер.
    
    b. Разработать функционал проверки соблюдения «срока поставки» из таблицы. В случае, если срок прошел, скрипт отправляет уведомление в Telegram.

5. При проверке под правильностью работы понимается соответствие функционала программы поставленному ТЗ.
6. При оценке читаемости кода не требуется 100% соблюдения стандарта PEP8, но код должен быть логичен и не перегружен, необходимо соблюдение отступов и логики названия переменных и структур данных.
7. Оценка эффективности включает в правильность применение алгоритмов и структур данных. Например, стоит учитывать, что кортеж (tuple) работает быстрее, чем списки (list).
8. Комментированность кода – комментарии должны быть понятны и содержать достаточную информацию о функции, классе или методе.

## Инструкция

1. Перейти в терминал.
2. В терминале перейти в папку с проектом.
3. Для добавления переменных окружения выполнить:
   ```bash
   export LOGURU_FORMAT="..." WORKSHEET_KEY="..." ...
   ``` 
4. Для добавления необходимых библиотек выполнить:
   ```bash
   poetry install
   poetry shell
   ``` 
5. Для запуска выполнить:
   ```bash
   python main.py
   ``` 

## Логика работы

Проект запускается каждые 10 минут для обеспечения обновления данных в онлайн режиме. `(3)`

1. Получаем данные из нужного листа гугл-таблицы. `(1)`
2. Проверяем сроки поставки и рассылаем телеграм-уведомления по просроченным заказам. `(4b)`
3. Создаём базу данных и соединение с ней. `(2а)`
4. Создаём таблицу. `(2а)`
5. Очищаем таблицу.
6. Получаем курс доллара к рублю с сайта ЦБ РФ. `(2b)`
7. Заполняем таблицу, в цикле высчитывая "стоимость в руб.". `(2b)`
8. Закрываем соединение с базой данных.
