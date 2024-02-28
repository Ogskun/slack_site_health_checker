import aiohttp
import asyncio
import slack

from settings import (
    APPS,
    SLACK_CHANNEL,
    SLACK_TOKEN,
)

client = slack.WebClient(token=SLACK_TOKEN)


async def check_site_urls(session):
    apps = []

    for site in APPS:
        try:
            apps.append({
                'response': session.get(site['url']), 
                'name': site['name']
            })
        except Exception as e:
            raise e

    return apps

async def check_apps_status():
    async with aiohttp.ClientSession() as session:

        tasks = await check_site_urls(session)

        coroutines = [coroutine['response'] for coroutine in tasks]
        
        responses = await asyncio.gather(*coroutines, return_exceptions=True)
        
        for index, value in enumerate(responses):
            message = f'{tasks[index]["name"]} is down'

            if isinstance(value, Exception):
                client.chat_postMessage(channel=SLACK_CHANNEL, text=message)
                continue

            if value.status == 401:
                # Ignore checking if site has HT password
                continue
            
            if value.status != 200:
                client.chat_postMessage(channel=SLACK_CHANNEL, text=message)


loop = asyncio.get_event_loop()
loop.run_until_complete(check_apps_status())