from datetime import datetime




def print_tree(node, indent=0, file=None):
    # 提取当前节点的基础信息
    tag = node.get("tag", "")
    class_attr = node.get("class", "")
    buttions = node.get("buttons", [])  # 获取buttions列表（可能为空）

    # 判断是否需要打印当前节点（buttions非空）
    should_print = len(buttions) > 0

    # 打印当前节点（若需要）
    if should_print:
        # 构建缩进字符串（每层2空格）
        indent_str = "  " * indent
        # 整理节点属性（仅非空属性）
        attrs = []
        if tag:
            attrs.append(f"tag='{tag}'")
        if class_attr:
            attrs.append(f"class='{class_attr}'")
        # 整理buttions内容（每个按钮的text和relative_url）
        buttion_strs = []
        for btn in buttions:
            btn_text = btn.get("text", "").strip()
            btn_url = btn.get("relative_url", "").strip()
            if btn_text or btn_url:  # 按钮有有效内容才显示
                btn_info = f"text='{btn_text}', url='{btn_url}'"
                buttion_strs.append(btn_info)
        if buttion_strs:
            attrs.append(f"buttons=[{', '.join(buttion_strs)}]")
        # 打印节点信息
        #print(f"{indent_str}{{ {', '.join(attrs)} }}")
        if file:
            file.write(f"{indent_str}{{ {', '.join(attrs)} }}\n")

    # 递归处理子节点（无论当前节点是否打印）
    for child in node.get("children", []):
        print_tree(child, indent + 1, file)





def remove_empty_children(node):
    """
    递归移除没有 buttons 且没有 children 的“空节点”
    可以作用于树的根节点（list 或 dict）
    """
    if isinstance(node, dict):
        if "children" in node and len(node["children"]) == 0:
            del node["children"]
        else:
            for child in node.get("children", []):
                remove_empty_children(child)
    elif isinstance(node, list):
        for item in node:
            remove_empty_children(item)