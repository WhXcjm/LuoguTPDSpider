from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium import webdriver
from pathlib import Path
from html import unescape
import warnings
import requests
import msvcrt
import queue
import time
import json
import sys
import re
import os
CookiesFile=Path(r'.\log\cookies.txt')
browser = webdriver.Chrome()
browser.set_script_timeout(5)
browser.set_page_load_timeout(5)
browser.get('https://www.luogu.com.cn')
browser.delete_all_cookies()
with open(CookiesFile, 'r') as f:
	# 使用json读取cookies 注意读取的是文件 所以用load而不是loads
	cookies_list = json.load(f)
	for cookie in cookies_list:
		browser.add_cookie(cookie)
# ---------------
browser.refresh()
try:
	browser.get('https://www.luogu.com.cn/problem/T29952',timeout=5)
except WebDriverException as e:
	print(e)
	print(browser.page_source)
input()