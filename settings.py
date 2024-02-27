import os
from dotenv import load_dotenv

load_dotenv()

# Slack app token
SLACK_TOKEN = os.environ.get('SLACK_TOKEN')

# Channel name which is connected to your app
SLACK_CHANNEL = os.environ.get('SLACK_CHANNEL')

# List of site urls
APPS = [{
    # 'name': '',
    # 'url': '',
}]

try:
    from .localsettings import *
except:
    pass