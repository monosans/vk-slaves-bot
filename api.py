# -*- coding: utf-8 -*-
from random import uniform
from time import sleep

from loguru import logger
from requests import Session


class Slaves:
    def __init__(
        self,
        authorization: str,
        user_agent: str,
        min_delay: float = 6,
        max_delay: float = 8,
    ) -> None:
        """
        authorization (str): vk_access_token_settings...
        user_agent (str): User agent браузера.
        min_delay (float): Мин. задержка между одинаковыми запросами в
            секундах.
        max_delay (float): Макс. задержка между одинаковыми запросами в
            секундах.
        """
        self._s = Session()
        self._s.headers.update(
            {
                "authorization": authorization,
                "origin": "https://prod-app7794757-c1ffb3285f12.pages-ac.vk-apps.com",
                "referer": f"https://prod-app7794757-c1ffb3285f12.pages-ac.vk-apps.com/index.html?{authorization}",
                "User-agent": user_agent,
            }
        )
        self._MIN_DELAY = min_delay
        self._MAX_DELAY = max_delay

    def buy_fetter(self, slave_id: int) -> dict:
        """Покупка оков указанному раба."""
        return self._req("buyFetter", "balance", {"slave_id": slave_id})

    def buy_slave(self, slave_id: int) -> dict:
        """Покупка указанного раба."""
        return self._req("buySlave", "balance", {"slave_id": slave_id})

    def job_slave(self, slave_id: int, job_name: str) -> dict:
        """Выдача работы указанному рабу."""
        return self._req(
            "jobSlave", "balance", {"slave_id": slave_id, "name": job_name}
        )

    def sale_slave(self, slave_id: int) -> dict:
        """Продажа указанного раба."""
        return self._req("saleSlave", "balance", {"slave_id": slave_id})

    def slave_list(self, user_id: int) -> dict:
        """Получение списка рабов указанного пользователя."""
        return self._req(f"slaveList?id={user_id}", "slaves")

    def start(self) -> dict:
        """Получение полной информации о своём профиле."""
        return self._req("start", "me")

    def top_users(self) -> dict:
        """Получение топа игроков."""
        return self._req("topUsers", "list")

    def user(self, user_id: int) -> dict:
        """Получение информации об указанном пользователе."""
        return self._req(f"user?id={user_id}", "balance")

    def _req(
        self, endpoint: str, key_to_check: str, json: dict = None
    ) -> dict:
        """Метод для отправки запросов серверу игры.

        Args:
            endpoint (str): Конечная точка.
            key_to_check (str): Ключ, наличие которого проверять в ответе
                сервера, чтобы убедиться в правильности ответа.
            json (dict, optional): Данные для отправки в запросе.
                Если равен None (по умолчанию), отправляется GET запрос,
                иначе POST.

        Returns:
            dict: Если key_to_check есть в ответе сервера, возвращает ответ,
                иначе {}.
        """
        try:
            r = self._s.request(
                "GET" if json is None else "POST",
                f"https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0/{endpoint}",
                json=json,
            ).json()
        except Exception as e:
            logger.error(f"{endpoint}: {e}")
            sleep(uniform(self._MIN_DELAY, self._MAX_DELAY))
            return self._req(endpoint, key_to_check, json)
        if key_to_check in r:
            return r
        logger.error(f"{endpoint}: {r}")
        return {}
