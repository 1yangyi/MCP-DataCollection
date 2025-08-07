# MCP-DataCollection

提取大学官网网页结构中的可点击按钮，并输出为结构化树结构（TXT + JSON），用于后续数据分析以及信息抓取


# 项目介绍

高校网站导航结构分析
页面按钮提取
web爬虫预处理
可视化按钮路径构建


# 使用说明

pip install -r requirements.txt
中国高校 -> data/raw_html/chinese_university/
qs top高校 -> data/raw_html/qs_university/


# 输出说明

.txt  缩进可读结构树
.json 标准JSON树结构 （大模型处理）