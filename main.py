# main.py
from pprint import pprint
from utils import tools
from scraping import *
import json


with open('istaraw.json', 'r', encoding='utf-8') as f:
    raw = json.load(f)

a = Instagram()
a.get('@joerogan', 'bs64')
a._save('dist/joerogan')
