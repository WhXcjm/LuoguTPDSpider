# 请尊重版权！！
# 洛谷团队题目爬取Spider
## 概述

参考速度：350题/15分钟

使用Cookies
## 使用方法

### 1. 懒得了解python
注：程序中都有提示

下载自己chrome对应版本的chromedriver，自己搜搜

国内可以考虑: http://npm.taobao.org/mirrors/chromedriver/

国外的话: http://chromedriver.storage.googleapis.com/

下载完放到exe同目录或者添加path

然后运行Spider v?.?.?.exe根据提示操作，注册码用Register Machine.exe（1.2以后不需要key）

### 2. 有一定py和爬虫基础
主程序Spider.py, 看着import自己pip装插件

少注释，感觉较好理解

## 版本记录

### v ? -1
本地成功运行

### v1.1.1	

加入~~水的一批的~~加密，关闭selenium dev-tool提醒，加入icon，修锅，降低requests版本（因为pyinstaller4.2对requests2.25.1支持有问题，无法正常使用，于是改用requests2.24.0，然后啥问题也没有了）

### v1.2.0

加入题目列表储存
