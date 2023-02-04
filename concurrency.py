import requests
import time
import concurrent.futures
import threading
import asyncio
import aiohttp

# using just requests took 49 seconds while session took 21 seconds
# using threading with sessions can take as low as 2 seconds

# requests and sessions without concurrency
"""
def download_site(url, session):
    with session.get(url) as response:
        print(f"Read {len(response.content)} from {url}")

def download_all_sites(sites):
    with requests.Session() as session:
        for url in sites:
            download_site(url, session)
"""

# requests without sessions, without concurrency
"""
def download_site(url):
    response =  requests.get(url)
    print(f"Read {len(response.content)} from {url}")

def download_all_sites(sites):
    for url in sites:
        download_site(url)
"""


# threading
#"""
thread_local = threading.local()

def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def download_site(url):
    session = get_session()
    with session.get(url) as response:
        print(f"Read {len(response.content)} from {url}")


def download_all_sites(sites):
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        executor.map(download_site, sites)
#"""

# asyncio
"""
async def download_site(session, url):
    async with session.get(url) as response:
        print("Read {0} from {1}".format(response.content_length, url))

async def download_all_sites(urls):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.ensure_future(download_site(session, url))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)
"""

if __name__ == "__main__":
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 40
    start_time = time.time()
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # asyncio.run(download_all_sites(sites))
    download_all_sites(sites)
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} in {duration} seconds")