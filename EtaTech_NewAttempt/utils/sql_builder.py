import json
import pandas as pd


class SQLBuilder:
    def __init__(self, data_dict_path, all_tables_schema_path, llm_chat, db_tool):
        self.data_dict_path = data_dict_path
        self.all_tables_schema_path = all_tables_schema_path
        self.db_table, self.data_dict = self.data_dict_init()
        self.llm_chat = llm_chat
        self.db_tool = db_tool

    # 数据字典初始化
    def data_dict_init(self):
        """
        data_dict_path是Excel表格形式的数据字典路径，里面包含两个表，
        一个是库表关系，包含库名中文，库名英文，表英文，表中文，表描述这几个字段
        另一个是表字段信息，包含table_name，column_name，column_description，注释，Annotation这几个字段
        提取出库表关系表中的库名英文，表英文，组装成新的数据表名称，用于后续sql语句的构建，同时针对数据表保留对应的表描述
        在上述基础上为每个表添加对应的字段信息，用于后续sql语句的构建，同时保留对应的字段描述（如果存在字段描述的话）
        :return: data_dict，一个列表，包含库表关系表中的库名英文，表英文，组装成新的数据表名称，用于后续sql语句的构建，同时保留对应的表描述
        """
        db_table = []
        data_dict = []
        # 读取Excel文件
        table_relation = pd.read_excel(self.data_dict_path, sheet_name='库表关系')
        table_info = pd.read_excel(self.data_dict_path, sheet_name='表字段信息')
        for i in range(len(table_relation)):
            table_name = table_relation.loc[i, '库名英文'] + '.' + table_relation.loc[i, '表英文']
            table_description = table_relation.loc[i, '表描述']
            # 添加表字段信息
            table_column = []
            for j in range(len(table_info)):
                if table_info.loc[j, 'table_name'] == table_relation.loc[i, '表英文']:  # 如果表名相同，则添加字段信息
                    column = {'column_name': table_info.loc[j, 'column_name']}
                    if pd.notnull(table_info.loc[j, 'column_description']):  # 如果字段描述不为空，则添加字段描述
                        column['column_description'] = table_info.loc[j, 'column_description']
                    if pd.notnull(table_info.loc[j, '注释']):  # 如果注释不为空，则添加注释
                        column['注释'] = table_info.loc[j, '注释']
                    table_column.append(column)
            db_table.append({'table_name': table_name, 'table_description': table_description})
            data_dict.append({'table_name': table_name, 'table_description': table_description, 'table_column': table_column})
        # 以json格式保存数据字典
        with open('out/data_dict.json', 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, ensure_ascii=False, indent=4)
        return db_table, data_dict

    # 构建sql语句
    def get_sql_list(self, question):
        # 确定数据表
        table_name_list = self.get_table_name(question)
        # 确定数据表字段
        sql_list = self.build_sql(question, table_name_list)
        return sql_list

    def get_table_name(self, question):
        # 确定数据表
        self.llm_chat.set_message([
            {
                'role': 'system',
                'content': "请从数据表描述中中确定数据表名称，返回格式为json数组，数据表描述将以json数组格式给你，根据每一个对象的table_description属性判断问题所闻数据来源于可能那个数据表，给出所有可能的表的table_name属性值，并使用json数组形式返回，例如：[\"astockbasicinfodb.lc_business\"]"+"\n"
                           "数据表描述："+str(self.db_table)
            },
            {
                'role': 'user',
                'content': "问题如下：\n"+question+"根据数据表描述给我当前问题可能使用到的数据表名称，返回格式为json数组，例如：['astockbasicinfodb.lc_business']"
            }
        ])
        return self.llm_chat.send_message()

    def build_sql(self, question, table_name_list):
        # 确定数据表字段
        table_schema = []
        for table in self.data_dict:
            if table['table_name'] in table_name_list:
                table_schema.append(table)
        self.llm_chat.set_message([
            {
                'role': 'system',
                'content': "请根据所提供的数据字典，对当前问题进行实体提取，数据字典"+str(table_schema)
            }
        ])




