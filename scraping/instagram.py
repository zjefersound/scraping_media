# instagram.py
import datetime
import json
from typing import Union, Literal

from logs import setup_logger
from utils import tools
from .base import BaseScrape

from playwright.sync_api import sync_playwright, Playwright

logger = setup_logger(__name__)
SETTINGS = tools.read_settings()

class Instagram(BaseScrape):
    pass
