## **vk-slaves-bot - многофункциональный бот для игры ["Рабы"](https://vk.com/app7794757) (игра закрыта с 31.03.2021) ВКонтакте.**

[Группа ВКонтакте](https://vk.com/club203543653), в ней публикуются новости и другая полезная информация. У группы есть беседа, в которой можно задавать вопросы.

**Лучшая благодарность - звёздочка на GitHub и "спасибо" в [ЛС в ВК](https://vk.com/id607137534).**

**Если хотите отблагодарить материально, пишите в [ЛС](https://vk.com/id607137534).**

## В консоль спамит **'balance'**, **'slaves'**, **'id'** или **'price'**. Что делать?

Возможные причины такого поведения:

- Некорректное значение `authorization` в `config.py`, попробуйте заново получить его.
- Не хватает баланса на покупку раба.
- Блокировка на несколько часов. Для проверки - попробуйте купить раба вручную, если выходит ошибка `ErrFloodBuy`, значит у Вас блокировка на несколько часов. Для предотвращения подобных ситуаций, советуем повысить значения `min_delay` и `max_delay` в `config.py`.

## В консоль спамит **'Expecting value'**.

Вероятнее всего у вас стоит слишком высокое значение `min_price`, из-за чего бот долго ищет подходящих рабов и выдаёт эти сообщения. Эту ошибку можно просто игнорировать.

## Установка на Windows

- Устанавливаем [Python](https://www.python.org/downloads/windows) (Для Windows 7 нужен [Python 3.8](https://python.org/ftp/python/3.8.8/python-3.8.8.exe)). Во время установки обязательно ставим галочку `Add Python to PATH (Добавить Python в PATH)`
- [Скачиваем архив с ботом](https://github.com/monosans/vk-slaves-bot/archive/refs/heads/main.zip).
- Распаковываем архив.
- Редактируем файл `config.py` через любой текстовый редактор:
  - authorization:
    - Открываем [игру](https://vk.com/app7794757)
    - Нажимаем `F12` (Для Chromium браузеров)
    - Перезагружаем страницу горячей клавишей `F5`
    - В появившейся панели выбираем вкладку `Network`
    - Находим кнопку `Filter` (в виде воронки)
    - В появившемся поле пишем `start`
    - В панели появится поле `start`, нажимаем по нему
    - Появится еще одна панель, выбираем в ней вкладку `Headers`
    - Ищем поле `authorization`
    - Копируем его значение (начинается c **vk_access_token_settings**, **Bearer** копировать не нужно)
    - Вставляем скопированный текст в значение `authorization` в `config.py` между кавычками
  - my_id - **числовой** id вашей страницы ВКонтакте. Узнать можно через [сайт](https://regvk.com/id).
  - buy_slaves_mode - режим покупки рабов (0 - выкл, 1 - покупать случайных рабов, 2 - покупать рабов у игроков из топа, 3 - покупать рабов у людей из списка `buy_from_ids`)
  - buy_from_ids - ID людей, у которых вы хотите перекупать рабов при `buy_slaves_mode = 3`, через запятую. ID можно получить через [сайт](https://regvk.com/id).
  - buy_fetters - покупать ли оковы (0 - выкл, 1 - вкл)
  - upgrade_slaves - улучшать ли рабов для повышения дохода (0 - выкл, 1 - вкл)
  - min_price - минимальная цена для покупки раба. Значения выше 40 приведут к более долгому поиску рабов.
  - max_price - максимальная цена для покупки раба. Не советуем ставить выше 26151, потому что это будет невыгодно.
  - max_fetter_price - максимальная цена для покупки оков. Значение 35303 установлено для рабов с ценой 26151 (это выгодно).
  - jobs - названия устанавливаемых работ. Если хотите, чтобы была только одна работа, пишите так: `jobs = ["ИмяРаботы"]`. Если хотите несколько, пишите их через запятую, при этом берите каждое значение в кавычки, например: `jobs = ["Повар", "Строитель", "Учитель", "Кассир"]`
  - min_delay - минимальная задержка между одинаковыми операциями в секундах. Чем ниже, тем выше вероятность получения блокировки на несколько часов.
  - max_delay - максимальная задержка между одинаковыми операциями в секундах. Чем ниже, тем выше вероятность получения блокировки на несколько часов.

Запуск: `start.bat`. Если после запуска ничего не происходит или выходит ошибка, связанная с Python или pip:

- Откройте `cmd`
- Напишите `python -V`
- Вывод должен соответстовать виду: `Python версия`. При этом версия должна быть выше **3.7.X**.
- Если вывод не соотвествует виду, нужно переустановить [Python](https://www.python.org/downloads/windows). Во время установки нужно обязательно поставить галочку `Add Python to Path (Добавить Python в PATH)`

## Установка на Termux (Android)

- Устанавливаем [Termux с F-Droid](https://f-droid.org/repo/com.termux_108.apk), т.к. в Google Play разработчик его больше не обновляет.
- Запускаем Termux.
- Пишем по порядку:
  - cd
  - pkg install -y git python
  - git clone https://github.com/monosans/vk-slaves-bot
- Редактируем файл `config.py` командой `nano vk-slaves-bot/config.py`. Для удобного редактирования можно скачать [приложение Hacker's Keyboard](https://play.google.com/store/apps/details?id=org.pocketworkstation.pckeyboard), в нём в горизонтальном положении есть стрелочки для управления курсором.
- Чтобы получить `authorization` с телефона, используем [приложение F12](https://play.google.com/store/apps/details?id=com.asfmapps.f12):
  - authorization:
    - Открываем приложение F12, заходим на [сайт мобильного ВКонтакте](https://m.vk.com) и авторизуемся.
    - Открываем [игру](https://m.vk.com/app7794757) через тот же F12.
    - Нажимаем кнопку F12, переходим на вкладку `Network` (3-я по счёту).
    - Ставим галочку около `Advance`.
    - Сворачиваем панель и нажимаем на стрелочку для перезагрузки страницы.
    - Вновь нажимаем кнопку F12, переходим на вкладку `Network`.
    - Немного листаем вверх и находим запись `https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/start`, нажимаем по ней.
    - Появится ещё одна панель. Под записью Request Headers находим поле `authorization`.
    - Копируем его значение (начинается c **vk_access_token_settings**, **Bearer** копировать не нужно)
    - Вставляем скопированный текст в значение `authorization` в `config.py` между кавычками.
- После редактирования файла, для сохранения нажмите Ctrl-O, Enter, Ctrl-X.

Запуск: `sh vk-slaves-bot/launch.sh`

## Переустановка в Termux

Ввести команды по порядку:

```
cd
rm -rf vk-slaves-bot
```

После этого заново установить по инструкции.
