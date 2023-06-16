import asyncio
import aiohttp
from decorators import time_measure, timer
import os

async def download_cat_timer(session, img_url, i:int):
    response = await session.get(img_url)
    img_bytes = await response.read()
    #print(img_url)
    format = img_url[-3:]
    if not os.path.exists("Коты"):
        os.makedirs("Коты")
    file = open(f"Коты/cat{i+1}.{format}", 'wb')
    file.write(img_bytes)
    file.close()
    #print(f"cat{i}.{format}")

async def requests_timer():
    link = "https://api.thecatapi.com/v1/images/search?limit=10"

    session = aiohttp.ClientSession()
    response = await session.get(link)
    answer = await response.json()

    tasks = []
    for i in range(1, 11):
        img_url = answer[i-1]["url"]
        tasks.append(download_cat_timer(session, img_url, i))
    await asyncio.gather(*tasks)
    await session.close()

# @time_measure
def main_timer():
    asyncio.run(requests_timer())

main_timer()
