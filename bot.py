#!/usr/bin/env python3
from json import load, loads
from random import randint
from threading import Thread
from time import sleep

import requests


def buy_slave():
    """
    Покупает рабов, даёт работу. Надевает оковы, если включено в config.json.
    """
    while True:
        try:
            # Случайный ID пользователя в промежутке
            rand_slave = randint(1, 646306305)

            # Покупка раба
            buySlave = requests.post(
                "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/buySlave",
                headers={
                    "Content-Type": "application/json",
                    "authorization": auth,
                },
                json={"slave_id": rand_slave},
            )

            # Вывод информации о профиле
            profile = loads(buySlave.text)
            print(
                f"""Баланс: {profile["balance"]}
Рабов: {profile["slaves_count"]}
Доход в минуту: {profile["slaves_profit_per_min"]}"""
            )

            # Даёт рабу работу
            job_request = requests.post(
                "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/jobSlave",
                headers={
                    "Content-Type": "application/json",
                    "authorization": auth,
                },
                json={
                    "slave_id": rand_slave,
                    "name": job,
                },
            )
            job_text = job_request.text
            print(f"Дал работу vk.com/id{loads(job_text)['slave']['id']}")

            # Надевает оковы
            # if config["buy_fetters"] == 1:
            #     fetter_request = requests.post(
            #         "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/buyFetter",
            #         headers={
            #             "Content-Type": "application/json",
            #             "authorization": auth,
            #         },
            #         json={
            #             "slave_id": rand_slave,
            #         },
            #     )
            #     fetter_text = fetter_request.text
            #     print(f"Купил оковы vk.com/id{loads(fetter_text)['id']}")

            # Задержка для обхода бана за флуд
            sleep(delay + randint(-1, 1))
        except Exception as e:
            print(e)


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
                    },
                ).text,
            )

            # Перебор списка рабов
            for slave in start["slaves"]:
                # Проверка на наличие оков
                if slave["fetter_to"] == 0:
                    # Покупка оков
                    requests.post(
                        "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/buyFetter",
                        headers={
                            "Content-Type": "application/json",
                            "authorization": auth,
                        },
                        json={
                            "slave_id": slave["id"],
                        },
                    )
                    print(f"Купил оковы vk.com/id{slave['id']}")

                    # Задержка для обхода бана за флуд
                    sleep(delay + randint(-1, 1))
        except Exception as e:
            print(e)


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
                        },
                        json={
                            "slave_id": slave["id"],
                            "name": job,
                        },
                    )
                    print(f"Дал работу vk.com/id{slave['id']}")

                    # Задержка для обхода бана за флуд
                    sleep(delay + randint(-1, 1))
        except Exception as e:
            print(e)


if __name__ == "__main__":
    with open("config.json") as f:
        config = load(f)
    auth = config["authorization"]
    delay = config["delay"]
    job = config["job"]
    if config["buy_slaves"] == 1:
        Thread(target=buy_slave).start()
    if config["buy_fetters"] == 1:
        Thread(target=buy_fetter).start()
    Thread(target=job_slave).start()
