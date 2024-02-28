from flask import Flask
import json

app = Flask('__main__', template_folder= 'templates', static_folder = 'static')
sysConfig = None

with open ('config.json', encoding = 'UTF-8') as config:
    sysConfig = json.load(config)

from services import lineBotService
from services import memberService
from services import linepayService