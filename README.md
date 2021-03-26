# vk-slaves-bot

Бот для мини-игры ["Рабы" ("Рабство")](https://vk.com/app7794757) ВК

[Группа в ВК](https://vk.com/club203543653), в ней будет публиковаться информация об обновлениях.

**Если возникают какие-либо проблемы при установке или использовании, пишите в ВК [@id607137534](https://vk.com/id607137534).**

**Лучшая благодарность - звёздочка на GitHub и "спасибо" в [ЛС в ВК](https://vk.com/id607137534).**

**Если хотите отблагодарить материально, пишите в [ЛС](https://vk.com/id607137534).**

## В консоль спамит **'balance'** или **'slaves'**. Что делать?

Возможные причины такого поведения:

- Неправильный `authorization` в `config.json`. Зайдите в игру, проверьте, прибавляется ли количество рабов.
- Бан не несколько часов. Попробуйте купить раба вручную. Если выходит ошибка `ErrFloodBuy`, значит у Вас бан на несколько часов. Если бан был получен при использовании этого бота, попробуйте повысить `delay` в `config.json`.

Если ни один из перечисленных пунктов к Вам 100% не относится, вместо start.bat (или bot.py), запустите debug.bat (или debug.py). Дайте ему поработать секунд 15 и закройте. В папке с ботом появятся новые json файлы (profile, buySlavesFetter, buySlavesJob, fetterStart, jobStart). Если в json файлах написано Server Error, на это может быть несколько причин:

- Проблемы с Интернетом у Вас.
- Проблемы с сервером, никак не касающиеся ни меня, ни Вас.

## При запуске ошибка **SyntaxError: Non-ASCII character**

Вместо **bot.py** используйте **ascii.py**. На Windows запускайте через **start-ascii.bat**.

## Установка на Windows

- Устанавливаем [Python](https://www.python.org/downloads/windows). Во время установки ставим галочку `Add Python to PATH (Добавить Python в PATH)`
- [Скачиваем архив с ботом](https://github.com/monosans/vk-slaves-bot/archive/refs/heads/main.zip).
- Распаковываем архив.
- Редактируем файл `config.json`:
  - authorization:
    - Открываем ВК
    - Нажимаем `F12` (Для Chromium браузеров)
    - В появившейся панели выбираем вкладку `Network`
    - Находим кнопку `Filter` (воронка)
    - В появившемся поле пишем `buySlave`
    - Покупаем любого раба
    - В панели появится поле `buySlave`, нажимаем по нему
    - Появится еще одна панель, выбираем в ней вкладку `Headers`
    - Ищем поле `authorization`
    - Копируем его значение (начинается на **vk_access_token_settings**)
    - Вставляем скопированный текст в значение `authorization` в `config.json`
  - buy_slaves - покупать ли рабов (0 - выкл, 1 - вкл)
  - buy_fetters - покупать ли оковы (0 - выкл, 1 - вкл)
  - job - какую давать работу
  - delay - задержка в секундах. Низкие значения приведут к бану на несколько часов. Программа работает только при значении больше 1.0

Запуск: `start.bat`.
Если при запуске вылетает:

- Откройте `cmd`
- Напишите **python -V**
- Вывод должен соответстовать виду: `Python версия`. При этом версия должна быть выше **3.7**.
- Если вывод не соотвествует виду, нужно переустановить [Python](https://www.python.org/downloads/windows). Во время установки нужно поставить галочку `Add Python to Path (Добавить Python в PATH)`

## Установка на Termux (Android)

- Устанавливаем Termux, желательно с F-Droid, т.к. в Google Play разработчик его больше не обновляет.
- Запускаем Termux.
- Пишем по порядку:
  - cd
  - pkg install -y git
  - git clone https://github.com/monosans/vk-slaves-bot
  - sh vk-slaves-bot/termux.sh
- Редактируем файл `config.json` по инструкции для Windows или перекидываем с компьютера имеющийся. Как сделать это, можете посмотреть на YouTube или почитать в интернете.

Запуск: `sh vk-slaves-bot/launch.sh`

## Установка на Testflight (iOS)

Возможно, инструкция скоро появится.
