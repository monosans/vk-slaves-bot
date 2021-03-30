# vk-slaves-bot

Бот для мини-игры ["Рабы" ("Рабство")](https://vk.com/app7794757) ВК

[Группа в ВК](https://vk.com/club203543653), в ней публикуются новости и другая полезная информация. У группы есть [беседа](https://vk.me/join/d4lmYy0XQdusTdgdW3acrqXcaH_plolkc7o=), в которой можете задавать вопросы.

**Лучшая благодарность - звёздочка на GitHub и "спасибо" в [ЛС в ВК](https://vk.com/id607137534).**

**Если хотите отблагодарить материально, пишите в [ЛС](https://vk.com/id607137534).**

## В консоль спамит **'balance'**, **'slaves'** или **'id'**. Что делать?

Возможные причины такого поведения:

- Неправильный `authorization` в `config.json`. Зайдите в игру, проверьте, прибавляется ли количество рабов. Попробуйте заново получить `authorization`.
- Не хватает баланса на покупку раба.
- Бан на несколько часов. Попробуйте купить раба вручную. Если выходит ошибка `ErrFloodBuy`, значит у Вас бан на несколько часов. Если бан был получен при использовании этого бота, попробуйте повысить `delay` в `config.json`.

## Установка на Windows

- Устанавливаем [Python](https://www.python.org/downloads/windows) (Для Windows 7 нужен [Python 3.8](https://python.org/ftp/python/3.8.8/python-3.8.8.exe)). Во время установки ставим галочку `Add Python to PATH (Добавить Python в PATH)`
- [Скачиваем архив с ботом](https://github.com/monosans/vk-slaves-bot/archive/refs/heads/main.zip).
- Распаковываем архив.
- Редактируем файл `config.json` через любой текстовый редактор:

  - authorization:
    - Открываем [игру](https://vk.com/app7794757)
    - Нажимаем `F12` (Для Chromium браузеров)
    - Перезагружаем страницу горячей клавишей `F5`
    - В появившейся панели выбираем вкладку `Network`
    - Находим кнопку `Filter` (воронка)
    - В появившемся поле пишем `start`
    - В панели появится поле `start`, нажимаем по нему
    - Появится еще одна панель, выбираем в ней вкладку `Headers`
    - Ищем поле `authorization`
    - Копируем его значение (начинается на **vk_access_token_settings**, **Bearer** копировать не нужно)
    - Вставляем скопированный текст в значение `authorization` в `config.json` между кавычками
  - my_id - **числовой** id вашей страницы ВКонтакте. Узнать можно через [сайт](https://regvk.com/id).

  - buy_slaves_mode - режим покупки рабов (0 - выкл, 1 - покупать случайных рабов, 2 - покупать рабов у игроков из топа, 3 - покупать рабов у людей из списка `"buy_from_ids"`)
  - buy_from_ids - ID людей через запятую, у которых вы хотите скупать рабов при `"mode": 3`. ID можно получить через [сайт](https://regvk.com/id).
  - buy_fetters - покупать ли оковы (0 - выкл, 1 - вкл)
  - upgrade_slaves - улучшать ли рабов для повышения дохода (0 - выкл, 1 - вкл)
  - min_price - минимальная цена для покупки раба. Значения выше 40 приведут к более долгому поиску рабов.
  - max_price - максимальная цена для покупки раба. Не советую ставить выше 26151, потому что это будет невыгодно.
  - max_fetter_price - максимальная цена для покупки оков.
  - job - какую давать работу. Если хотите, чтобы была только одна работа, пишите так: `"job": ["ИмяРаботы"]`, Если хотите, чтобы было несколько работ, среди которых выбиралась рандомная, пишите их через запятую, при этом берите каждое значение в кавычки, например: `"job": ["Повар", "Строитель", "Учитель", "Кассир"],`
  - delay - задержка между одинаковыми операциями в секундах. Чем ниже, тем выше вероятность получения бана на несколько часов.

Запуск: `start.bat`. Если после запуска ничего не происходит или выходит ошибка, связанная с Python или pip:

- Откройте `cmd`
- Напишите `python -V`
- Вывод должен соответстовать виду: `Python версия`. При этом версия должна быть выше **3.7**.
- Если вывод не соотвествует виду, нужно переустановить [Python](https://www.python.org/downloads/windows). Во время установки нужно поставить галочку `Add Python to Path (Добавить Python в PATH)`

## Установка на Termux (Android)

- Устанавливаем Termux, желательно с [F-Droid](https://f-droid.org/repo/com.termux_108.apk), т.к. в Google Play разработчик его больше не обновляет.
- Запускаем Termux.
- Пишем по порядку:
  - cd
  - pkg install -y git
  - git clone https://github.com/monosans/vk-slaves-bot
  - sh vk-slaves-bot/termux.sh
- Редактируем файл `config.json` командой `nano vk-slaves-bot/config.json` по инструкции для Windows. Для удобства редактирования можете скачать Hacker's Keyboard в Google Play, в ней в горизонтальном положении есть стрелочки для управления курсором. Чтобы получить `authorization` с телефона, можно использовать [приложение F12](https://play.google.com/store/apps/details?id=com.asfmapps.f12).
- Когда файл отредактирован, для сохранения нажмите Ctrl-O, Enter, Ctrl-X.

Запуск: `sh vk-slaves-bot/launch.sh`

## Переустановка в Termux

Ввести команды по порядку:

```
cd
rm -rf vk-slaves-bot
```

После этого заново установить по инструкции.

## Установка на Testflight (iOS)

Нужно установить Testflight из App Store. Что делать дальше, я не знаю, используйте гугл.
