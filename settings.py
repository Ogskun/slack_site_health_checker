import os
from dotenv import load_dotenv

load_dotenv()

SLACK_TOKEN = os.environ.get('SLACK_TOKEN')
SLACK_CHANNEL = os.environ.get('SLACK_CHANNEL')

APPS = [{
    # 'name': '',
    # 'url': '',
}]

try:
    from .localsettings import *
except:
    pass