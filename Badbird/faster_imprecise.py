# This version is a alternative version to twitterr.py, it is much faster at sending requests, but loads files slower and is a bit more imprecise.

import asyncio
import aiohttp
import re

async def check_username_availability(username):
    async with aiohttp.ClientSession() as session:
        headers = {
            "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
            "x-guest-token": "1541486022587998209"
        }
        async with session.get(f"https://twitter.com/i/api/i/users/username_available.json?username={username}", headers=headers) as resp:
            return username, await resp.text()

async def check_usernames(usernames):
    tasks = []
    for username in usernames:
        tasks.append(asyncio.create_task(check_username_availability(username)))
    results = await asyncio.gather(*tasks)
    available_usernames = []
    for username, result in results:
        if re.search(r'"valid":true', result):
            print(f'\033[92m[AVAILABLE] {username}\033[0m')
            available_usernames.append(username)
        else:
            print(f'\033[91m[UNAVAILABLE] {username}\033[0m')
    with open('available_usernames.txt', 'a') as f:
        for username in available_usernames:
            f.write(username + '\n')

async def main():
    with open('usernames.txt') as f:
        usernames = f.read().splitlines()
    await check_usernames(usernames)

asyncio.run(main())
