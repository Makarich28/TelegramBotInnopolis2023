import asyncio


async def count(name: str, n: int):
    for i in range(n, -1, -1):
        print(name, i)
        await asyncio.sleep(1)


async def main():
    await asyncio.gather(count("Таймер_1:", 10), count("Таймер_2:", 5), count("Таймер_3:", 7))


asyncio.run(main())

