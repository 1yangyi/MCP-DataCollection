from bs4 import BeautifulSoup
# 解析HTML

import re
# 处理onclick 的javaScripts,提取字符串




def is_clickable(element):
    """判断元素是否为可点击按钮（返回True/False）"""
    tag = element.name
    if tag == 'button':
        return True
    if tag == 'input':
        input_type = element.get('type', '').lower()
        return input_type in {'button', 'submit', 'reset'}
    if tag == 'a':
        href = element.get('href', '')
        return href and not href.startswith(('javascript:', '#'))
    if element.has_attr('onclick'):
        return True
    if tag == 'h3' or tag == 'h2':
        return True
    return False





def extract_button_info(element):
    """提取单个按钮的详细信息（text、relative_url等）"""
    # 提取text（针对input标签特殊处理value属性）
    if element.name == 'input':
        text = element.get('value', '')  # input的text是value属性
    else:
        text = element.get_text(strip=True)  # 其他标签提取子节点文本

    # 提取relative_url（根据元素类型）
    relative_url = ""
    if element.name == 'a':
        # 超链接：直接取href的原始值
        relative_url = element.get('href', '')
    elif element.name in ['input', 'button']:
        # 表单提交按钮：查找父<form>的action属性
        form = element.find_parent('form')
        if form:
            relative_url = form.get('action', '')
    else:
        # 其他元素（如带onclick的div）：尝试从onclick中解析
        onclick = element.get('onclick', '')
        match = re.search(r"window\.location\.href\s*=\s*['\"]([^'\"]+)['\"]", onclick)
        if match:
            relative_url = match.group(1)

    return {
        "tag": element.name,
        "text": text,
        "relative_url": relative_url
    }


def build_tree_structure(element, parent_node=None):
    """递归构建树状结构（包含按钮的text和relative_url）"""
    # 当前节点的基础信息（标签、class、id）
    node_info = {
        "tag": element.name,
        "class": ' '.join(element.get('class', [])),  # class转为字符串
        #"id": element.get('id', ""),
        "buttons": [] , # 当前节点直接包含的按钮列表（含text和relative_url）
        "children": []  # 子节点列表（节点或按钮）
    }

    # 递归处理子节点（仅处理元素节点，跳过文本节点）
    for child in element.children:
        if child.name is None:  # 跳过文本节点（如换行符）
            continue

        # 递归构建子节点的树结构
        child_tree = build_tree_structure(child, parent_node=node_info)

        # 将子节点添加到当前节点的children中（仅当子节点非空）
        if child_tree["buttons"] or child_tree["children"]:
            node_info["children"].append(child_tree)

    # 将当前可点击元素添加到父节点的buttons列表中
    if is_clickable(element):
        button_info = extract_button_info(element)
        if parent_node is not None:
            parent_node["buttons"].append(button_info)  # 添加到父节点的buttons
        else:
            node_info["buttons"].append(button_info)  # 根节点自身是按钮（罕见）

    return node_info


def filter_empty_nodes(node):
    """递归过滤无按钮的空节点，返回处理后的节点字典"""
    # 复制当前节点，避免修改原节点
    filtered_node = {
        "tag": node["tag"],
        "class": node["class"],
        #"id": node["id"],
        "buttons": [],
        "children": []
    }

    # 保留当前节点的按钮
    filtered_node["buttons"] = node["buttons"].copy()

    # 递归过滤子节点
    for child in node["children"]:
        filtered_child = filter_empty_nodes(child)
        # 仅保留非空的子节点（即过滤后仍有按钮或子节点的子节点）
        if filtered_child.get("buttons") or filtered_child.get("children"):
            filtered_node["children"].append(filtered_child)

    # 如果当前节点没有按钮，且没有保留的子节点，则返回空字典（表示移除该节点）
    if not filtered_node["buttons"] and not filtered_node["children"]:
        return {}

    return filtered_node


def extract_clickable_buttons_tree(url,output_path):
    """主函数：提取网页中所有可点击按钮并按树状结构输出（含text和relative_url）"""
    html = fetch_html(url)
    # 处理网络请求失败的情况
    if isinstance(html, dict):
        return html
    try:
        soup = BeautifulSoup(html, 'html.parser')
    except Exception as e:
        return {"tree": False}  # HTML解析失败时返回

    # 从根节点<html>开始构建树状结构
    root = soup.find('html')
    if not root:
        return {"tree": False}  # 未找到HTML根节点

    # 构建完整的树状结构
    tree = build_tree_structure(root)

    filtered_tree = filter_empty_nodes(tree)

    with open(output_path, "w", encoding="utf-8") as f:
        print_tree(filtered_tree, indent=0, file=f)  # 传递文件对象给函数

    # 若过滤后无有效节点，返回tree:false
    if not filtered_tree.get("buttons") and not filtered_tree.get("children"):
        return {"tree": False}

    return {"tree": filtered_tree}
