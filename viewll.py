import requests
import re
import time
import datetime  
  
proxies = {  
  "http": "http://127.0.0.1:1080",  
  "https": "http://127.0.0.1:1080",  
}  
def req():
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
        'Connection': 'close',
    }
    try:
        response = requests.get('https://polls.polldaddy.com/vote-js.php?p=13755834', headers=headers, verify=True, proxies=proxies)
    except:
        pass
    # print(response.text)
    return response.text

def reData(pattern,response_content):
    match = re.search(pattern, response_content)  
    if match:  
        percentage = match.group(1)
        votes = match.group(2)
        return percentage, votes

def toNum(number_string):
    number_string_without_comma = number_string.replace(',', '')  
    # 将字符串转换为整数  
    return int(number_string_without_comma)  

pattern = r'Milk Love </span><span class="pds-feedback-result"><span class="pds-feedback-per">&nbsp;([\d.]+)%</span><span class="pds-feedback-votes">&nbsp; \(([^"]+) votes\)'  
patternLing_Orm = r'Ling Orm </span><span class="pds-feedback-result"><span class="pds-feedback-per">&nbsp;([\d.]+)%</span><span class="pds-feedback-votes">&nbsp; \(([^"]+) votes\)'



votes_old = "0"
votesLing_Orm_old = "0"

while True:
    text = str(req())#获取排名页面
    
    percentage, votes = reData(pattern, text)
    percentageLing_Orm, votesLing_Orm = reData(patternLing_Orm, text)

    lex_votes = toNum(votes) - toNum(votes_old)
    lex_votesLing_Orm = toNum(votesLing_Orm) - toNum(votesLing_Orm_old)

    votes_old = votes
    votesLing_Orm_old = votesLing_Orm
    # 获取当前时间  
    now = datetime.datetime.now()  
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")

    print(f"-----------{formatted_time}-----------")
    print(f"Ling Orm: vote:{votesLing_Orm}  percent:{percentageLing_Orm}")
    print(f"milklove: vote:{votes}  percent:{percentage}")
    print(f"Ling_Orm增长: {lex_votesLing_Orm}")
    print(f"milklove增长: {lex_votes}")
    print(f"相差: {toNum(votesLing_Orm)-toNum(votes)}\n")
    time.sleep(10)