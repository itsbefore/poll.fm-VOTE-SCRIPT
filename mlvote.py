import requests
import re  
import urllib3
import time
import datetime  
import threading
import random  
import string  
import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
  
id = "61391006"

proxies = {  
  "http": "http://127.0.0.1:1080",  
  "https": "http://127.0.0.1:1080",  
}  

def generate_random_string(length):  
    # 定义可选择的字符集  
    chars = string.ascii_letters + string.digits  
    # 使用random.choice从chars中随机选择length个字符  
    random_string = ''.join(random.choice(chars) for i in range(length))  
    return random_string  
  


def vote(getN,stra):
    headers = {
        'Host': 'polls.polldaddy.com',
        'Sec-Ch-Ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'Sec-Ch-Ua-Mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Dest': 'script',
        'Referer': 'https://poll.fm/',
        # 'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    # print("[-]获取数学问题验证码...")
    response = requests.get(f'https://polls.polldaddy.com/vote-js.php?p=13755834&a={stra},&n={getN}', headers=headers, verify=False, proxies=proxies)
    # print(response.text)
    response_string = response.text

    math_problem_match = re.search(r'<span><p>([^"]+)= </p><input id="answer_', response_string)  
    maths_key_match = re.search(r'name="maths_key" value="([^"]+)"', response_string)  
    
    answer=None
    maths_key=None
    
    #print(now)
    if math_problem_match:  
        math_problem = math_problem_match.group(1)  
        # print(f"[-]数学问题: {math_problem}",end="")  
        answer = eval(math_problem)
        # print(f"计算结果是: {answer}")
    
    if maths_key_match:  
        maths_key = maths_key_match.group(1)  
        # print(f"[-]maths_key的值: {maths_key}")
    
    if answer and maths_key:
        # print("[-]开始投票(有数学问题)...")
        response = requests.get(f'https://polls.polldaddy.com/vote-js.php?p=13755834&b=0&a={id},&o=&va=16&cookie=0&tags=13755834-src:poll-embed&n={getN}&maths=1&answer={answer}&maths_key={maths_key}', headers=headers, verify=False, proxies=proxies)
        if "Thank you for voting!" in response.text:
            with lock:  
                global num  
                num += 1 
            now = datetime.datetime.now()  
            formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
            print(f"[+][{formatted_time}] 投票成功 milklove vote +{num}")
    else:
        print("[!]没有数学问题, 投票失效, 请稍后重试.")
        # print(response_string)
        return 0
        # exit(0)


    
def getN(stra):
    cookies = {
        'ccpa_applies': 'false',
    }

    headers = {
        'Host': 'poll.fm',
        'Sec-Ch-Ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'Sec-Ch-Ua-Mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Dest': 'script',
        'Referer': 'https://poll.fm/13755834/embed?continueFlag=d47e28589e5560290b008213062e2508',
        # 'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        # 'Cookie': 'ccpa_applies=false',
    }
    
    url = f'https://poll.fm/n/45e9312a31ff676c023c9b55d94a8f2a/13755834?{gettime()}'
    
    # print(f"[-]开始请求N : {url}")
    response = requests.get(url, cookies=cookies, headers=headers, verify=False, proxies=proxies)
        
    # print(response.text)   
    response_content = response.text
    match = re.search(r"PDV_n\d+='([^']+)'", response_content)  
     
    if match:  
        value = match.group(1)  
        # print(f"[+]获取到N: {value}")  # 输出: 9bf5d6d580|286
        if vote(value,stra)==0:
            return 0

def gettime():
    now = datetime.datetime.now()   
    seconds = int(datetime.datetime.timestamp(now))  
    milliseconds = now.microsecond // 1000  
    milliseconds_since_epoch = seconds * 1000 + milliseconds  
    # print(f"[+]获取毫秒时间戳: {milliseconds_since_epoch}")
    return milliseconds_since_epoch



def main():
    stra = generate_random_string(5) 
    for i in range(7000):#135,961
        # print(f"\n--------------第{i+1}次请求---------------")
        # print(f"[+]随机a值: {stra}")
        k = getN(stra)
        # time.sleep(2)
        if k==0:
            stra = generate_random_string(5) 
            
if __name__ == "__main__":  

    lock = threading.Lock()
    num = 0
    threads = []  

    # 创建并启动线程  
    for i in range(10):  
        t = threading.Thread(target=main)  
        threads.append(t)  
        t.start()  
  
    # 等待所有线程完成  
    for t in threads:  
        t.join()  
    
    # 打印总的请求次数  
    print(f"Total requests made: {num}")