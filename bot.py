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
            "User-agent": "Mozilla/5.0",
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
            "User-agent": "Mozilla/5.0",
            "origin": "https://prod-app7794757-c1ffb3285f12.pages-ac.vk-apps.com",
        },
        json={"slave_id": id},
    )


def sell_slave(id):
    """Продаёт раба."""
    post(
        "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/saleSlave",
        headers={
            "Content-Type": "application/json",
            "authorization": auth,
            "User-agent": "Mozilla/5.0",
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
            "User-agent": "Mozilla/5.0",
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
        f"https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/user?id={id}",
        headers={
            "Content-Type": "application/json",
            "authorization": auth,
            "User-agent": "Mozilla/5.0",
            "origin": "https://prod-app7794757-c1ffb3285f12.pages-ac.vk-apps.com",
        },
    ).json()


def get_slave_list(id):
    """Возвращает список рабов пользователя."""
    return get(
        f"https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/slaveList?id={id}",
        headers={
            "Content-Type": "application/json",
            "authorization": auth,
            "User-agent": "Mozilla/5.0",
            "origin": "https://prod-app7794757-c1ffb3285f12.pages-ac.vk-apps.com",
        },
    ).json()


def get_top_users():
    """Возвращает список топ игроков."""
    return get(
        "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/topUsers",
        headers={
            "Content-Type": "application/json",
            "authorization": auth,
            "User-agent": "Mozilla/5.0",
            "origin": "https://prod-app7794757-c1ffb3285f12.pages-ac.vk-apps.com",
        },
    ).json()


def get_start():
    """Получает полную информацию о своём профиле."""
    return get(
        "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/start",
        headers={
            "Content-Type": "application/json",
            "authorization": auth,
            "User-agent": "Mozilla/5.0",
            "origin": "https://prod-app7794757-c1ffb3285f12.pages-ac.vk-apps.com",
        },
    ).json()


def upgrade_slave(me, slave_id):
    """Прокачивает раба, чтобы он приносил 1000 в минуту."""
    # Проверка на то, дал ли нормальный сервер нормальный ответ
    if "balance" in me.keys():
        # Проверка на то, хватит ли баланса для прокачки
        if int(me["balance"]) >= 39214:
            try:
                slave_price = int(get_user(slave_id)["price"])
                while slave_price <= 26151:
                    sell_slave(slave_id)
                    print(f"Продал id{slave_id} для улучшения")
                    buy_slave(slave_id)
                    print(f"Улучшил id{slave_id}")
                    sleep(delay + random())
                    slave_price = int(get_user(slave_id)["price"])
            except Exception as e:
                print(e.args)
                sleep(delay + random())
                pass


def upgrade_slaves():
    """Прокачивает рабов, чтобы они приносили 1000 в минуту."""
    while True:
        try:
            # Перебор списка рабов
            for slave in get_start()["slaves"]:
                balance = get_user(my_id)["balance"]
                if int(balance) >= 39214:
                    slave_price = get_user(slave["id"])["price"]
                    while int(slave_price) <= 26151:
                        sell_slave(slave["id"])
                        print(f"Продал id{slave['id']} для улучшения")
                        buy_slave(slave["id"])
                        print(f"Улучшил id{slave['id']}")
                        sleep(delay + random())
                        slave_price = get_user(slave["id"])["price"]
                    balance = get_user(my_id)["balance"]
        except Exception as e:
            print(e.args)
            sleep(delay + random())


def buy_top_users_slaves():
    """То же самое, что и buy_slaves, только перекупает рабов у топ игроков."""
    while True:
        try:
            top_users = get_top_users()
            if "list" in top_users.keys():
                for top_user in top_users["list"]:
                    top_user_slaves = get_slave_list(int(top_user["id"]))
                    if "slaves" in top_user_slaves.keys():
                        for slave in top_user_slaves["slaves"]:
                            if int(slave["fetter_to"]) == 0:
                                slave_id = slave["id"]
                                slave_info = get_user(slave_id)
                                if (
                                    slave_info["price"] <= max_price
                                    and slave_info["price"] >= min_price
                                ):
                                    # Покупка раба
                                    buy_slave(slave_id)

                                    # Получение информации о себе
                                    me = get_user(my_id)

                                    print(
                                        f"""\n==[{strftime("%d.%m.%Y %H:%M:%S")}]==
Купил id{slave_info["id"]} за {slave_info["price"]} у id{top_user["id"]}
Баланс: {"{:,}".format(me['balance'])}
Рабов: {"{:,}".format(me['slaves_count'])}
Доход в минуту: {"{:,}".format(me['slaves_profit_per_min'])}
Место в рейтинге: {"{:,}".format(me['rating_position'])}\n""",
                                    )

                                    # Прокачивает раба
                                    if conf_upgrade_slaves == 1:
                                        upgrade_slave(me, slave_id)

                                    # Покупает оковы только что купленному рабу
                                    if buy_fetters == 1:
                                        fetter_price = int(
                                            get_user(slave_id)["fetter_price"]
                                        )
                                        if fetter_price <= max_fetter_price:
                                            buy_fetter(slave_id)
                                            print(
                                                f"Купил оковы vk.com/id{slave_id} за {fetter_price}"
                                            )
                                    sleep(delay + random())
        except Exception as e:
            print(e.args)
            sleep(delay + random())


def buy_slaves():
    """Покупает и улучшает рабов, надевает оковы, если включено в config.json."""
    while True:
        try:
            # Случайный раб в промежутке
            slave_id = randint(1, 646959225)
            slave_info = get_user(slave_id)

            # Проверка раба на соотвествие настройкам цены
            while (
                int(slave_info["price"]) > max_price
                or int(slave_info["price"]) < min_price
            ):
                slave_id = randint(1, 646959225)
                slave_info = get_user(slave_id)

            # Покупка раба
            buy_slave(slave_id)

            # Получение информации о себе
            me = get_user(my_id)

            print(
                f"""\n==[{strftime("%d.%m.%Y %H:%M:%S")}]==
Купил id{slave_info["id"]} за {slave_info["price"]}
Баланс: {"{:,}".format(me['balance'])}
Рабов: {"{:,}".format(me['slaves_count'])}
Доход в минуту: {"{:,}".format(me['slaves_profit_per_min'])}
Место в рейтинге: {"{:,}".format(me['rating_position'])}\n""",
            )

            # Прокачивает раба
            if conf_upgrade_slaves == 1:
                upgrade_slave(me, slave_id)

            # Покупает оковы только что купленному рабу
            if buy_fetters == 1:
                fetter_price = int(get_user(slave_id)["fetter_price"])
                if fetter_price <= max_fetter_price:
                    buy_fetter(slave_id)
                    print(f"Купил оковы vk.com/id{slave_id} за {fetter_price}")

            sleep(delay + random())
        except Exception as e:
            print(e.args)
            sleep(delay + random())


def buy_from_ids():
    """То же самое, что и buy_slaves, только перекупает рабов из списка в config.json."""
    while True:
        try:
            for id in buy_from_ids_list:
                slaves = get_slave_list(int(id))
                if "slaves" in slaves.keys():
                    for slave in slaves["slaves"]:
                        if int(slave["fetter_to"]) == 0:
                            slave_id = slave["id"]
                            slave_info = get_user(slave_id)
                            if (
                                slave_info["price"] <= max_price
                                and slave_info["price"] >= min_price
                            ):
                                # Покупка раба
                                buy_slave(slave_id)

                                # Получение информации о себе
                                me = get_user(my_id)

                                print(
                                    f"""\n==[{strftime("%d.%m.%Y %H:%M:%S")}]==
Купил id{slave_info["id"]} за {slave_info["price"]} у id{id}
Баланс: {"{:,}".format(me['balance'])}
Рабов: {"{:,}".format(me['slaves_count'])}
Доход в минуту: {"{:,}".format(me['slaves_profit_per_min'])}
Место в рейтинге: {"{:,}".format(me['rating_position'])}\n""",
                                )

                                # Прокачивает раба
                                if conf_upgrade_slaves == 1:
                                    upgrade_slave(me, slave_id)

                                # Покупает оковы только что купленному рабу
                                if buy_fetters == 1:
                                    fetter_price = int(
                                        get_user(slave_id)["fetter_price"]
                                    )
                                    if fetter_price <= max_fetter_price:
                                        buy_fetter(slave_id)
                                        print(
                                            f"Купил оковы vk.com/id{slave_id} за {fetter_price}"
                                        )
                                sleep(delay + random())
        except Exception as e:
            print(e.args)
            sleep(delay + random())


def buy_fetters():
    """Покупает оковы тем, у кого их нет."""
    while True:
        try:
            slaves = get_start()["slaves"]

            # Удаление первого раба из списка,
            # чтобы не происходило коллизии с прокачкой
            if conf_upgrade_slaves == 1:
                del slaves[0]

            # Перебор списка рабов
            for slave in slaves:
                # Проверка на наличие оков
                if int(slave["fetter_to"]) == 0:
                    fetter_price = int(get_user(slave["id"])["fetter_price"])
                    if fetter_price <= max_fetter_price:
                        buy_fetter(slave["id"])
                        print(
                            f"Купил оковы vk.com/id{slave['id']} за {fetter_price}"
                        )
                        sleep(delay + random())
        except Exception as e:
            print(e.args)
            sleep(delay + random())


def job_slaves():
    """Даёт безработным работу."""
    while True:
        try:
            slaves = get_start()["slaves"]
            if buy_slaves_mode == 0 and conf_buy_fetters == 1:
                del slaves[0]
            # Перебор списка рабов
            for slave in slaves:
                # Проверка на наличие у раба работы
                if not slave["job"]["name"]:
                    job_slave(int(slave["id"]))
                    print(f"Дал работу id{slave['id']}")
                    sleep(delay + random())
        except Exception as e:
            print(e.args)
            sleep(delay + random())


if __name__ == "__main__":
    print(
        """vk.com/free_slaves_bot
github.com/monosans/vk-slaves-bot
Версия 3.8""",
    )

    # Конфиг
    with open("config.json") as f:
        try:
            config = load(f)
        except:
            print("Неверный конфиг")
            sys.exit()
    auth = str(config["authorization"])
    buy_slaves_mode = int(config["buy_slaves_mode"])
    conf_buy_fetters = int(config["buy_fetters"])
    max_fetter_price = int(config["max_fetter_price"])
    delay = int(config["delay"])
    try:
        job = list(config["job"])
    except:
        job = str(config["job"])
    min_price = int(config["min_price"])
    max_price = int(config["max_price"])
    my_id = int(config["my_id"])
    conf_upgrade_slaves = int(config["upgrade_slaves"])
    buy_from_ids_list = list(config["buy_from_ids"])
    if buy_slaves_mode == 1:
        print("Включена покупка случайных рабов.")
        Thread(target=buy_slaves).start()
    elif buy_slaves_mode == 2:
        print("Включена перекупка рабов у топеров.")
        Thread(target=buy_top_users_slaves).start()
    elif buy_slaves_mode == 3:
        print("Включена перекупка у IDшников из config.json.")
        Thread(target=buy_from_ids).start()
    if conf_upgrade_slaves == 1 and buy_slaves_mode == 0:
        Thread(target=upgrade_slaves).start()
    if conf_buy_fetters == 1:
        Thread(target=buy_fetters).start()
    Thread(target=job_slaves).start()
