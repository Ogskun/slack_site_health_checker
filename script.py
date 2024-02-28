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
    return [{'response': session.get(site['url']), 'name': site['name']} for site in APPS]


async def check_apps_status():
    async with aiohttp.ClientSession() as session:
        tasks = await check_site_urls(session)

        coroutines = [coroutine['response'] for coroutine in tasks]

        responses = await asyncio.gather(*coroutines)

        for index, value in enumerate(responses):

            if value.status == 401:
                # Ignore checking if site has HT password
                continue
            
            if value.status != 200:
                message = f'{tasks[index]["name"]} is down'
                client.chat_postMessage(channel=SLACK_CHANNEL, text=message)


loop = asyncio.get_event_loop()
loop.run_until_complete(check_apps_status())