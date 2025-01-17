import json
import os

from EtaTech_NewAttempt.utils.chat_tool import ChatTool

access_token = 'df4f19f600214b9da99db3265023df0a'
model_air = "glm-4-air"
api_key_air = '2f252bef2ec446719359d4457574fee1.JOfVYlXzamOs2Qwc'
model_zero = "glm-zero-preview"
api_key_zero = "bb39dea715524cce99af3e9e9a5d8be0.tbf9mU4sw3BUnerD"
# question_data_path = r'../../data/question.json'
question_data_path = r'../../data/question_test.json'

# 读取问题组文件
with open(question_data_path, 'r', encoding='utf-8') as f:
    question_data = json.load(f)
# 读取问题
questions = []
for team in question_data:
    new_question=""
    for question in team["team"]:
        new_question += question["question"]
    questions.append(new_question)

print(questions)


chat = ChatTool(api_key_air, model_air)

all_tables_schema_file_path = '../../data/all_tables_schema.txt'
data_dictionary_path = '../../data/数据字典.xlsx'
out_data_base_path = '../out/data/'
all_tables_schema_file = os.path.join(out_data_base_path, "all_tables_schema.json")
table_description_file = os.path.join(out_data_base_path, "table_description.json")

# 读取table_description.json文件
table_description = json.load(open(table_description_file, 'r', encoding='utf-8'))

messages = [
    {
        "role": "system",
        "content": "你是一个自然语言分析大师，你需要根据数据库表信息，仔细研读每个表的注意事项，里面包含表与表之间的关联关系。"
                   "随后根据问题，分析问题意图，并识别出问题中的实体，最后将问题关联的所有数据表以json数组的形式返回，数组中每个元素只包含数据库名和表名即可。"
                   "表信息如下：\n" + str(table_description)
    },
    {
        "role": "user",
        "content": "请根据问题，分析问题意图，并识别出问题中的实体，最后将问题关联的所有数据表以json数组的形式返回，数组中每个元素只包含数据库名和表名即可。"
                   "问题如下：\n" + questions[0]
    }
]

chat.set_message(messages)
print(chat.send_message())