from extractor import build_tree_structure, filter_empty_nodes
from processor import process_file
from tree_parser import build_tree
from utils import print_tree
import json
import os

from bs4 import BeautifulSoup






# 处理一个 HTML 文件：读取、解析、保存 txt/json
def process_html_file(html_path, txt_path, json_path):
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")
    root = soup.find("html")
    if not root:
        print(f"⚠️ HTML 无法解析：{html_path}")
        return

    tree = build_tree_structure(root)
    filtered = filter_empty_nodes(tree)

    # 保存缩进结构
    with open(txt_path, "w", encoding="utf-8") as f:
        print_tree(filtered, indent=0, file=f)

    # 修复缩进
    process_file(txt_path)

    # 构建 JSON 树结构
    with open(txt_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    json_tree = build_tree(lines)

    # 保存 JSON
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_tree, f, ensure_ascii=False, indent=2)

    print(f" 处理完成：{html_path}")
    print(f"  ├── TXT 输出：{txt_path}")
    print(f"  └── JSON 输出：{json_path}")




if __name__ == "__main__":
    base_raw = "data/raw_html"
    base_out = "data/output"

    categories = ["chinese_university", "qs_university"]

    for category in categories:
        raw_folder = os.path.join(base_raw, category)
        txt_folder = os.path.join(base_out, category, "txt_tree")
        json_folder = os.path.join(base_out, category, "json_tree")

        # 确保输出目录存在
        os.makedirs(txt_folder, exist_ok=True)
        os.makedirs(json_folder, exist_ok=True)

        # 遍历该类别下的所有 HTML 文件
        for filename in os.listdir(raw_folder):
            if filename.lower().endswith(".html"):
                name = os.path.splitext(filename)[0]  # 例如 WHU.html → WHU

                html_path = os.path.join(raw_folder, filename)
                txt_path = os.path.join(txt_folder, f"{name}.txt")
                json_path = os.path.join(json_folder, f"{name}.json")

                process_html_file(html_path, txt_path, json_path)

