import asyncio
from copy import deepcopy
from enum import Enum
from typing import List
from datetime import timedelta
from dataclasses import dataclass

timeout_seconds = timedelta(seconds=15).total_seconds()


@dataclass
class Payload:
    json_sting: str


@dataclass
class Address:
    email: str


@dataclass
class Event:
    recipients: List[Address]
    payload: Payload


class Result(Enum):
    Accepted = 1
    Rejected = 2


def read_data() -> Event:
    # Метод для чтения порции данных
    pass


async def send_data(dest: Address, payload: Payload) -> Result:
    # Метод для рассылки данных
    pass


async def wait_and_send_data(dest: Address, payload: Payload) -> Result:
    await asyncio.sleep(timeout_seconds)
    # Метод для рассылки данных
    return await send_data(dest, payload)

async def perform_operation() -> None:
    send_tasks = []
    # получение цикла событий
    loop = asyncio.get_running_loop()
    # выполнение функции в отдельном потоке
    data_task = None
    while True:
        if data_task:
            if data_task.done():
                try:
                    data: Event = data_task.result()
                    data_task = loop.run_in_executor(None, read_data())
                    for dest in data.recipients:
                        send_tasks.append(
                            (
                                loop.run_in_executor(None, send_data(dest=dest, payload=data.payload)),
                                dest,
                                data.payload,
                            )
                        )
                    for task in deepcopy(send_tasks):
                        if task.done():
                            try:
                                result = task[0].result()
                                if result == Result.Rejected:
                                    send_tasks.append(
                                        loop.run_in_executor(None, wait_and_send_data(dest=dest, payload=data.payload)),
                                        dest,
                                        data.payload,
                                    )
                                elif result == Result.Accepted:
                                    print(f'Ok send for: {task[1]}, data: {task[2]}')
                                else:
                                    print(f'Error send for: {task[1]}, data: {task[2]}')
                            except Exception:
                                print(f'Error send for: {task[1]}, data: {task[2]}')
                            send_tasks.remove(task)

                except Exception:
                    data_task = None
        else:
            data_task = loop.run_in_executor(None, read_data())

# Запуск асинхронного кода
asyncio.run(perform_operation())
