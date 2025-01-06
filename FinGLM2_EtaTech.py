# coding=utf-8
from utils.recall_tool import RecallTool
from utils.db_tool import DBTool
from utils.chat_tool import ChatTool

# 1.初始化工具
access_token = 'e904a3cadd95478296e90c6bb954f614'
model = "glm-4-air"
api_key = '2f252bef2ec446719359d4457574fee1.JOfVYlXzamOs2Qwc'
question_data_path = r'data/question.json'
data_dictionary_path = 'data/数据字典.xlsx'
all_tables_schema_file_path = 'data/all_tables_schema.txt'
out_file_path = 'out/EtaTech_result.json'

db_tool = DBTool(access_token)
chat_tool = ChatTool(api_key, model)
recall_tool = RecallTool(chat_tool, data_dictionary_path, all_tables_schema_file_path)

# 2.表格召回
sql_list = recall_tool.recall_db("600872的全称、A股简称、法人、法律顾问、会计师事务所及董秘是？")

# 3.执行SQL
data = []
for sql in sql_list:
    result = db_tool.execute_sql(sql)
    data.append(result)
# 4.生成答案
question = "600872的全称、A股简称、法人、法律顾问、会计师事务所及董秘是？"
answer = chat_tool.set_message(
    messages=[
        {
            "role": "system",
            "content": "你是一个金融专家，请根据以下数据回答问题："
        },
        {
            "role": "user",
            "content": "请根据以下数据回答问题：\n" + str(data) + "\n问题："+question
        }
    ]
)
print(chat_tool.send_message())
