#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Vote host: https://www.thaiupdate.info/
# True host: https://poll.fm/
# Author: 饼干
# Notice: Only for MilkLove

import requests
import re
import sys
import time
import urllib3
import datetime
import threading
import secrets
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

P = "14890595"
ID = "66059332"
MD5 = "2d370c3ad34459c1d834f68aef97491b"

# 代理设置,可以挂梯子,也可以不挂,默认不挂
proxies = {
#   "http": "http://127.0.0.1:7890",  
#   "https": "http://127.0.0.1:7890",  
}  

# 随机UA
def user_agent_generator():
    base_ua = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537."
    current_version = 36

    def get_next_ua():
        nonlocal current_version
        ua = f"{base_ua}{current_version}"
        current_version += 1
        return ua

    return get_next_ua

# 投票函数
def vote():
    global num
    global get_ua
    # random_sec_ch_ua, random_user_agent = random_secchua_ua()
    strA = secrets.token_hex(8)
    random_sec_ch_ua = f'"Google Chrome";v="{secrets.randbelow(100)}", "Chromium";v="{secrets.randbelow(100)}", ";Not A Brand";v="99"'
    random_user_agent = get_ua()
    
    headers1 = {
        'Sec-Ch-Ua': random_sec_ch_ua,
        'Sec-Ch-Ua-Mobile': '?0',
        'User-Agent': random_user_agent,
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Dest': 'script',
        'Referer': f'https://poll.fm/{P}/embed',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'ccpa_applies=false',
    }
    headers2 = {
        'Sec-Ch-Ua': random_sec_ch_ua,
        'Sec-Ch-Ua-Mobile': '?0',
        'User-Agent': random_user_agent,
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Dest': 'script',
        'Referer': 'https://poll.fm/',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'close'
    }

    # 1.获取N值
    url1 = f'https://poll.fm/n/{MD5}/{P}?{int((datetime.datetime.now()).timestamp() * 1000)}'

    try:
        res1 = requests.get(url=url1, headers=headers1, verify=False, proxies=proxies, timeout=5)
    except Exception:
        return -1   # 网络错误

    match = re.search(r"PDV_n\d+='([^']+)'", res1.text)
    valueN = match.group(1)

    # 2.获取数学题
    url2='https://polls.polldaddy.com/vote-js.php'
    params2 = {
        'p': P,
        'a': strA+',',
        'n': valueN
    }
    
    try:
        res2 = requests.get(url=url2, params=params2, headers=headers2, verify=False, proxies=proxies, timeout=5)
        res2_content = res2.text
    except Exception:
        return -1   # 网络错误

    formatted_time = (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    
    if '<input id="answer_' in res2_content:
        math_problem_match = re.search(r'<span><p>([^"]+)= </p><input id="answer_', res2_content)
        maths_key_match = re.search(r'name="maths_key" value="([^"]+)"', res2_content)
        answer = eval(math_problem_match.group(1))
        maths_key = maths_key_match.group(1)
    else:
        print(f"[-][\033[94m{formatted_time}\033[0m] [\033[91m投票失败\033[0m] 没有数学问题验证码")
        time.sleep(0.5)
        return -2   # 没有数学题, 投票失败

    # 3.发起投票
    url3 = f'https://polls.polldaddy.com/vote-js.php'
    params3 = {
        'p': P,
        'a': ID+',',
        'o': '',
        'va': '16',
        'cookie': '0',
        'tags': f'{P}-src:poll-embed',
        'n': valueN,
        'maths': '1',
        'answer': answer,
        'maths_key': maths_key
    }

    try:
        response2 = requests.get(url=url3, params=params3, headers=headers2, verify=False, proxies=proxies, timeout=5)
    except Exception:
        return -1   # 网络错误

    if f"PDF_callback{P}" in response2.text: 
        num += 1
        print(f"[+][\033[94m{formatted_time}\033[0m] [\033[92m投票成功\033[0m] milklove vote +{num}")
        return 0    # 投票成功
    else:
        print(f"[-][\033[94m{formatted_time}\033[0m] [\033[93m投票无效\033[0m] 有数学问题 但投票无效")
        time.sleep(2)
        return -3   # 投票无效

def banner(act='banner'):
    banner = r'''
 __    __     __         __   __   ______     ______   ______    
/\ "-./  \   /\ \       /\ \ / /  /\  __ \   /\__  _\ /\  ___\   
\ \ \-./\ \  \ \ \____  \ \ \'/   \ \ \/\ \  \/_/\ \/ \ \  __\   
 \ \_\ \ \_\  \ \_____\  \ \__|    \ \_____\    \ \_\  \ \_____\ 
  \/_/  \/_/   \/_____/   \/_/      \/_____/     \/_/   \/_____/ 
                                            version 2.0
                                            Author  饼干  
    '''
    helper = r'''
Usage: python mlvote.py [threadcount]
Example: python mlvote.py 10

说明：
1. 用 Python 3 来运行这个程序。
2. `threadcount` 是用来设置线程数的。 

小贴士：试试不同的数字，找到跑得最快的那个。
'''
    
    print(banner)
    if act == 'helper':
        print(helper)

def vote_worker():
    while True:
        vote()

if __name__ == "__main__":  
    try:
        threadcount = int(sys.argv[1])
    except:
        banner('helper')
        exit()

    banner()
    num = 0

    # 创建 User-Agent 生成器
    get_ua = user_agent_generator()

    lock = threading.Lock()
    threads = [] 
    for i in range(threadcount-1):  
        t = threading.Thread(target=vote_worker)
        threads.append(t)
        t.start()
