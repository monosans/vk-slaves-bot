#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from random import choice, randint, uniform
from threading import Thread
from time import sleep, strftime
from traceback import print_exc
from typing import Mapping

from requests import request

from config import (
    authorization,
    buy_fetters,
    buy_from_ids,
    buy_slaves_mode,
    jobs,
    max_delay,
    max_fetter_price,
    max_price,
    min_delay,
    min_price,
    my_id,
    upgrade_slaves,
)


def req(endpoint: str, json: Mapping = {}) -> Mapping:
    if json == {}:
        method = "GET"
    else:
        method = "POST"
    return request(
        method,
        f"https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/{endpoint}",
        json=json,
        headers={
            "authorization": authorization,
            "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.70 Safari/537.36",
            "origin": "https://prod-app7794757-c1ffb3285f12.pages-ac.vk-apps.com",
        },
    ).json()


def buy_slave(id: int) -> None:
    """Покупает раба."""
    req("buySlave", {"slave_id": id})


def get_buy_slave(id: int) -> Mapping:
    """Покупает раба."""
    return req("buySlave", {"slave_id": id})


def buy_fetter(id: int) -> None:
    """Покупает оковы."""
    req("buyFetter", {"slave_id": id})


def sell_slave(id: int) -> None:
    """Продаёт раба."""
    req("saleSlave", {"slave_id": id})


def job_slave(id: int) -> None:
    """Даёт работу."""
    req("jobSlave", {"slave_id": id, "name": choice(jobs)})


def get_user(id: int) -> Mapping:
    """Получает информацие о пользователе."""
    return req(f"user?id={id}")


def get_slave_list(id: int) -> Mapping:
    """Возвращает список рабов пользователя."""
    return req(f"slaveList?id={id}")


def get_top_users() -> Mapping:
    """Возвращает список топ игроков."""
    return req("topUsers")


def get_start() -> Mapping:
    """Получает полную информацию о своём профиле."""
    return req("start")


def upgrade_slave(slave_id: int) -> None:
    """Прокачивает раба, чтобы он приносил 1000 в минуту."""
    # Получение информации о себе
    me = get_user(my_id)

    # Проверка на то, дал ли нормальный сервер нормальный ответ
    if "balance" in me.keys():
        # Проверка на то, хватит ли баланса для прокачки
        if me["balance"] >= 39214:
            try:
                slave_info = get_user(slave_id)
                if "fetter_to" in slave_info.keys():
                    if slave_info["fetter_to"] == 0:
                        while slave_info["price"] <= 26151:
                            sell_slave(slave_id)
                            print(f"Продал id{slave_id} для улучшения")
                            buy_slave(slave_id)
                            print(f"Улучшил id{slave_id}")
                            sleep(uniform(min_delay, max_delay))
                            slave_info = get_user(slave_id)
            except Exception:
                print_exc()
                sleep(uniform(min_delay, max_delay))


def slaves_upgrade() -> None:
    """Прокачивает рабов, чтобы они приносили 1000 в минуту."""
    while True:
        try:
            start = get_start()
            if "slaves" in start.keys():
                # Перебор списка рабов
                for slave in start["slaves"]:
                    # me = get_user(my_id)
                    if "balance" in start.keys():
                        balance = start["balance"]
                        if balance >= 39214:
                            slave_info = get_user(slave["id"])
                            if "fetter_to" in slave_info.keys():
                                if slave_info["fetter_to"] == 0:
                                    while slave_info["price"] <= 26151:
                                        sell_slave(slave["id"])
                                        print(
                                            f"Продал id{slave['id']} для улучшения"
                                        )
                                        buy_slave(slave["id"])
                                        print(f"Улучшил id{slave['id']}")
                                        sleep(uniform(min_delay, max_delay))
                                        slave_info = get_user(slave["id"])
                                        balance = get_user(my_id)["balance"]
        except Exception:
            print_exc()
            sleep(uniform(min_delay, max_delay))


def buy_top_users_slaves() -> None:
    """То же самое, что и buy_slaves, только перекупает рабов у топ игроков."""
    while True:
        try:
            top_users = get_top_users()
            if "list" in top_users.keys():
                for top_user in top_users["list"]:
                    top_user_slaves = get_slave_list(top_user["id"])
                    if "slaves" in top_user_slaves.keys():
                        for slave in top_user_slaves["slaves"]:
                            if slave["fetter_to"] == 0:
                                slave_id = slave["id"]
                                slave_info = get_user(slave_id)
                                if "price" in slave_info.keys():
                                    if slave_info["price"] in range(
                                        min_price, max_price + 1
                                    ):
                                        slave = get_user(slave_id)

                                        # Покупка раба
                                        profile = get_buy_slave(slave_id)

                                        if "balance" in profile.keys():
                                            print(
                                                f"""[{strftime('%H:%M:%S')}]
Купил id{slave_info['id']} за {slave_info['price']} у id{top_user['id']}
Баланс: {'{:,}'.format(profile['balance'])}
Рабов: {'{:,}'.format(profile['slaves_count'])}
Доход в минуту: {'{:,}'.format(profile['slaves_profit_per_min'])}
Место в топе дохода: {'{:,}'.format(profile['rating_position'])}"""
                                            )

                                            # Прокачивает раба
                                            if upgrade_slaves == 1:
                                                upgrade_slave(slave_id)

                                            # Покупает оковы только что купленному рабу

                                            if (
                                                buy_fetters == 1
                                                and "fetter_price"
                                                in slave.keys()
                                            ):
                                                if (
                                                    slave["fetter_price"]
                                                    <= max_fetter_price
                                                ):
                                                    buy_fetter(slave_id)
                                                    print(
                                                        f"Купил оковы id{slave_id} за {slave['fetter_price']}"
                                                    )
                                        sleep(uniform(min_delay, max_delay))
        except Exception:
            print_exc()
            sleep(uniform(min_delay, max_delay))


def buy_slaves() -> None:
    """Покупает и улучшает рабов, надевает оковы, если включено в config.py."""
    while True:
        try:
            # Случайный раб в промежутке
            slave_id = randint(1, 649539349)
            slave_info = get_user(slave_id)

            # Проверка раба на соотвествие настройкам цены
            while slave_info["price"] not in range(min_price, max_price + 1):
                slave_id = randint(1, 649539349)
                slave_info = get_user(slave_id)

            slave = get_user(slave_id)

            # Покупка раба
            profile = get_buy_slave(slave_id)

            if "balance" in profile.keys():
                print(
                    f"""[{strftime('%H:%M:%S')}]
Купил id{slave_info['id']} за {slave_info['price']}
Баланс: {'{:,}'.format(profile['balance'])}
Рабов: {'{:,}'.format(profile['slaves_count'])}
Доход в минуту: {'{:,}'.format(profile['slaves_profit_per_min'])}
Место в топе дохода: {'{:,}'.format(profile['rating_position'])}"""
                )

                # Прокачивает раба
                if upgrade_slaves == 1:
                    upgrade_slave(slave_id)

                # Покупает оковы только что купленному рабу
                if buy_fetters == 1 and "fetter_price" in slave.keys():
                    if slave["fetter_price"] <= max_fetter_price:
                        buy_fetter(slave_id)
                        print(
                            f"Купил оковы id{slave_id} за {slave['fetter_price']}"
                        )
            sleep(uniform(min_delay, max_delay))
        except Exception:
            print_exc()
            sleep(uniform(min_delay, max_delay))


def buy_slaves_from_ids() -> None:
    """То же самое, что и buy_slaves, только перекупает рабов у buy_from_ids в config.py."""
    while True:
        try:
            for id in buy_from_ids:
                slaves = get_slave_list(id)
                if "slaves" in slaves.keys():
                    for slave in slaves["slaves"]:
                        if slave["fetter_to"] == 0:
                            slave_id = slave["id"]
                            slave_info = get_user(slave_id)
                            if "price" in slave_info.keys():
                                if slave_info["price"] in range(
                                    min_price, max_price + 1
                                ):
                                    slave = get_user(slave_id)

                                    # Покупка раба
                                    profile = get_buy_slave(slave_id)

                                    if "balance" in profile.keys():
                                        print(
                                            f"""[{strftime('%H:%M:%S')}]
Купил id{slave_info['id']} за {slave_info['price']} у id{id}
Баланс: {'{:,}'.format(profile['balance'])}
Рабов: {'{:,}'.format(profile['slaves_count'])}
Доход в минуту: {'{:,}'.format(profile['slaves_profit_per_min'])}
Место в топе дохода: {'{:,}'.format(profile['rating_position'])}"""
                                        )

                                        # Прокачивает раба
                                        if upgrade_slaves == 1:
                                            upgrade_slave(slave_id)

                                        # Покупает оковы только что купленному рабу
                                        if (
                                            buy_fetters == 1
                                            and "fetter_price" in slave.keys()
                                        ):
                                            if (
                                                slave["fetter_price"]
                                                <= max_fetter_price
                                            ):
                                                buy_fetter(slave_id)
                                                print(
                                                    f"Купил оковы id{slave_id} за {slave['fetter_price']}"
                                                )
                                    sleep(uniform(min_delay, max_delay))
        except Exception:
            print_exc()
            sleep(uniform(min_delay, max_delay))


def set_fetters() -> None:
    """Покупает оковы тем, у кого их нет."""
    while True:
        try:
            start = get_start()
            if "slaves" in start.keys():
                slaves = start["slaves"]
                # Удаление первого раба из списка,
                # чтобы не происходило коллизии с прокачкой
                if upgrade_slaves == 1:
                    del slaves[0]

                # Перебор списка рабов
                for slave in slaves:
                    # Проверка на наличие оков
                    if slave["fetter_to"] == 0:
                        if slave["fetter_price"] <= max_fetter_price:
                            buy_fetter(slave["id"])
                            print(
                                f"Купил оковы id{slave['id']} за {slave['fetter_price']}"
                            )
                            sleep(uniform(min_delay, max_delay))
        except Exception:
            print_exc()
            sleep(uniform(min_delay, max_delay))


def job_slaves() -> None:
    """Даёт безработным работу."""
    while True:
        try:
            start = get_start()
            if "slaves" in start.keys():
                slaves = start["slaves"]
                if buy_slaves_mode == 0 and buy_fetters == 1:
                    del slaves[0]
                # Перебор списка рабов
                for slave in slaves:
                    # Проверка на наличие у раба работы
                    if not slave["job"]["name"]:
                        job_slave(slave["id"])
                        print(f"Дал работу id{slave['id']}")
                        sleep(uniform(min_delay, max_delay))
        except Exception:
            print_exc()
            sleep(uniform(min_delay, max_delay))


if __name__ == "__main__":
    print(
        """vk.com/free_slaves_bot
github.com/monosans/vk-slaves-bot
Версия 4.0"""
    )
    # Запуск
    if buy_slaves_mode == 1:
        print("Включена покупка случайных рабов")
        Thread(target=buy_slaves).start()
    elif buy_slaves_mode == 2:
        print("Включена перекупка у топеров")
        Thread(target=buy_top_users_slaves).start()
    elif buy_slaves_mode == 3:
        print("Включена перекупка у buy_from_ids из config.py")
        Thread(target=buy_slaves_from_ids).start()
    elif upgrade_slaves == 1 and buy_slaves_mode == 0:
        Thread(target=slaves_upgrade).start()
    if buy_fetters == 1:
        Thread(target=set_fetters).start()
    Thread(target=job_slaves).start()
