import asyncio
import aiohttp
import aiofiles

link = 'https://elements-cover-images-0.imgix.net/f223ce8d-5a80-4e09-9bbc-c809e4c76b76?auto=compress%2Cformat&fit=max&w=433&s=30397a9afa9b31cd51efb9130e5c1705 433w, https://elements-cover-images-0.imgix.net/f223ce8d-5a80-4e09-9bbc-c809e4c76b76?auto=compress%2Cformat&fit=max&w=632&s=650904d6e65dd5dcb6c54e5a98ac6fa7 632w, https://elements-cover-images-0.imgix.net/f223ce8d-5a80-4e09-9bbc-c809e4c76b76?auto=compress%2Cformat&fit=max&w=710&s=922dc5c574a4b37e468e1d353a107019 710w, https://elements-cover-images-0.imgix.net/f223ce8d-5a80-4e09-9bbc-c809e4c76b76?auto=compress%2Cformat&fit=max&w=866&s=43777e39df2446220a9fdc90a19c9350 833w, https://elements-cover-images-0.imgix.net/f223ce8d-5a80-4e09-9bbc-c809e4c76b76?auto=compress%2Cformat&fit=max&w=900&s=8da385c63e3a9af9d53d7022576c15f0 900w, https://elements-cover-images-0.imgix.net/f223ce8d-5a80-4e09-9bbc-c809e4c76b76?auto=compress%2Cformat&fit=max&w=1019&s=710308d6a4ee537e2adb6d946d224511 1019w, https://elements-cover-images-0.imgix.net/f223ce8d-5a80-4e09-9bbc-c809e4c76b76?auto=compress%2Cformat&fit=max&w=1170&s=7ba1f40849a995ff2852a781be1df0cb 1170w, https://elements-cover-images-0.imgix.net/f223ce8d-5a80-4e09-9bbc-c809e4c76b76?auto=compress%2Cformat&fit=max&w=1370&s=87c6b26e0008eb702a2ae137ce7d5da2 1370w, https://elements-cover-images-0.imgix.net/f223ce8d-5a80-4e09-9bbc-c809e4c76b76?auto=compress%2Cformat&fit=max&w=2038&s=b2672cdcf603100fc82fcef160531a8e 2038w'

vague_links = link.split(' ')
links = filter(lambda x: 'https' in x, vague_links)

async def download_image(session, url):
    file_path = "images/" + url[-5:] + ".jpg"
    try:
        async with session.get(url) as response:
            response = await response.content.read()
            f = await aiofiles.open(file_path, mode='wb')
            await f.write(response)
            await f.close()
            print('success!!!')
    except Exception as e:
        print(e)
        print('Could not download image')


async def download_all_images(urls):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.ensure_future(download_image(session, url))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(download_all_images(links))