# python3
# -*- coding: utf-8 -*-
# @Time    : 2022/12/3 22:25
# @Author  : yzyyz
# @Email   :  youzyyz1384@qq.com
# @File    : source_data.py
# @Software: PyCharm
from typing import Optional

import httpx

url = 'https://novelai.8zyw.cn/ajax.php?act=generate'


async def ask_url(dec: str, model: int = 1, seed: str = None) -> Optional[dict]:
    data = {'desc': dec,
            'uc': 'bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, jpeg artifacts, signature, watermark, username, blurry, bad feet ,nude,fuck,pussy,make love,ml,porn,sex,sexy',
            'exclude': 'none', 'resolution': 'NORMALPortrait', 'model': 'nai-diffusion', 'sampler': 'k_euler_ancestral',
            'steps': '28', 'scale': '11', 'qualityToggle': 'on', 'seed': '', 'type': 'text', 'file': '',
            'strength': '0.7', 'noise': '0.2', 'share': 'on', 'apikey': ''}
    if model == 2:
        data['model'] = "safe-diffusion"
    if seed:
        data['seed'] = seed
    async with httpx.AsyncClient() as client:
        try:
            res = await client.post(url=url, data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
            if res.status_code == 200:
                return res.json()
            else:
                return None
        except Exception:
            return None
