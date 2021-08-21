#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from random import choice, randint, uniform
from sys import stderr
from threading import Thread
from time import sleep, time

from loguru import logger

from api import Slaves
from config import (
    AUTHORIZATION,
    BUY_FETTERS,
    BUY_FROM_IDS,
    BUY_IDS,
    BUY_SLAVES_MODE,
    JOBS,
    MAX_DELAY,
    MAX_FETTER_PRICE,
    MAX_PRICE,
    MIN_DELAY,
    MIN_PRICE,
    TOP_EXCLUDE,
    UPGRADE_LIMIT,
    UPGRADE_SLAVES,
    USER_AGENT,
)


def sleep_delay() -> None:
    sleep(uniform(MIN_DELAY, MAX_DELAY))


def get_start() -> dict:
    """Получение start при запуске бота."""
    start = client.start()
    if start:
        return start
    sleep_delay()
    return get_start()


def do_start() -> None:
    """Получение start во время работы бота."""
    global start
    while True:
        start = get_start()
        sleep_delay()


def upgrade_slave(slave_id: int, price: int) -> None:
    """Прокачка заданного раба."""
    sleep_delay()
    while price <= UPGRADE_LIMIT:
        if client.sale_slave(slave_id):
            logger.info(f"Продал id{slave_id}")
        if client.buy_slave(slave_id):
            logger.info(f"Улучшил id{slave_id}")
        slave = client.user(slave_id)
        while not slave:
            sleep_delay()
            slave = client.user(slave_id)
        price = slave["price"]


def buy_target_slaves(target_id: int) -> None:
    """Перекупка рабов у target_id при BUY_SLAVES_MODE = 2 или 3."""
    have_bought = False
    slave_list = client.slave_list(target_id)
    if slave_list:
        for slave in slave_list["slaves"]:
            slave_price = slave["price"]
            if (
                slave["fetter_to"] < time()
                and MIN_PRICE <= slave_price <= MAX_PRICE
            ):
                buy_slave_fetter_upgrade(slave["id"], slave_price, target_id)
                have_bought = True
                sleep_delay()
    if not have_bought:
        sleep_delay()


def slaves_upgrade() -> None:
    """Прокачка имеющихся рабов при BUY_SLAVES_MODE = 0 и UPGRADE_SLAVES = 1."""
    while True:
        slaves = start["slaves"]
        for slave in slaves:
            if slave["fetter_to"] < time():
                upgrade_slave(slave["id"], slave["price"])


def buy_slave_fetter_upgrade(
    slave_id: int, price: int, target_id: int = None
) -> None:
    """Покупка, закование и прокачка раба."""
    buy_slave = client.buy_slave(slave_id)
    if buy_slave:
        logger.info(
            f"""
Купил id{slave_id} за {price}{f' у id{target_id}' if target_id else ''}
Баланс: {buy_slave['balance']}
Рабов: {buy_slave['slaves_count']}
Доход в минуту: {buy_slave['slaves_profit_per_min']}"""
        )
        if UPGRADE_SLAVES == 1:
            upgrade_slave(slave_id, buy_slave["price"])
        if BUY_FETTERS == 1 and client.buy_fetter(slave_id):
            logger.info(f"Заковал id{slave_id}")


def buy_random_slaves() -> None:
    """Покупка случайных рабов при BUY_SLAVES_MODE = 1."""
    while True:
        user = client.user(randint(1, 670000000))
        if user:
            user_id = user["id"]
            price = user["price"]
            while (
                price < MIN_PRICE
                or price > MAX_PRICE
                or user["fetter_to"] > time()
            ):
                logger.info(f"Найден раб за {price}. Ищу нового.")
                sleep_delay()
                tmp_user = client.user(randint(1, 670000000))
                if tmp_user:
                    user_id = tmp_user["id"]
                    price = tmp_user["price"]
            buy_slave_fetter_upgrade(user_id, price)
        sleep_delay()


def buy_top_users_slaves() -> None:
    """Перекупка рабов у топеров при BUY_SLAVES_MODE = 2."""
    TOP_EXCLUDE.append(start["me"]["id"])
    while True:
        top_users = client.top_users()
        if top_users:
            for top_user in top_users["list"]:
                user_id = top_user["id"]
                if user_id not in TOP_EXCLUDE:
                    buy_target_slaves(user_id)
        else:
            sleep_delay()


def buy_slaves_from_ids() -> None:
    """Перекупка рабов у BUY_FROM_IDS при BUY_SLAVES_MODE = 3."""
    while True:
        for user_id in BUY_FROM_IDS:
            buy_target_slaves(user_id)


def hunt_ids() -> None:
    """Покупка и удерживание BUY_IDS при BUY_SLAVES_MODE = 4."""
    my_id = start["me"]["id"]
    while True:
        for user_id in BUY_IDS:
            user = client.user(user_id)
            if user and user["fetter_to"] < time():
                price = user["price"]
                if user["master_id"] == my_id:
                    if BUY_FETTERS == 1 and client.buy_fetter(user_id):
                        logger.info(f"Заковал id{user_id}")
                elif MIN_PRICE <= price <= MAX_PRICE:
                    buy_slave_fetter_upgrade(user_id, price)
            sleep_delay()


def fetter_slaves() -> None:
    """Покупка оков имеющимся рабам при BUY_SLAVES_MODE = 0 и BUY_FETTERS = 1."""
    while True:
        slaves = start["slaves"]
        for slave in slaves:
            fetter_price = slave["fetter_price"]
            if (
                slave["fetter_to"] < time()
                and fetter_price <= MAX_FETTER_PRICE
            ):
                slave_id = slave["id"]
                if client.buy_fetter(slave_id):
                    logger.info(f"Заковал id{slave_id} за {fetter_price}")
                sleep_delay()


def job_slaves() -> None:
    """Выдача работы рабам."""
    while True:
        slaves = start["slaves"]
        for slave in slaves:
            if not slave["job"]["name"]:
                slave_id = slave["id"]
                if client.job_slave(slave_id, choice(JOBS)):
                    logger.info(f"Дал работу id{slave_id}")
                sleep_delay()


if __name__ == "__main__":
    logger.remove()
    logger.add(
        stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{message}</level>",
        colorize=True,
    )
    client = Slaves(
        AUTHORIZATION.strip(), USER_AGENT.strip(), MIN_DELAY, MAX_DELAY
    )
    start = get_start()
    if BUY_SLAVES_MODE == 0:
        if UPGRADE_SLAVES == 1:
            Thread(target=slaves_upgrade).start()
        if BUY_FETTERS == 1:
            Thread(target=fetter_slaves).start()
    elif BUY_SLAVES_MODE == 1:
        Thread(target=buy_random_slaves).start()
    elif BUY_SLAVES_MODE == 2:
        Thread(target=buy_top_users_slaves).start()
    elif BUY_SLAVES_MODE == 3:
        Thread(target=buy_slaves_from_ids).start()
    elif BUY_SLAVES_MODE == 4:
        Thread(target=hunt_ids).start()
    Thread(target=job_slaves).start()
    sleep_delay()
    Thread(target=do_start).start()
