#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from random import choice, randint, uniform
from threading import Thread
from time import sleep, strftime

from requests import get, post

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


def buy_slave(id):
    """Покупает раба."""
    post(
        "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/buySlave",
        headers=headers,
        json={"slave_id": id},
    )


def get_buy_slave(id):
    """Покупает раба."""
    return post(
        "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/buySlave",
        headers=headers,
        json={"slave_id": id},
    ).json()


def buy_fetter(id):
    """Покупает оковы."""
    post(
        "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/buyFetter",
        headers=headers,
        json={"slave_id": id},
    )


def sell_slave(id):
    """Продаёт раба."""
    post(
        "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/saleSlave",
        headers=headers,
        json={"slave_id": id},
    )


def job_slave(id):
    """Даёт работу."""
    post(
        "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/jobSlave",
        headers=headers,
        json={
            "slave_id": id,
            "name": choice(jobs),
        },
    )


def get_user(id):
    """Получает информацие о пользователе."""
    return get(
        f"https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/user?id={id}",
        headers=headers,
    ).json()


def get_slave_list(id):
    """Возвращает список рабов пользователя."""
    return get(
        f"https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/slaveList?id={id}",
        headers=headers,
    ).json()


def get_top_users():
    """Возвращает список топ игроков."""
    return get(
        "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/topUsers",
        headers=headers,
    ).json()


def get_start():
    """Получает полную информацию о своём профиле."""
    return get(
        "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/start",
        headers=headers,
    ).json()


def upgrade_slave(slave_id):
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
            except Exception as e:
                print(e.args)
                sleep(uniform(min_delay, max_delay))
                pass


def slaves_upgrade():
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
                                            f"Продал id{slave['id']} для улучшения",
                                        )
                                        buy_slave(slave["id"])
                                        print(f"Улучшил id{slave['id']}")
                                        sleep(uniform(min_delay, max_delay))
                                        slave_info = get_user(slave["id"])
                                        balance = get_user(my_id)["balance"]
        except Exception as e:
            print(e.args)
            sleep(uniform(min_delay, max_delay))


def buy_top_users_slaves():
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
                                    if (
                                        slave_info["price"] <= max_price
                                        and slave_info["price"] >= min_price
                                    ):
                                        # Узнаем заранее цену на оковы,
                                        # чтобы в будущем моментально их купить
                                        fetter_price = get_user(slave_id)[
                                            "fetter_price"
                                        ]

                                        # Покупка раба
                                        profile = get_buy_slave(slave_id)

                                        print(
                                            f"""[{strftime("%H:%M:%S")}]
Купил id{slave_info["id"]} за {slave_info["price"]} у id{top_user["id"]}
Баланс: {"{:,}".format(profile['balance'])}
Рабов: {"{:,}".format(profile['slaves_count'])}
Доход в минуту: {"{:,}".format(profile['slaves_profit_per_min'])}
Место в топе дохода: {"{:,}".format(profile['rating_position'])}""",
                                        )

                                        # Прокачивает раба
                                        if upgrade_slaves == 1:
                                            upgrade_slave(slave_id)

                                        # Покупает оковы только что купленному рабу
                                        if buy_fetters == 1:
                                            if (
                                                fetter_price
                                                <= max_fetter_price
                                            ):
                                                buy_fetter(slave_id)
                                                print(
                                                    f"Купил оковы id{slave_id} за {fetter_price}",
                                                )
                                        sleep(uniform(min_delay, max_delay))
        except Exception as e:
            print(e.args)
            sleep(uniform(min_delay, max_delay))


def buy_slaves():
    """Покупает и улучшает рабов, надевает оковы, если включено в config.py."""
    while True:
        try:
            # Случайный раб в промежутке
            slave_id = randint(1, 647360748)
            slave_info = get_user(slave_id)

            # Проверка раба на соотвествие настройкам цены
            while (
                slave_info["price"] > max_price
                or slave_info["price"] < min_price
            ):
                slave_id = randint(1, 647360748)
                slave_info = get_user(slave_id)

            # Узнаем заранее цену на оковы,
            # чтобы в будущем моментально их купить
            fetter_price = get_user(slave_id)["fetter_price"]

            # Покупка раба
            profile = get_buy_slave(slave_id)

            if "balance" in profile.keys():
                print(
                    f"""[{strftime("%H:%M:%S")}]
Купил id{slave_info["id"]} за {slave_info["price"]}
Баланс: {"{:,}".format(profile['balance'])}
Рабов: {"{:,}".format(profile['slaves_count'])}
Доход в минуту: {"{:,}".format(profile['slaves_profit_per_min'])}
Место в топе дохода: {"{:,}".format(profile['rating_position'])}""",
                )

                # Прокачивает раба
                if upgrade_slaves == 1:
                    upgrade_slave(slave_id)

                # Покупает оковы только что купленному рабу
                if buy_fetters == 1:
                    if fetter_price <= max_fetter_price:
                        buy_fetter(slave_id)
                        print(f"Купил оковы id{slave_id} за {fetter_price}")
                sleep(uniform(min_delay, max_delay))
        except Exception as e:
            print(e.args)
            sleep(uniform(min_delay, max_delay))


def buy_slaves_from_ids():
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
                                if (
                                    slave_info["price"] <= max_price
                                    and slave_info["price"] >= min_price
                                ):

                                    # Узнаем заранее цену на оковы,
                                    # чтобы в будущем моментально их купить
                                    fetter_price = get_user(slave_id)[
                                        "fetter_price"
                                    ]

                                    # Покупка раба
                                    profile = get_buy_slave(slave_id)

                                    print(
                                        f"""[{strftime("%H:%M:%S")}]
Купил id{slave_info["id"]} за {slave_info["price"]} у id{id}
Баланс: {"{:,}".format(profile['balance'])}
Рабов: {"{:,}".format(profile['slaves_count'])}
Доход в минуту: {"{:,}".format(profile['slaves_profit_per_min'])}
Место в топе дохода: {"{:,}".format(profile['rating_position'])}""",
                                    )

                                    # Прокачивает раба
                                    if upgrade_slaves == 1:
                                        upgrade_slave(slave_id)

                                    # Покупает оковы только что купленному рабу
                                    if buy_fetters == 1:
                                        if fetter_price <= max_fetter_price:
                                            buy_fetter(slave_id)
                                            print(
                                                f"Купил оковы id{slave_id} за {fetter_price}",
                                            )
                                    sleep(uniform(min_delay, max_delay))
        except Exception as e:
            print(e.args)
            sleep(uniform(min_delay, max_delay))


def set_fetters():
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
                                f"Купил оковы id{slave['id']} за {slave['fetter_price']}",
                            )
                            sleep(uniform(min_delay, max_delay))
        except Exception as e:
            print(e.args)
            sleep(uniform(min_delay, max_delay))


def job_slaves():
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
        except Exception as e:
            print(e.args)
            sleep(uniform(min_delay, max_delay))


if __name__ == "__main__":
    print(
        """vk.com/free_slaves_bot
github.com/monosans/vk-slaves-bot
Версия 4.0""",
    )
    headers = {
        "Content-Type": "application/json",
        "authorization": authorization,
        "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.51 Safari/537.36",
        "origin": "https://prod-app7794757-c1ffb3285f12.pages-ac.vk-apps.com",
    }
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
