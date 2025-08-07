from extractor import build_tree_structure, filter_empty_nodes
from processor import process_file
from tree_parser import build_tree
from utils import print_tree
import json
import os

from bs4 import BeautifulSoup


if __name__ == "__main__":
    # 设置文件路径
    html_path = "data/raw_html/WHU.html"
    txt_path = "data/txt_tree/WHU.txt"
    json_path = "data/json_tree/WHU.json"

    # 读取本地 HTML 文件
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    root = soup.find('html')

    # 生成按钮树
    full_tree = build_tree_structure(root)
    filtered_tree = filter_empty_nodes(full_tree)

    # 保存为缩进文本结构
    with open(txt_path, "w", encoding="utf-8") as f:
        print_tree(filtered_tree, indent=0, file=f)

    # 缩进结构清洗
    process_file(txt_path)

    # 读取清洗后的 txt，构建 JSON 树结构
    with open(txt_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    tree = build_tree(lines)

    # 输出到 json
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(tree, f, ensure_ascii=False, indent=2)

    print("✅ 成功提取按钮结构并输出为 JSON！")

