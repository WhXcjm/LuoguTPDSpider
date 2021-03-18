# %%
# All Rights Reserved for WhXcjm
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

warnings.filterwarnings("ignore",category=DeprecationWarning)
Key = int(time.strftime("%Y%m%d"))** 11 * int(time.strftime("%m%Y%d")) % 1000001
inKey = int(input('Please input the key:'))
print("Please wait for 2 seconds")
time.sleep(2)
if (inKey == Key):
	print("Verification succeeded")
else:
	print("Verification failed")
	input()
	exit()
# Preparation
def PR(a):
	sys.stdout.write(a)
	sys.stdout.flush()
teamnumber = input("Enter your team number:")
GroupProblemsPage = 'https://www.luogu.com.cn/team/{}#problem'.format(
	teamnumber)
PagesRe = re.compile("共.*?<strong.*?>.*?(\\d+).*?</strong>.*?页", re.S)
ProblemsSetRe = re.compile(
	"row card-row.*?id\">(.*?)</div.*?href=\".*?\".*?>\\s*(.*?)\\s*?</a>",
	re.S)
DownloadDataRe = re.compile(r'上传数据.*?href="(.*?)".*?target.*?下载数据', re.S)
ProblemCardRe = re.compile('(<div data-v-394f29d4="" data-v-658c888e="" data-v-796309f8="">.*?</div>)[^<]*?</section>[^<]*?</section>', re.S)

try:
	os.mkdir("log")
except OSError as e:
	pass
try:
	os.mkdir("Output")
except OSError as e:
	pass

log = open('.\\log\\log.log', 'a+')

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('log-level=2')
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
try:
	browser = webdriver.Chrome(chrome_options=chrome_options)
except WebDriverException as e:
	print("\nERROR!!!\nProbably you should check your chromedriver")
	print('This website is a choice: http://npm.taobao.org/mirrors/chromedriver/')
	print('Press \'M\' to see details or any other key to exit')
	KKey = str(msvcrt.getch().decode('utf8'))
	if (KKey == 'm' or KKey == 'M'):
		print(e)
	else:
		exit()
	msvcrt.getch()
	exit()

headers = {
	'User-Agent':
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
}
# test
input('Ready?')
# get cookies
# ---------------has run
CookiesFile=Path(r'.\log\cookies.txt')
browser.get(GroupProblemsPage)
if CookiesFile.exists():
	pass
else:
	while (input("Login and then enter \"okk\":") != "okk"):
		pass
	with open(CookiesFile,'w') as f:
		f.write(json.dumps(browser.get_cookies()))
# browser.close()
# ---------------

#%%

# use cookies

# ---------------
browser.get(GroupProblemsPage)
wait = WebDriverWait(browser, 10)
wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'card-header')))
browser.delete_all_cookies()
with open(CookiesFile, 'r') as f:
	# 使用json读取cookies 注意读取的是文件 所以用load而不是loads
	cookies_list = json.load(f)
	for cookie in cookies_list:
		browser.add_cookie(cookie)
# ---------------
browser.refresh()
wait = WebDriverWait(browser, 10)
wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'row-wrap')))
# ---------------

# browser.close()
# ---------------
html = browser.page_source
# with open('.\\log\\problems_page.html', 'wb') as f:
# 	f.write((html).encode("GBK",'ignore'))
PagesTotal = re.search(PagesRe, html)
PagesTotal = int(PagesTotal.group(1))
PagesList=[]
for i in range(1,PagesTotal+1):
	tmppage = '{}{}{}'.format(GroupProblemsPage, '?page=', i)
	PagesList.append(tmppage)
# print(PagesList)
log.write(str(PagesList))
ProblemsSet=[]
for web in PagesList:
	browser.get(web)
	wait = WebDriverWait(browser, 10)
	wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'row-wrap')))
	html = browser.page_source
	log.write(str((html).encode("GBK",'ignore')))
	ProblemsSet.extend(re.findall(ProblemsSetRe, html))
ProblemsSet.sort()
log.write(str(ProblemsSet))
with open('ProblemsSet.json', 'w', encoding='utf8') as fp:
	json.dump(ProblemsSet,fp,ensure_ascii=False)
# ---------------

# has saved ProblemsSet
ProblemsSet = []
with open('ProblemsSet.json', 'r', encoding='utf8') as fp:
	ProblemsSet = json.load(fp)
for problem in ProblemsSet:
	Num = str(problem[0])
	PR(Num)
	OutputPath = '.\\Output\\{}\\'.format(Num)
	try:
		os.mkdir(OutputPath)
	except IOError as e:
		pass
	urlq = 'https://www.luogu.com.cn/problem/{}'.format(Num)
	urld = 'https://www.luogu.com.cn/problem/edit/{}#data'.format(Num)
	log.write('-----\n{}\nQuesUrl:{}\nDataUrl:{}\n'.format(
		problem[0], urlq, urld))
	PR('.')
	browser.get(urlq)
	log.write('Getting the problem-card\n')

	wait = WebDriverWait(browser, 10)
	wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'main')))
	html = browser.page_source
	PR('.')
	ProblemCard = re.search(ProblemCardRe, html)
	if ProblemCard is None:
		log.write('Can\'t find the problem-card\n')
	else:
		with open('{}{}.html'.format(OutputPath,Num), 'wb') as f:
			f.write((ProblemCard.group(1)).encode("utf8", 'ignore'))
		log.write('Succeeded\n')
	PR('.')
	log.write('Getting Data\n')
	log.flush()
	# get data 下载数据
	# -----------
	browser.get(urld)
	wait = WebDriverWait(browser, 10)
	wait.until(
		EC.presence_of_all_elements_located((By.CLASS_NAME, 'form-layout')))
	html = browser.page_source
	DataUrl = re.search(DownloadDataRe, html)
	PR('.')
	if (DataUrl is None):
		log.write("There is no data\n")
		print("  ERROR!! There is no data in {}".format(Num))
		continue
	else:
		DataUrl = unescape(DataUrl.group(1))
		log.write(DataUrl+'\n')
	log.write('\nGetting {}\'s Data\n'.format(Num))
	PR('.')
	# print(DataUrl)
	res = requests.get(url=DataUrl, headers=headers, timeout=(5,600))
	# print(res)
	if res.status_code != requests.codes.ok:
		print('Failed in {}'.format(Num))
		log.write('Failed\n')
	else:
		log.write('Succeeded\n')
	with open('{}{}data.zip'.format(OutputPath, Num), 'wb') as fp:
		fp.write(res.content)
	PR('.\n')
	# -----------
	log.write('\n')
log.close()
browser.close()
# %%
