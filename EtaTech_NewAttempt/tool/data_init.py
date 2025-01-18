import json
import os

import pandas as pd


def data_init(all_tables_schema_file_path, data_dictionary_path, out_data_base_path):
    """
    初始化数据，包括读取表结构文件和数据字典文件，生成表描述和表结构信息。

    参数:
    all_tables_schema_file_path (str): 表结构文件的路径。
    data_dictionary_path (str): 数据字典文件的路径。
    out_data_base_path (str): 输出数据文件的路径。

    返回:
    tuple: 包含表描述文件路径和数据字典文件路径的元组。
    """

    # 构建表结构文件的完整路径
    all_tables_schema_file = os.path.join(out_data_base_path, "all_tables_schema.json")
    table_schemas = []
    current_table = None

    # 读取表结构文件
    with open(all_tables_schema_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # 跳过分隔线和空行以及包含“列名”的行
            if '----------------------' in line or line == '' or '列名' in line:
                continue
            # 标识新表的开始
            if '===' in line:
                if current_table is not None:
                    table_schemas.append(current_table)
                current_table = {"name": line.strip().split()[1], "schemas": []}
            else:
                # 解析表结构信息
                row = line.split()
                if current_table is not None and len(row) >= 3:
                    column_name = row[0].strip()
                    column_annotation = row[1].strip()
                    column_sample = ' '.join(row[2:]).strip()
                    current_table['schemas'].append({
                        "列名": column_name,
                        "注释": column_annotation,
                        "数据示例": column_sample
                    })

    # 添加最后一个表
    if current_table is not None:
        table_schemas.append(current_table)

    # 将表结构信息保存到文件
    with open(all_tables_schema_file, 'w', encoding='utf-8') as f:
        json.dump(table_schemas, f, ensure_ascii=False, indent=4)

    # 构建数据字典路径和表描述文件路径
    data_dict_path = os.path.join(out_data_base_path, 'data_dictionary')
    table_description_path = os.path.join(out_data_base_path, 'table_description.json')

    # 读取数据字典文件中的库表关系和表字段信息
    df1 = pd.read_excel(data_dictionary_path, sheet_name='库表关系').fillna(0).to_dict(orient='records')
    df2 = pd.read_excel(data_dictionary_path, sheet_name='表字段信息').fillna(0).to_dict(orient='records')

    table_description = []
    data_dictionary = []

    # 遍历库表关系数据
    for schema_i in df1:
        schema = schema_i['库名英文']
        table = []
        # 检查数据字典中是否包含当前数据库
        if not any(d['数据库'] == schema for d in data_dictionary):
            table = []
        else:
            for data_dictionary_i in data_dictionary:
                if data_dictionary_i['数据库'] == schema:
                    table = data_dictionary_i['表']
        # 遍历库表关系数据，生成表描述
        for table_i in df1:
            if table_i['库名英文'] == schema:
                table_name = table_i['表英文']
                state = table_i['表描述'] + "\n"
                description = ""
                column = []
                # 遍历表字段信息，生成列描述
                for column_i in df2:
                    if column_i['table_name'] == table_name:
                        if column_i['注释'] != 0:
                            description += column_i['column_description'] + '(' + column_i['column_name'] + "): " + column_i['注释'] + '\n'
                        # 查找表结构信息中的列数据示例
                        for table_schemas_i in table_schemas:
                            if table_schemas_i['name'].lower() == (schema + "." + table_name).lower():
                                for column_schemas_i in table_schemas_i['schemas']:
                                    if column_schemas_i['列名'] == column_i['column_name']:
                                        column_sample = column_schemas_i['数据示例']
                                        column.append(
                                            {
                                                "列名": column_i['column_name'],
                                                "列注释": column_i['column_description'],
                                                "列数据示例": column_sample
                                            }
                                        )
                table_description.append({
                    "数据库名": schema,
                    "表名": table_name,
                    "表描述": state,
                    "注意事项": description
                })
                table.append({
                    "表名": table_name,
                    "列": column
                })
        data_dictionary.append({
            "数据库": schema,
            "表": table
        })

    # 创建数据字典目录
    os.makedirs(data_dict_path, exist_ok=True)
    # 将数据字典保存到文件
    for data_dict in data_dictionary:
        file_path = os.path.join(data_dict_path, f"{data_dict['数据库']}.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, ensure_ascii=False, indent=4)

    # 创建表描述文件目录
    os.makedirs(os.path.dirname(table_description_path), exist_ok=True)
    # 将表描述保存到文件
    with open(table_description_path, 'w', encoding='utf-8') as f:
        json.dump(table_description, f, ensure_ascii=False, indent=4)

    # 返回表描述文件路径和数据字典文件路径
    return table_description_path, data_dict_path

# if __name__ == "__main__":
#     all_tables_schema_file_path = '../../data/all_tables_schema.txt'
#     all_tables_schema_file = '../out/data/all_tables_schema.json'
#     data_dictionary_path = '../../data/数据字典.xlsx'
#     out_data_base_path = '../out/data/'
#     data_init(all_tables_schema_file_path, all_tables_schema_file, data_dictionary_path, out_data_base_path)