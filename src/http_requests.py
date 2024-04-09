# src/scraper.py
import requests
from bs4 import BeautifulSoup

def http_requests(url):
    # 发送HTTP请求并返回响应对象
    headers = {
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
        'DNT': '1',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
        'sec-ch-ua-platform': '"Windows"',
    }
    response = requests.get(url, headers=headers)
    return response
