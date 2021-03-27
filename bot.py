#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from json import load, loads
from random import randint, random
from threading import Thread
from time import sleep

import requests


def buy_slave():
    """
    Покупает рабов, даёт работу. Надевает оковы, если включено в config.json.
    """
    while True:
        try:
            if config["invisible_slaves"] == 1:
                # Случайный невидимый ID в промежутке
                rand_slave = randint(-999999999, -1)
            else:
                # Случайный ID пользователя в промежутке
                rand_slave = randint(1, 646412830)
            # Покупка раба
            buySlave = requests.post(
                "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/buySlave",
                headers={
                    "Content-Type": "application/json",
                    "authorization": auth,
                    "User-agent": "Mozilla/5.0",
                },
                json={"slave_id": rand_slave},
            )

            # Вывод информации о профиле
            profile = loads(buySlave.text)
            print(
                f"""Баланс: {profile['balance']}
Рабов: {profile['slaves_count']}
Доход в минуту: {profile['slaves_profit_per_min']}"""
            )

            # Покупает оковы
            if config["buy_fetters"] == 1:
                fetter_request = requests.post(
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
                fetter_text = fetter_request.text
                print(f"Купил оковы vk.com/id{loads(fetter_text)['id']}")
                sleep(delay + random())
        except Exception as e:
            if not "line" in str(e):
                print(e)
            sleep(delay + random())


def buy_fetter():
    """Покупает оковы тем, у кого их нет."""
    while True:
        try:
            # Получение полной информации об аккаунте
            start = loads(
                requests.get(
                    "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/start",
                    headers={
                        "Content-Type": "application/json",
                        "authorization": auth,
                        "User-agent": "Mozilla/5.0",
                    },
                ).text,
            )

            if config["buy_slaves"] == 1:
                # Удаление из списка первого раба,
                # чтобы не происходило коллизии с методом buy_slave
                del start["slaves"][0]
            # Перебор списка рабов
            for slave in start["slaves"]:
                # Проверка на наличие оков
                if slave["fetter_to"] == 0 and slave["id"] >= 1:
                    # Покупка оков
                    requests.post(
                        "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/buyFetter",
                        headers={
                            "Content-Type": "application/json",
                            "authorization": auth,
                            "User-agent": "Mozilla/5.0",
                        },
                        json={
                            "slave_id": slave["id"],
                        },
                    )
                    print(f"Купил оковы vk.com/id{slave['id']}")
                    sleep(delay + random())
        except Exception as e:
            if not "line" in str(e):
            	print(e)
            sleep(delay + random())


def job_slave():
    """Даёт безработным работу."""
    while True:
        try:
            start = loads(
                requests.get(
                    "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/start",
                    headers={
                        "Content-Type": "application/json",
                        "authorization": auth,
                        "User-agent": "Mozilla/5.0",
                    },
                ).text,
            )

            # Перебор списка рабов
            for slave in start["slaves"]:
                # Проверка на наличие у раба работы
                if not slave["job"]["name"]:
                    # Даёт рабу работу
                    requests.post(
                        "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/jobSlave",
                        headers={
                            "Content-Type": "application/json",
                            "authorization": auth,
                            "User-agent": "Mozilla/5.0",
                        },
                        json={
                            "slave_id": slave["id"],
                            "name": job,
                        },
                    )
                    print(f"Дал работу vk.com/id{slave['id']}")
                    sleep(delay + random())
        except Exception as e:
            if not "line" in str(e):
            	print(e)
            sleep(delay + random())


if __name__ == "__main__":
    with open("config.json") as f:
        config = load(f)
    auth = config["authorization"]
    delay = config["delay"]
    job = config["job"]
    print("Бот запущен")
    if config["buy_slaves"] == 1:
        Thread(target=buy_slave).start()
    if config["buy_fetters"] == 1:
        Thread(target=buy_fetter).start()
    Thread(target=job_slave).start()
