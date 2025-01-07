import json

from utils.chat_tool import ChatClient
from utils.db_tool import DatabaseAccessTool

# 使用示例
api_key_air = "2f252bef2ec446719359d4457574fee1.JOfVYlXzamOs2Qwc"
api_key_zone = "bb39dea715524cce99af3e9e9a5d8be0.tbf9mU4sw3BUnerD"
access_token = "e904a3cadd95478296e90c6bb954f614"  # 替换为你的Access Token
db_tool = DatabaseAccessTool(access_token)


def get_sql(message, txt_file_path="data/all_tables_schema.txt"):
    client = ChatClient(api_key_air, model = "glm-4-air")
    client.clear_messages()
    # 设置更具体的系统提示词
    system_prompt = (
        "作为数据分析大师，你的任务是根据以下数据库表描述信息，理解各个数据库及数据表之间的关系。"
        "针对用户的问题，生成准确、高效的MySQL SQL查询语句。请确保只返回SQL语句字符串，并将SQL字符串用MarkDown的代码块格式包裹。"
    )
    client.add_message("system", system_prompt)
    # 尝试读取文件内容并添加到客户端消息中
    with open(txt_file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()
        client.add_message("system", "请严格使用表描述信息中的表名和字段名，表描述信息如下：" + file_content)
    # 添加用户的消息
    client.add_message("user", message)
    msg = extract_and_normalize_sql(client.send_message())
    return msg


def extract_and_normalize_sql(input_string):
    # 按照```分割字符串
    parts = input_string.split("```")
    # 取第二部分，即SQL语句部分
    sql_part = parts[1].strip()
    # 去掉前面的‘sql’和回车符
    if sql_part.startswith("sql"):
        sql_part = sql_part[3:].strip()
    return sql_part


def get_answer(questions):
    client = ChatClient(api_key_zone, model="glm-zero-preview")
    for question in questions:
        print("**********************************************************")
        print("----------------------------------------------------------")
        print("当前问题：" + question["question"])
        print("----------------------------------------------------------")
        sql = get_sql(question["question"])
        print("获取到的SQL：" + sql)
        print("----------------------------------------------------------")
        data = db_tool.execute_sql(sql)
        print("获取到的数据：" + str(data))
        print("----------------------------------------------------------")
        client.add_message("user", "数据库运行了:" + sql + "获取到如下数据：" + json.dumps(data)+"\n"+"请根据这些数据回答问题：" + question["question"]+"\n"+"如果查询失败，请自行搜索数据回答问题，确保问题回答自然")
        question["answer"] = client.send_message()
        client.add_message("system", question["answer"])
        print("----------------------------------------------------------")
        print("当前答案：" + question["answer"])
        print("----------------------------------------------------------")
        print("**********************************************************")
    return questions
