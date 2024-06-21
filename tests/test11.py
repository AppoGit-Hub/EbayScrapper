import asyncio
import aiohttp
import bs4
import time

async def fetch(url: str, session: aiohttp.ClientSession):
    async with session.get(url) as response:
        return url, await response.text()

async def single(url: str):
    async with aiohttp.ClientSession() as session:
        return await fetch(url, session)

async def batch(urls: list[str]):
    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(*[fetch(url, session) for url in urls])

start_time = time.perf_counter()
print("Gather")
urls = ["https://www.instagram.com/".format(page=index) for index in range(1, 10)]
print("Transform")
if False:
    soups = [(url, bs4.BeautifulSoup(response, "html.parser")) for url, response in asyncio.run(batch(urls))]
    for index, (url, soup) in enumerate(soups):
        pass
else:
    for url, response in asyncio.run(batch(urls)):
        soup = bs4.BeautifulSoup(response, "html.parser")
        pass

print("Process")
end_time = time.perf_counter()
print(end_time - start_time)

start_time = time.perf_counter()
asyncio.run(single("https://www.instagram.com/"))
end_time = time.perf_counter()
print(f"Single resquest: {end_time - start_time}")
