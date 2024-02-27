import asyncio
import aiohttp
import slack

from settings import (
    APPS,
    SLACK_CHANNEL,
    SLACK_TOKEN,
)

client = slack.WebClient(token=SLACK_TOKEN)


def check_site_urls(session):
    return [session.get(site['url']) for site in APPS]


async def check_apps_status():
    async with aiohttp.ClientSession() as session:
        tasks = check_site_urls(session)

        responses = await asyncio.gather(*tasks)

        for response in responses:
            if response.status == 401:
                # Ignore checking if site has HT password
                continue

            if response.status != 200:
                message = f'{response.url} is down'
                client.chat_postMessage(channel=SLACK_CHANNEL, text=message)


loop = asyncio.get_event_loop()
loop.run_until_complete(check_apps_status())