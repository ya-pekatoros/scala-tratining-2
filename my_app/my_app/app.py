#! /usr/bin/env python3
import asyncio

from sender import perform_operation


async def main():
    identifier: str = input("Введите номер заявки: ")
    # Инициализация asyncio loop
    loop = asyncio.get_event_loop()
    # Запуск асинхронной операции

    loop.run_until_complete(perform_operation())

if __name__ == "__main__":
    asyncio.run(main())
