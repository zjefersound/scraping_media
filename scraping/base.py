# base.py
from datetime import datetime, timezone
import os
import urllib.request
import base64
from typing import Literal, Union
from abc import ABC
from uuid import uuid4
from copy import deepcopy

from utils import tools
from logs import setup_logger

logger = setup_logger(__name__)
SETTINGS = tools.read_settings()


class ImgHandler:
    imgs = []
    
    def get(self, img_url: str, name: str | None = None):
        if not name:
            name = uuid4().hex
        
        with urllib.request.urlopen(img_url) as img_response:
            img_data = img_response.read()
        
        img_base64 = base64.b64encode(img_data).decode('utf-8')
        self.imgs.append({'img': img_base64, 'name': name})
        return img_base64

    def save(self, root: str):
        if not self.imgs:
            return None
        
        for img in self.imgs:
            image_data = base64.b64decode(img['img'])
            filename = os.path.join(root, img['name'] + ".jpeg")
            with open(filename, "wb") as file:
                file.write(image_data) 
            print(f"img save in {filename}")

class BaseScrape(ABC):
    img_handler = ImgHandler()
    raw_data = None
    clean_data = None
    bs64_data = None
    
    def struct_profile(profile: dict):
        raise NotImplementedError("Must implement in children class")

    def struct_post(profile: dict):
        raise NotImplementedError("Must implement in children class")

    def _clean(raw_data):
        raise NotImplementedError("Must implement in children class")
    
    def _convert_bs64(self, clean_data: dict):
        data = deepcopy(clean_data)
        profile = data.get('profile', {})
        posts = data.get('posts', [])
        
        if profile.get('img'):
            try:
                img64 = self.img_handler.get(profile['img'], name='profile_img')
                profile['img'] = img64
            except Exception as e:
                logger.error(f'Img cant be scraped to bs64 - url: {profile['img']}, error: {e}')
                pass
        
        post_notna = [post for post in posts if post.get('img')]
        total = len(post_notna)
        i = 1
        for _, post in enumerate(posts):
            if not post.get('img'):
                continue
            
            try:
                img64 = self.img_handler.get(post['img'], name=post['id'])    
            except Exception as e:
                logger.error(f'Img cant be scraped to bs64 - url: {post['img']}, error: {e}')
                img64 = None
            
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
