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
        responses = await asyncio.gather(*(task['response'] for task in tasks), return_exceptions=True)

        for task, response in zip(tasks, responses):
            if isinstance(response, Exception) or response.status not in {200, 401}:
                client.chat_postMessage(
                    channel=SLACK_CHANNEL, text=f'{task["name"]} is down')


loop = asyncio.get_event_loop()
loop.run_until_complete(check_apps_status())