#!/usr/bin/env python3

"""Versiya dlya teh, u kogo pri zapuske oshibka Non-ASCII character"""

from json import load, loads
from random import randint
from threading import Thread
from time import sleep

import requests


def buy_slave():
    while True:
        try:
            rand_slave = randint(1, 646412830)
            buySlave = requests.post(
                "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/buySlave",
                headers={
                    "Content-Type": "application/json",
                    "authorization": auth,
                },
                json={"slave_id": rand_slave},
            )
            profile = loads(buySlave.text)
            print(
                f"""Balance: {profile['balance']}
Rabov: {profile['slaves_count']}
Dohod d minutu: {profile['slaves_profit_per_min']}"""
            )
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
            print(f"Dal rabotu vk.com/id{loads(job_text)['slave']['id']}")
            if config["buy_fetters"] == 1:
                fetter_request = requests.post(
                    "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/buyFetter",
                    headers={
                        "Content-Type": "application/json",
                        "authorization": auth,
                    },
                    json={
                        "slave_id": rand_slave,
                    },
                )
                fetter_text = fetter_request.text
                print(f"Kupil okovy vk.com/id{loads(fetter_text)['id']}")
            sleep(delay + randint(-1, 1))
        except Exception as e:
            print(e)


def buy_fetter():
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
            for slave in start["slaves"]:
                if slave["fetter_to"] == 0:
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
                    print(f"Kupil okovy vk.com/id{slave['id']}")
                    sleep(delay + randint(-1, 1))
        except Exception as e:
            print(e)


def job_slave():
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
            for slave in start["slaves"]:
                if not slave["job"]["name"]:
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
                    print(f"Dal rabotu vk.com/id{slave['id']}")
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
