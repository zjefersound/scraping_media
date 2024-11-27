# main.py
from pprint import pprint
from utils import tools
from scraping import *
import json

key = tools.read_settings('env.json').get('apikey')
# with open('istaraw.json', 'r', encoding='utf-8') as f:
#     raw = json.load(f)
# a = Instagram()
# a.get('@joerogan', 'bs64')
# a._save('dist/joerogan')
a = Youtube(api_key=key)
a.get('@joerogan', type='bs64')
a.save()
