import requests










def fetch_html(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # 检查HTTP状态码（如404/500）
        response.encoding = response.apparent_encoding  # 自动检测编码
        return response.text  # 返回字符串类型的HTML
    except requests.exceptions.RequestException as e:
        # 网络请求失败时返回字典标记
        return {"tree": False}


def check_buttons_pairs(s):
    # 使用正则表达式匹配：在 'buttons' 后出现至少两个连续的 'text' 和 'url' 对
    pattern = r'buttons(.*?text.*?url.*?){2}'
    if re.search(pattern, s, re.DOTALL):  # re.DOTALL 使 . 匹配包括换行符的所有字符
        return True
    else:
        return False