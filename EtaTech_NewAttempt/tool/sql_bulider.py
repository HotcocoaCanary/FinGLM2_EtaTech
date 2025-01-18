import json

# 从自定义模块中导入所需的功能
from EtaTech_NewAttempt.tool.data_recall import recall_data
from EtaTech_NewAttempt.utils.chat_tool import ChatTool
from EtaTech_NewAttempt.utils.db_tool import DBTool

# 模型名称和API密钥
# model_air = "glm-4-air"
# api_key_air = '2f252bef2ec446719359d4457574fee1.JOfVYlXzamOs2Qwc'
model = "glm-zero-preview"
api_key = "bb39dea715524cce99af3e9e9a5d8be0.tbf9mU4sw3BUnerD"

# 创建ChatTool实例
chat = ChatTool(api_key, model)


def get_sql_list(select_table_description, table_dict, questions, known):
    """
    生成SQL语句列表
    :param select_table_description: 数据表说明
    :param table_dict: 数据表结构信息
    :param questions: 用户问题
    :param known: 已知信息
    :return: SQL语句列表
    """
    # 构建消息列表，用于与ChatTool交互
    messages = [
        {
            "role": "system",
            "content": "你是一个SQL生成大师，你需要仔细分析数据库表结构信息，结合表说明和注意事项，最后根据我提问的问题，生成对应的SQL语句，每一个元素为一个sql语句，其中key为sql，value为对应的sql语句）。\n"
                       "注意：查询时，一定要使用‘数据库名.表名’的格式（‘将数据库名’和‘表名’使用数据表结构信息中的数据库名和表名替换）。\n"
                       "针对需要多次分步骤运行的sql语句，我会先运行你返回的sql语句，并将结果保存在known中返回给你。可以根据known中的数据，生成后续的sql语句或优化查询sql语句。\n"
                       "可能用到的数据表结构信息如下：\n" + str(table_dict) +
                       "对应数据表注意事项及说明如下：\n" + str(select_table_description) +
                       "当前已知信息：\n" + str(known)
        },
        {
            "role": "user",
            "content": "根据我当前问题，请生成对应的SQL语句（以json数组的形式返回，每一个元素为一个sql语句，其中key为sql，value为对应的sql语句）。\n"
                       "问题如下：\n" + questions
        }
    ]

    # 设置消息并获取ChatTool的回复
    chat.set_message(messages)
    answer = chat.send_message()

    # 解析回复中的SQL语句列表
    sql_list = json.loads(answer.split("```json")[1].split("```")[0].strip())
    return sql_list


def execute_sql_and_check(sql_list, select_table_description, table_dict, questions):
    """
    执行SQL语句并检查结果
    :param sql_list: SQL语句列表
    :param select_table_description: 数据表说明
    :param table_dict: 数据表结构信息
    :param questions: 用户问题
    :return: 已知信息列表
    """
    known = []
    check = 0
    for sql in sql_list:
        # 执行SQL语句
        result = DBTool().execute_sql(sql["sql"])
        print(result)
        known.append(result)
        # 检查执行结果
        if 'success' not in result:
            check += 1
    # 如果超过一半的SQL语句执行失败，重新生成SQL语句并执行
    if check >= len(sql_list) / 2:
        sql_list = get_sql_list(select_table_description, table_dict, questions, known)
        return execute_sql_and_check(sql_list, select_table_description, table_dict, questions)
    return known


def get_answer_data(question_data, table_description_path, data_dict_path):
    """
    获取答案数据
    :param question_data: 问题数据
    :param table_description_path: 数据表说明路径
    :param data_dict_path: 数据字典路径
    """
    for i in question_data:
        # 获取数据表说明、数据表结构信息和用户问题
        select_table_description, table_dict, questions = recall_data(i["team"], table_description_path, data_dict_path)

        # 生成SQL语句列表
        sql_list = get_sql_list(select_table_description, table_dict, questions, [])

        # 执行SQL语句并检查结果
        # TODO: SQL生成还是不稳定，不能达到半数以上运行成功找到想要的数据
        known = execute_sql_and_check(sql_list, select_table_description, table_dict, questions)

        # 打印已知信息
        print(known)
        # TODO: 根据已知信息生成答案
