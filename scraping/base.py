# base.py
from datetime import datetime, timezone
import json
import os
import time
import urllib.request
import base64
from typing import Literal, Union
from abc import ABC
from uuid import uuid4
from copy import deepcopy
from PIL import Image

from utils import tools
from logs import setup_logger

logger = setup_logger(__name__)
SETTINGS = tools.read_settings()


class ImgHandler:
    def __init__(self):
        self.imgs = []
    
    # def get2(self, img_url: str, name: str | None = None):
    #     if not name:
    #         name = uuid4().hex
        
    #     with urllib.request.urlopen(img_url) as img_response:
    #         img_data = img_response.read()
        
    #     img_base64 = base64.b64encode(img_data).decode('utf-8')
    #     self.imgs.append({'img': img_base64, 'name': name})
    #     return img_base64
    
    def get(self, img_url: str, name: str | None = None):
        if not name:
            name = uuid4().hex
        
        with urllib.request.urlopen(img_url) as img_response:
            img_data = img_response.read()
        
        ext = '.mp4' if '.mp4' in img_url else '.jpeg'
        filename = name + ext

        # Only convert images to base64
        if ext != '.mp4':
            img_base64 = base64.b64encode(img_data).decode('utf-8')
            self.imgs.append({'img': img_base64, 'name': name})
            return img_base64
        
        return filename


    def save(self, root: str):
        if not self.imgs:
            return None
        
        for img in self.imgs:
            image_data = base64.b64decode(img['img'])
            filename = os.path.join(root, img['name'] + ".jpeg")
            with open(filename, "wb") as file:
                file.write(image_data) 
            print(f"img save in {filename}")
            # ---- Crop/resize to vertical ----
            try:
                with Image.open(filename) as im:
                    w, h = im.size
                    if w > h:  # landscape → crop to vertical (center)
                        new_w = int(h * 9 / 16)  # keep 9:16 ratio
                        left = (w - new_w) // 2
                        right = left + new_w
                        im = im.crop((left, 0, right, h))
                    elif w < h:  # portrait → crop top-bottom if needed
                        new_h = int(w * 16 / 9)
                        top = (h - new_h) // 2
                        bottom = top + new_h
                        im = im.crop((0, top, w, bottom))

                    # Overwrite original file
                    im.save(filename, "JPEG")
                    print(f"img cropped & replaced in {filename}")
            except Exception as e:
                print(f"Skipping crop for {filename}: {e}")

class BaseScrape(ABC):
    
    def __init__(self):
        super().__init__()
        self.img_handler = ImgHandler()
        self.raw_data = None
        self.clean_data = None
        self.bs64_data = None
    
    def struct_profile(self, profile: dict):
        raise NotImplementedError("Must implement in children class")

    def struct_post(self, post: dict):
        raise NotImplementedError("Must implement in children class")

    def _clean(self, raw_data):
        raise NotImplementedError("Must implement in children class")
    
    def _convert_bs64(self, clean_data: dict):
        time_s = SETTINGS.get('gral', {}).get('img_scrape_sleep_s', 2)
        data = deepcopy(clean_data)
        profile = data.get('profile', {})
        posts = data.get('posts', [])
        
        if profile.get('img'):
            try:
                img64 = self.img_handler.get(profile['img'], name='profile_img')
                profile['img'] = img64
            except Exception as e:
                logger.error(f'Img cant be scraped to bs64 - url: {profile["img"]}, error: {e}')
                pass
        
        post_notna = [post for post in posts if post.get('img')]
        total = len(post_notna)
        # max_posts = 10
        # total = min(len(post_notna), max_posts)
        i = 1
        for _, post in enumerate(posts):
            if not post.get('img'):
                continue
            
            try:
                img64 = self.img_handler.get(post['img'], name=post['id'])    
            except Exception as e:
                logger.error(f'Img cant be scraped to bs64 - url: {post["img"]}, error: {e}')
                img64 = None
            
            time.sleep(time_s)
            
            posts[_]['img'] = img64
            print(f'{i} / {total} posts img scraped')
            i += 1
            
        return {
            'profile': profile,
            'posts': posts
        }

    def _type(self, type: Literal['raw', 'clean', 'bs64'] = 'raw'):
        if type == 'raw':
            return self.raw_data
        
        elif type == 'clean':
            self.clean_data = self._clean(self.raw_data)
            return self.clean_data
        
        elif type == 'bs64':
            self.clean_data = self._clean(self.raw_data)
            self.bs64_data = self._convert_bs64(self.clean_data)
            return self.bs64_data

        else:
            return None

    def _save(self, dir_name: str):
        root = tools.make_dir(dir_name)
        tools.save_dict(self.raw_data, 'raw', root, stamp=False)
        tools.save_dict(self.clean_data, 'clean', root, stamp=False)
        tools.save_dict(self.bs64_data, 'bs64', root, stamp=False)
        self.img_handler.save(root=root)

class RequestsHandler:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def make_request(self, endpoint: str, params: dict = None, headers: dict = None) -> dict:
        """
        Makes a GET request to the specified endpoint with optional query parameters and headers using urllib.
        
        The method automatically handles common exceptions like HTTP errors, timeouts, 
        and too many redirects, logging the appropriate error message if any issue arises.
        
        :param endpoint: The API endpoint to which the request will be made (e.g., "/data").
        :param params: Optional dictionary of query parameters to include in the request.
        :param headers: Optional dictionary of HTTP headers to include in the request.
        
        :return: A dictionary containing the JSON response from the server, or an empty dictionary 
                 if an error occurred or no valid response was received.
        """
        params = params or {}
        headers = headers or {}
        url = f"{self.base_url}{endpoint}"
        
        if params:
            query_string = urllib.parse.urlencode(params)
            url = f"{url}?{query_string}"

        logger.info(f'RequestsHandler - Making GET request to "{url}"')

        try:
            req = urllib.request.Request(url, headers=headers)

            with urllib.request.urlopen(req) as response:
                response_data = response.read().decode('utf-8')
                return json.loads(response_data)

        except urllib.error.HTTPError as e:
            logger.error(f'RequestsHandler - HTTPError - URL: {url}, Status Code: {e.code}, Response: {e.read().decode()}')
        except urllib.error.URLError as e:
            logger.error(f'RequestsHandler - URLError - URL: {url}, Error: {e.reason}')
        except urllib.error.TimeoutError as e:
            logger.error(f'RequestsHandler - TimeoutError - URL: {url}, Error: {e}')
        except Exception as e:
            logger.error(f'RequestsHandler - Unexpected error: {e}')

        return {}
