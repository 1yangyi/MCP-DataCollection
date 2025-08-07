import re





def process_file(filename):
    # 读取文件所有行
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 存储处理后的行和节点栈
    processed_lines = []
    stack = []  # 栈中元素为 (当前行索引, 原始缩进, 节点值)

    for idx, line in enumerate(lines):
        # 计算当前行的原始缩进（空格数）
        indent = 0
        while indent < len(line) and line[indent] == ' ':
            indent += 1

        content = line.strip()
        current_value = content

        # 移除栈中所有缩进大于等于当前行的节点（找到父节点）
        while stack and stack[-1][1] >= indent:
            stack.pop()

        # 检查父节点是否满足条件
        adjust = 0
        if stack:
            parent_idx, parent_indent, parent_value = stack[-1]
            # 如果父节点满足条件，则计算需要删除的缩进量
            if check_buttons_pairs(parent_value):
                adjust = indent - parent_indent  # n = 当前缩进 - 父缩进

        # 应用缩进调整
        new_indent = max(0, indent - adjust)
        new_line = ' ' * new_indent + content + '\n'
        processed_lines.append(new_line)

        # 将当前节点压入栈
        stack.append((idx, indent, current_value))

    # 将处理后的内容写回文件
    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(processed_lines)



def check_buttons_pairs(s):
    # 使用正则表达式匹配：在 'buttons' 后出现至少两个连续的 'text' 和 'url' 对
    pattern = r'buttons(.*?text.*?url.*?){2}'
    if re.search(pattern, s, re.DOTALL):  # re.DOTALL 使 . 匹配包括换行符的所有字符
        return True
    else:
        return False