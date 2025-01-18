import json
import time

from EtaTech_NewAttempt.tool.data_recall import recall_data
from EtaTech_NewAttempt.utils.chat_tool import ChatTool
from EtaTech_NewAttempt.utils.db_tool import DBTool

# model_air = "glm-4-air"
# api_key_air = '2f252bef2ec446719359d4457574fee1.JOfVYlXzamOs2Qwc'
model = "glm-zero-preview"
api_key = "bb39dea715524cce99af3e9e9a5d8be0.tbf9mU4sw3BUnerD"
chat = ChatTool(api_key, model)

def get_sql_list(select_table_description, table_dict, questions, known):
    sql_list = []
    messages = [
        {
            "role": "system",
            "content": "你是一个SQL生成大师，你需要仔细分析数据库表结构信息，结合表说明和注意事项，最后根据我提问的问题，生成对应的SQL语句，每一个元素为一个sql语句，其中key为sql，value为对应的sql语句）。\n"
                       "注意：查询时，一定要使用‘数据库名.表名’的格式（‘将数据库名’和‘表名’使用数据表结构信息中的数据库名和表名替换）。\n"
                       "针对需要多次分步骤运行的sql语句，我会先运行你返回的sql语句，并将结果保存在known中返回给你。可以根据known中的数据，生成后续的sql语句或优化查询sql语句。\n"
                       "可能用到的数据表结构信息如下：\n" + str(table_dict)+
                       "对应数据表注意事项及说明如下：\n" + str(select_table_description)+
                       "当前已知信息：\n" + str(known)
        },
        {
            "role": "user",
            "content": "根据我当前问题，请生成对应的SQL语句（以json数组的形式返回，每一个元素为一个sql语句，其中key为sql，value为对应的sql语句）。\n"
                       "问题如下：\n" + questions
        }
    ]
    chat.set_message(messages)
    answer = chat.send_message()
    sql_list = json.loads(answer.split("```json")[1].split("```")[0].strip())
    return sql_list


def execute_sql_and_check(sql_list, select_table_description, table_dict, questions):
    known = []
    check = 0
    for sql in sql_list:
        result = DBTool().execute_sql(sql["sql"])
        print(result)
        known.append(result)
        if 'success' not in result:
            check += 1
    if check >= len(sql_list) / 2:
        sql_list = get_sql_list(select_table_description, table_dict, questions, known)
        return execute_sql_and_check(sql_list, select_table_description, table_dict, questions)
    return known


def get_answer_data(question_data, table_description_path, data_dict_path):
    for i in question_data:
        select_table_description, table_dict, questions= recall_data(i["team"], table_description_path, data_dict_path)
        sql_list = get_sql_list(select_table_description, table_dict, questions, [])
        known = execute_sql_and_check(sql_list, select_table_description, table_dict, questions)
        print(known)