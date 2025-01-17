import json

import pandas as pd


class RecallTool:
    def __init__(self, chat_tool, data_dictionary_path, all_tables_schema_path):
        self.chat_tool = chat_tool

        df1 = pd.read_excel(data_dictionary_path, sheet_name='库表关系').to_dict(orient='records')
        df2 = pd.read_excel(data_dictionary_path, sheet_name='表字段信息').to_dict(orient='records')
        db_table = []
        table_field = []
        for i in df1:
            db_table.append(
                {
                    "table_name": i['库名英文'] + '.' + i['表英文'],
                    "description": i['表描述']
                })
        for i in df2:
            for j in df1:
                if i['table_name'] == j['表英文']:
                    i['table_name'] = j['库名英文'] + '.' + i['table_name']
        for i in df2:
            table_field.append(
                {
                    "table_name": i['table_name'],
                    "column_name": i['column_name'],
                    "column_name_zh": i['column_description'],
                    "description": i['注释']
                })
        self.db_table = db_table
        self.table_field = table_field

        all_tables_schema = open(all_tables_schema_path, 'r', encoding='utf-8')
        self.all_tables_schema = all_tables_schema.read()
        all_tables_schema.close()

    def recall_db(self, question):
        answer = self.recall_db_table(question)
        tables = self.format_json(answer)
        MAX_TIME = 3
        while tables == "答案中未包含" and MAX_TIME > 0:
            answer = self.recall_db_table(question)
            tables = self.format_json(answer)
            MAX_TIME -= 1
        sql = self.recall_table_field(question, tables)
        return sql

    def recall_db_table(self, question):
        self.chat_tool.set_message([
            {
                "role": "system",
                "content": "接下来需要你完成数据召回任务。\n"
                           "数据如下："+ str(self.db_table)+"\n"
                           "提供的数据包含table_name和description两个字段，根据description的描述判断所问问题用到了哪些table_name，并用json数组数据的形式给出那些table_name的值。"
            },
            {
                "role": "user",
                "content": question
            }
        ])
        answer = self.chat_tool.send_message()
        return answer.choices[0].message.content

    def format_json(self, answer):
        try:
            match = answer.split("```json")[1].split("```")[0]
            answer_json = json.loads(match)
            return answer_json
        except Exception:
            return "答案中未包含"

    def format_sql(self, sql_text):
        import re
        pattern = r"```sql(.*?)```"
        matches = re.findall(pattern, sql_text, re.DOTALL)
        # 去掉以--开头的注释
        matches = [match for match in matches if not match.startswith("--")]
        # 去掉空行和换行符
        matches = [match.strip() for match in matches]
        # 将所有\n替换为空格
        matches = [match.replace("\n", " ") for match in matches]
        return matches


    def recall_table_field(self, question, tables):
        tables_data = []
        for table in tables:
            new_table = {'table_name': table}
            for i in self.table_field:
                if i['table_name'] == table:
                    new_table['column_name'] = i['column_name']
                    new_table['description'] = i['description']
                    tables_data.append(new_table)
        self.chat_tool.set_message([
            {
                "role": "system",
                "content": "接下来需要你完成实体提取并生成SQL语句组任务。\n"
                           "数据库全貌："+self.all_tables_schema+"\n"
                           "提供的数据包含table_name、column_name、column_name_zh和description四个字段，提取所问问题中包含的实体进行SQL语句生成，查询时使用的表名使用table_name（数据库名.表名），尽量不要使用多表查询，可以生成多个带有先后顺序的SQL查询语句（不要有任何注释），以MarkDown形式给出生成的SQL语句组"
                           "问题关联数据如下："+ str(tables_data)
            },
            {
                "role": "user",
                "content": question
            }
        ])
        answer = self.chat_tool.send_message()
        return answer.choices[0].message.content
