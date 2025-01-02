import requests
from bs4 import BeautifulSoup
import re
import time
import smtplib
import os

def check_content_existence(url, title_pattern, match_type='partial'):
    """
    访问指定网址，检查是否存在匹配指定标题模式的内容。

    Args:
        url (str): 要访问的网址
        title_pattern (str): 标题匹配模式（正则表达式）
        match_type (str): 匹配类型，可选 'partial'（部分匹配），'full'（完全匹配），'start'（开头匹配）

    Returns:
        bool: 如果找到匹配的内容返回 True，否则返回 False
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://ins.seu.edu.cn/',
    }

    try:
        # 发送 GET 请求
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # 如果请求不成功，抛出异常

        # 解析 HTML 内容
        soup = BeautifulSoup(response.text, 'html.parser')

        # 查找所有可能的标题元素
        potential_titles = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span', 'div'])

        # 检查每个潜在的标题是否匹配
        for element in potential_titles:
            text = element.get_text().strip()
            if text:  # 只检查非空文本
                if match_type == 'full':
                    if re.fullmatch(title_pattern, text, re.IGNORECASE):
                        print(f"\n找到匹配! 匹配文本: {text}")
                        return True
                elif match_type == 'start':
                    if re.match(title_pattern, text, re.IGNORECASE):
                        print(f"\n找到匹配! 匹配文本: {text}")
                        return True
                else:  # default to partial match
                    if re.search(title_pattern, text, re.IGNORECASE):
                        print(f"\n找到匹配! 匹配文本: {text}")
                        return True

        print("\n未找到匹配内容。")
        return False

    except requests.RequestException as e:
        print(f"访问网站时出错: {e}")
        return False

# 主程序
if __name__ == "__main__":
    url = "https://ins.seu.edu.cn/26759/list1.htm"
    title_pattern = r"博士"
    match_type = 'partial'

    print(f"正在检查网址: {url}")
    print(f"查找模式: '{title_pattern}'")
    print(f"匹配类型: {match_type}")

    time.sleep(2)

    content_exists = check_content_existence(url, title_pattern, match_type)

    if content_exists:
        message = f"在网页 {url} 中找到了匹配 '{title_pattern}' 的内容（{match_type}匹配）。"
        print(message)
    else:
        print(f"\n结果: 在网页中未找到匹配 '{title_pattern}' 的内容（{match_type}匹配）。")
