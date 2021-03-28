#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from json import load
from random import choice, randint, random
from threading import Thread
from time import sleep, strftime

from requests import get, post


def buy_slave(id):
    """Покупает раба."""
    post(
        "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/buySlave",
        headers={
            "Content-Type": "application/json",
            "authorization": auth,
            "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Safari/537.36",
            "origin": "https://prod-app7794757-c1ffb3285f12.pages-ac.vk-apps.com",
        },
        json={"slave_id": id},
    )


def buy_fetter(id):
    """Покупает оковы."""
    post(
        "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/buyFetter",
        headers={
            "Content-Type": "application/json",
            "authorization": auth,
            "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Safari/537.36",
            "origin": "https://prod-app7794757-c1ffb3285f12.pages-ac.vk-apps.com",
        },
        json={"slave_id": id},
    )


def get_start():
    """Получает полную информацию о своём профиле."""
    return get(
        "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/start",
        headers={
            "Content-Type": "application/json",
            "authorization": auth,
            "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Safari/537.36",
            "origin": "https://prod-app7794757-c1ffb3285f12.pages-ac.vk-apps.com",
        },
    ).json()


def sell_slave(id):
    """Продаёт раба."""
    post(
        "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/saleSlave",
        headers={
            "Content-Type": "application/json",
            "authorization": auth,
            "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Safari/537.36",
            "origin": "https://prod-app7794757-c1ffb3285f12.pages-ac.vk-apps.com",
        },
        json={"slave_id": id},
    )


def job_slave(id):
    """Даёт работу."""
    post(
        "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/jobSlave",
        headers={
            "Content-Type": "application/json",
            "authorization": auth,
            "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Safari/537.36",
            "origin": "https://prod-app7794757-c1ffb3285f12.pages-ac.vk-apps.com",
        },
        json={
            "slave_id": id,
            "name": choice(job),
        },
    )


def get_user(id):
    """Получает информацие о пользователе."""
    return get(
        "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/user",
        headers={
            "Content-Type": "application/json",
            "authorization": auth,
            "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Safari/537.36",
            "origin": "https://prod-app7794757-c1ffb3285f12.pages-ac.vk-apps.com",
        },
        params={"id": id},
    ).json()


def buy_slaves():
    """Покупает и улучшает рабов, надевает оковы, если включено в config.json."""
    while True:
        try:
            # Случайный раб в промежутке
            rand_slave = randint(1, 646735737)
            rand_slave_info = get_user(rand_slave)

            # Проверка раба на соотвествие настройкам цены
            while not (
                int(rand_slave_info["price"]) <= max_price
                and int(rand_slave_info["price"]) >= min_price
            ):
                rand_slave = randint(1, 646735737)
                rand_slave_info = get_user(rand_slave)

            # Покупка раба
            buy_slave(rand_slave)

            # Получение информации о себе
            me = get_user(my_id)

            print(
                f"""\n==[{strftime("%d.%m.%Y %H:%M:%S")}]==
Купил vk.com/id{rand_slave} за {rand_slave_info["price"]}
Баланс: {"{:,}".format(me['balance'])}
Рабов: {"{:,}".format(me['slaves_count'])}
Доход в минуту: {"{:,}".format(me['slaves_profit_per_min'])}
Место в рейтинге: {"{:,}".format(me['rating_position'])}\n""",
            )
            if upgrade_slaves == 1:
                # Перебор списка рабов
                if "balance" in me.keys():
                    # Проверка на то, хватит ли баланса для прокачки
                    if int(me["balance"]) >= 39214:
                        while int(get_user(rand_slave)["price"]) <= 26151:
                            sell_slave(rand_slave)
                            print("Продал раба для улучшения")
                            buy_slave(rand_slave)
                            print("Улучшил раба")
                            sleep(delay + random())

            # Покупает оковы только что купленному рабу
            if buy_fetters == 1:
                buy_fetter(rand_slave)
                print(f"Купил оковы vk.com/id{rand_slave}")

            sleep(delay + random())
        except Exception as e:
            print(e.args)
            sleep(delay + random())


def buy_fetters():
    """Покупает оковы тем, у кого их нет."""
    while True:
        try:
            # Получение полной информации об аккаунте
            start = get_start()

            # Перебор списка рабов
            for slave in start["slaves"]:
                # Проверка на наличие оков
                if int(slave["fetter_to"]) == 0:
                    buy_fetter(slave["id"])
                    print(f"Купил оковы vk.com/id{slave['id']}")
                    sleep(delay + random())
        except Exception as e:
            print(e.args)
            sleep(delay + random())


def job_slaves():
    """Даёт безработным работу."""
    while True:
        try:
            # Получение полной информации об аккаунте
            start = get_start()

            # Перебор списка рабов
            for slave in start["slaves"]:
                # Проверка на наличие у раба работы
                if not slave["job"]["name"]:
                    job_slave(slave["id"])
                    print(f"Дал работу vk.com/id{slave['id']}")
                    sleep(delay + random())
        except Exception as e:
            print(e.args)
            sleep(delay + random())


if __name__ == "__main__":
    print(
        """vk.com/free_slaves_bot
github.com/monosans/vk-slaves-bot
Версия 2.2""",
    )

    # Конфиг
    with open("config.json") as f:
        try:
            config = load(f)
        except:
            print("Неверный конфиг")
            sys.exit()
    auth = str(config["authorization"])
    conf_buy_fetters = int(config["buy_fetters"])
    conf_buy_slaves = int(config["buy_slaves"])
    delay = int(config["delay"])
    try:
        job = list(config["job"])
    except:
        job = str(config["job"])
    max_price = int(config["max_price"])
    min_price = int(config["min_price"])
    my_id = int(config["my_id"])
    upgrade_slaves = int(config["upgrade_slaves"])

    # Запуск
    if conf_buy_slaves == 1:
        Thread(target=buy_slaves).start()
    if conf_buy_fetters == 1:
        Thread(target=buy_fetters).start()
    Thread(target=job_slaves).start()
