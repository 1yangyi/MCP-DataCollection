import re
from utils import remove_empty_children


def parse_line(line):
    """解析单行数据，返回节点信息"""
    # 计算缩进层级（每2个空格为一级）
    indent = len(line) - len(line.lstrip())
    level = indent // 2

    # 解析按钮数据
    buttons = parse_buttons(line)

    return {
        "level": level,
        "buttons": buttons
    }



def parse_buttons(line):
    """解析一行中的buttons属性，返回按钮列表"""
    # 匹配buttons=[...]部分
    buttons_match = re.search(r"buttons=\[(.*?)\]", line)
    if not buttons_match:
        return []

    buttons_str = buttons_match.group(1)
    # 匹配text和url对
    pattern = r"text='(.*?)', url='(.*?)'"
    buttons = re.findall(pattern, buttons_str)
    return [{"text": text, "url": url} for text, url in buttons]



def build_tree(lines):
    root = []
    stack = [{"node": None, "level": -1, "children": root}]

    for line in lines:
        if not line.strip():
            continue

        data = parse_line(line)
        level = data["level"]
        buttons = data["buttons"]

        if not buttons:
            continue

        while stack and stack[-1]["level"] >= level:
            stack.pop()

        parent = stack[-1]

        for i, button in enumerate(buttons):
            new_node = {"text": button["text"], "url": button["url"]}

            if i == len(buttons) - 1:
                new_node["children"] = []
                stack.append({
                    "node": new_node,
                    "level": level,
                    "children": new_node["children"]
                })

            parent["children"].append(new_node)

    # ✅ 使用外部导入的清理函数
    remove_empty_children(root)

    return root
