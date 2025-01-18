import json

from EtaTech_NewAttempt.tool.data_recall import recall_data
from EtaTech_NewAttempt.utils.chat_tool import ChatTool

access_token = 'df4f19f600214b9da99db3265023df0a'
model_air = "glm-4-air"
api_key_air = '2f252bef2ec446719359d4457574fee1.JOfVYlXzamOs2Qwc'
model_zero = "glm-zero-preview"
api_key_zero = "bb39dea715524cce99af3e9e9a5d8be0.tbf9mU4sw3BUnerD"

# question_data_path = r'../../data/question.json'
question_data_path = r'../../data/question_test.json'

chat = ChatTool(api_key_zero, model_zero)

def get_sql_list(select_table_description, table_dict, questions, known):
    sql_list = []
    messages = [
        {
            "role": "system",
            "content": "你是一个SQL生成大师，你需要仔细分析数据库表结构信息，结合表说明和注意事项，最后根据我提问的问题，生成对应的SQL语句，每一个元素为一个sql语句，其中key为sql，value为对应的sql语句）。\n"
                       "注意：查询时，一定要使用‘数据库名.表名’的格式（‘将数据库名’和‘表名’使用数据表结构信息中的数据库名和表名替换）。\n"
                       "针对需要多次分步骤运行的sql语句，我会先运行你返回的sql语句，并将结果保存在known中返回给你。\n"
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
    print(answer)
    return sql_list

def get_answer_data(question_data):
    for i in question_data:
        select_table_description, table_dict, questions= recall_data(i["team"])


if __name__ == '__main__':
    question = json.load(open(question_data_path, 'r', encoding='utf-8'))
    get_answer_data(question)
