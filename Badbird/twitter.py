import asyncio
import aiohttp
import re
#Load up the usernames.txt file with usernames you want to check.
async def check_username_availability(username):
    async with aiohttp.ClientSession() as session:
        headers = {
            "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
            "x-guest-token": "1541486022587998209"
        }
        async with session.get(f"https://twitter.com/i/api/i/users/username_available.json?username={username}", headers=headers) as resp:
            return await resp.text()

async def check_batch(usernames):
    # create tasks for checking the availability of each username
    tasks = []
    for username in usernames:
        tasks.append(asyncio.create_task(check_username_availability(username)))
    # wait for tasks to complete
    results = await asyncio.gather(*tasks)
    available_usernames = []
    for result in results:
        # check if username is available
        if re.search(r'"valid":true', result):
            print(f'\033[92m[AVAILABLE] {username}\033[0m')  # print in green
            available_usernames.append(username)
        else:
            print(f'\033[91m[UNAVAILABLE] {username}\033[0m')  # print in red
    # save available usernames to file
    with open('available_usernames.txt', 'a') as f:  # append to file
        for username in available_usernames:
            f.write(username + '\n')

async def main():
    with open('usernames.txt') as f:
        usernames = f.read().splitlines()
    # check usernames in batches of 10
    for i in range(0, len(usernames), 10):
        await check_batch(usernames[i:i+1])

asyncio.run(main())
