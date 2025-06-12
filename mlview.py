import requests
import re
import time
import datetime
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning) # 防止ssl证书报错

p = "14890595"
NAME = "Love Pattranite"
# p = "14773738"
# NAME = "Milk Pansa"

proxies = {
#   "http": "http://127.0.0.1:8080",  
#   "https": "http://127.0.0.1:8080",  
}  

def format_time(seconds):
    """将秒数格式化为几天几小时几分钟几秒"""
    days = seconds // 86400
    seconds %= 86400
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return f"{int(days)}天 {int(hours)}小时 {int(minutes)}分钟 {int(seconds)}秒"

def fetch_poll_data():
    """获取投票数据"""
    headers = {
        'Host': 'polls.polldaddy.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Referer': 'https://poll.fm/',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    try:
        response = requests.get(f'https://polls.polldaddy.com/vote-js.php?p={p}', headers=headers, verify=False, proxies=proxies)
        return response.text
    except requests.RequestException as e:
        print(f"请求失败：{e}")
        return None

def extract_all_vote_info(response_content):
    """提取所有选手的投票信息"""
    pattern = r'title="([^"]+)">[^<]*</span><span class="pds-feedback-result"><span class="pds-feedback-per">&nbsp;([\d.]+)%</span><span class="pds-feedback-votes">&nbsp; \(([^"]+) votes\)'
    matches = re.finditer(pattern, response_content)
    
    results = {}
    for match in matches:
        name = match.group(1).strip()
        percentage = match.group(2)
        votes = match.group(3)
        results[name] = {
            'percentage': percentage,
            'votes': votes,
            'votes_count': int(votes.replace(',', ''))
        }
    return results

def print_vote_info(name, data, old_votes):
    """打印投票信息"""
    diff_votes = data['votes_count'] - old_votes.get(name, 0)
    # 设置固定宽度：名字25字符，投票数12字符，百分比8字符，增量8字符
    output = f"{name:<20} 投票数:{data['votes']:>8}  百分比:{data['percentage']:>6}%  增量:{diff_votes:>6}"
    
    if name == NAME:
        print(f"\033[92m{output}\033[0m")
    else:
        print(output)
    return diff_votes

def main():
    old_votes = {}
    interval = 10  # 轮询间隔

    while True:
        now = datetime.datetime.now()
        formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")

        text = fetch_poll_data()
        if text is None:
            time.sleep(interval)
            continue

        results = extract_all_vote_info(text)
        if not results:
            print("未获取到投票数据...")
            time.sleep(interval)
            continue

        print(f"\n-----------{formatted_time}-----------")

        # 按投票数排序
        sorted_results = dict(sorted(results.items(), key=lambda x: x[1]['votes_count'], reverse=True))
        
        # 获取第一名的信息
        first_place_name, first_place_data = next(iter(sorted_results.items()))
        first_place_increment = 0
        name_increment = 0
        diff_votes_with_first = 0

        # 打印所有选手信息
        for name, data in sorted_results.items():
            increment = print_vote_info(name, data, old_votes)
            if name == first_place_name:
                first_place_increment = increment
            if name == NAME:
                name_increment = increment
                diff_votes_with_first = first_place_data['votes_count'] - data['votes_count']

        # 打印票数差距
        print(f"\033[93m与第一名票数差距: {diff_votes_with_first}\033[0m")

        # 计算增量差
        increment_diff = name_increment - first_place_increment
        if increment_diff > 0 and diff_votes_with_first > 0:
            estimated_time_seconds = (diff_votes_with_first / increment_diff) * interval
            formatted_estimated_time = format_time(estimated_time_seconds)
            print(f"\033[94m预计需要时间: {formatted_estimated_time}\033[0m")
        elif increment_diff <= 0:
            print("\033[91m当前增量小于或等于第一名，无法超越。\033[0m")

        # 更新旧投票数
        old_votes = {name: data['votes_count'] for name, data in results.items()}
        
        time.sleep(interval)

if __name__ == "__main__":
    main()
