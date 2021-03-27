#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from json import load
from random import randint, random
from threading import Thread
from time import sleep, strftime

from requests import get, post


def buy_slave():
    """Покупает рабов и оковы, если включено в config.json."""
    while True:
        try:
            if config["invisible_slaves"] == 1:
                # Случайный невидимый ID в промежутке
                rand_slave = randint(-999999999, -1)
            else:
                # Случайный ID пользователя в промежутке
                rand_slave = randint(1, 646735737)
            # Покупка раба
            buySlave = post(
                "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/buySlave",
                headers={
                    "Content-Type": "application/json",
                    "authorization": auth,
                    "User-agent": "Mozilla/5.0",
                },
                json={"slave_id": rand_slave},
            )

            # Получение информации о профиле
            profile = buySlave.json()

            print(
                f"""\n===[{strftime("%d.%m.%Y %H:%M:%S")}]===
Баланс: {profile['balance']}
Рабов: {profile['slaves_count']}
Доход в минуту: {profile['slaves_profit_per_min']}
===========================\n"""
            )

            # Покупает оковы только что купленному рабу
            if config["buy_fetters"] == 1 and config["invisible_fetters"] == 1:
                fetter_request = post(
                    "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/buyFetter",
                    headers={
                        "Content-Type": "application/json",
                        "authorization": auth,
                        "User-agent": "Mozilla/5.0",
                    },
                    json={
                        "slave_id": rand_slave,
                    },
                )
                fetter_text = fetter_request.json()
                print(f"Купил оковы vk.com/id{fetter_text['id']}")
            sleep(delay + random())
        except Exception as e:
            print(e.args)
            sleep(delay + random())


def buy_fetter():
    """Покупает оковы тем, у кого их нет."""
    while True:
        try:
            # Получение полной информации об аккаунте
            start = get(
                "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/start",
                headers={
                    "Content-Type": "application/json",
                    "authorization": auth,
                    "User-agent": "Mozilla/5.0",
                },
            ).json()

            # Перебор списка рабов
            for slave in start["slaves"]:
                # Проверка на наличие оков
                if int(slave["fetter_to"]) == 0 and int(slave["id"]) >= 1:
                    # Покупка оков
                    post(
                        "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/buyFetter",
                        headers={
                            "Content-Type": "application/json",
                            "authorization": auth,
                            "User-agent": "Mozilla/5.0",
                        },
                        json={
                            "slave_id": int(slave["id"]),
                        },
                    )
                    print(f"Купил оковы vk.com/id{slave['id']}")
                    sleep(delay + random())

                # Покупка оков невидимкам, если включено в конфиге
                elif (
                    int(slave["fetter_to"]) == 0
                    and config["invisible_fetters"] == 1
                ):
                    # Покупка оков
                    post(
                        "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/buyFetter",
                        headers={
                            "Content-Type": "application/json",
                            "authorization": auth,
                            "User-agent": "Mozilla/5.0",
                        },
                        json={
                            "slave_id": int(slave["id"]),
                        },
                    )
                    print(f"Купил оковы vk.com/id{slave['id']}")
                    sleep(delay + random())

        except Exception as e:
            print(e.args)
            sleep(delay + random())


def job_slave():
    """Даёт безработным работу."""
    while True:
        try:
            start = get(
                "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/start",
                headers={
                    "Content-Type": "application/json",
                    "authorization": auth,
                    "User-agent": "Mozilla/5.0",
                },
            ).json()

            # Перебор списка рабов
            for slave in start["slaves"]:
                # Проверка на наличие у раба работы
                if not slave["job"]["name"]:
                    # Даёт рабу работу
                    post(
                        "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/jobSlave",
                        headers={
                            "Content-Type": "application/json",
                            "authorization": auth,
                            "User-agent": "Mozilla/5.0",
                        },
                        json={
                            "slave_id": int(slave["id"]),
                            "name": job,
                        },
                    )

                    print(f"Дал работу vk.com/id{slave['id']}")
                    sleep(delay + random())
        except Exception as e:
            print(e.args)
            sleep(delay + random())


if __name__ == "__main__":
    print("Версия 0.9")

    # Конфиг
    with open("config.json") as f:
        try:
            config = load(f)
        except Exception as e:
            print("Неверный конфиг")
            sys.exit()
    auth = str(config["authorization"])
    delay = int(config["delay"])
    job = str(config["job"])

    # Запуск
    if int(config["buy_slaves"]) == 1:
        Thread(target=buy_slave).start()
    if int(config["buy_fetters"]) == 1:
        Thread(target=buy_fetter).start()
    Thread(target=job_slave).start()
