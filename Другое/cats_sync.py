from __future__ import annotations
import os
import requests
from decorators import time_measure
import asyncio

a = "https://api.thecatapi.com/v1/images/search?limit=10"
dct = requests.get(a).json()

@time_measure
def cats_download_sync():
    for i in range(1, len(dct) + 1):
        s = dct[i - 1]["url"]
        # print(s)
        image_url = s
        image = requests.get(s).content
        format = image_url[-3:]
        # print(format)
        if not os.path.exists("Коты"):
            os.makedirs("Коты")
        with open(f'Коты//cat{i}.{format}', 'wb') as file:
            file.write(image)

cats_download_sync()


