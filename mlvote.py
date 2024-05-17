import requests
import re  
import urllib3
import time
import datetime  
import threading
import random  
import string  

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
  
id = "61391006"     # milklove 的投票id
errNum = 0          # 统计投票错误连续次数

# 代理配置
proxies = {}
# proxies = {  
#   "http": "http://127.0.0.1:1080",  
#   "https": "https://127.0.0.1:1080",  
# }  

# 获取随机字符串
def generate_random_string(length):  
    chars = string.ascii_letters + string.digits 
    random_string = ''.join(random.choice(chars) for i in range(length))  
    return random_string  

# 投票函数
def vote(getN,stra):
    global errNum
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
    try:
        response = requests.get(f'https://polls.polldaddy.com/vote-js.php?p=13755834&a={stra},&n={getN}', headers=headers, verify=False, proxies=proxies)
    except:
        return 0
    # print(response.text)
    response_string = response.text

    math_problem_match = re.search(r'<span><p>([^"]+)= </p><input id="answer_', response_string)  
    maths_key_match = re.search(r'name="maths_key" value="([^"]+)"', response_string)  
    
    with lock: 
        answer=None
        maths_key=None

    if math_problem_match:  
        math_problem = math_problem_match.group(1)   
        answer = eval(math_problem)
        # print(f"[-]数学问题验证码: {math_problem}",end="") 
        # print(f"计算结果是: {answer}")
    
    if maths_key_match:  
        maths_key = maths_key_match.group(1)  
        # print(f"[-]maths_key的值: {maths_key}")
    
    # 获取当前时间
    now = datetime.datetime.now()  
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    
    if answer and maths_key:
        try:
            response = requests.get(f'https://polls.polldaddy.com/vote-js.php?p=13755834&b=0&a={id},&o=&va=16&cookie=0&tags=13755834-src:poll-embed&n={getN}&maths=1&answer={answer}&maths_key={maths_key}', headers=headers, verify=False, proxies=proxies)
        except:
            return 0    # 请求报错
        
        with lock:
            errNum = 0
        
        if "PDF_callback13755834" in response.text: # 返回包有PDF_callback13755834代表投票成功!
            with lock:  
                global num  
                num += 1
            print(f"[\033[94m{formatted_time}\033[0m] [\033[92m投票成功\033[0m] 数学问题: {math_problem} milklove vote +{num}")    
        else:
            print(f"[\033[94m{formatted_time}\033[0m] [\033[93m投票无效\033[0m] 有数学问题验证码 但投票无效.")
    else:
        errNum += 1
        if errNum > 5: 
            exit(0)
        
        print(f"[\033[94m{formatted_time}\033[0m] [\033[91m投票失败\033[0m] 没有数学问题验证码 请稍后重试.")
        return 0 

# 获取服务端随机N值, 一个N值对应可以投5票, 所以需要先获取N
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
    
    url = f'https://poll.fm/n/45e9312a31ff676c023c9b55d94a8f2a/13755834?{gettime()}'    # N值的获取, 只需要传入时间戳

    try:
        response = requests.get(url, cookies=cookies, headers=headers, verify=False, proxies=proxies)
    except:
        return 0
    
    response_content = response.text
    
    match = re.search(r"PDV_n\d+='([^']+)'", response_content) # 获取服务端随机N值
     
    if match:  
        value = match.group(1)  
        # print(f"[+]获取到N: {value}")
        
        kk = vote(value,stra)   # 调用投票函数, 传入N值、随机字符串a
        
        if kk == 0: # 如果返回错误
            return 0    # 也返回错误码0

# 获取毫秒时间戳
def gettime():
    now = datetime.datetime.now()   
    seconds = int(datetime.datetime.timestamp(now))  
    milliseconds = now.microsecond // 1000  
    milliseconds_since_epoch = seconds * 1000 + milliseconds  
    # print(f"[+]获取毫秒时间戳: {milliseconds_since_epoch}")
    return milliseconds_since_epoch

def main():
    stra = generate_random_string(15) 
    for i in range(100): 
        k = getN(stra)
        if k==0:
            # time.sleep(2)
            stra = generate_random_string(15) 


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
    
    if errNum > 5:
        # 投票失败次数  
        print(f"Error times: {errNum}")
    # 打印总的请求次数  
    print(f"Total requests made: {num}")
