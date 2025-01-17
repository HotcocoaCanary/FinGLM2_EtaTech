import json
import os

import pandas as pd


def data_init(all_tables_schema_file_path, all_tables_schema_file, data_dictionary_path, out_data_base_path):
    table_schemas = []
    current_table = None

    with open(all_tables_schema_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if '----------------------' in line or line == '' or '列名' in line:
                continue
            if '===' in line:
                if current_table is not None:
                    table_schemas.append(current_table)
                current_table = {"name": line.strip().split()[1], "schemas": []}
            else:
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

    if current_table is not None:
        table_schemas.append(current_table)
    with open(all_tables_schema_file, 'w', encoding='utf-8') as f:
        json.dump(table_schemas, f, ensure_ascii=False, indent=4)


    data_dict_path = os.path.join(out_data_base_path, 'data_dictionary')
    table_description_path = os.path.join(out_data_base_path, 'table_description.json')

    df1 = pd.read_excel(data_dictionary_path, sheet_name='库表关系').fillna(0).to_dict(orient='records')
    df2 = pd.read_excel(data_dictionary_path, sheet_name='表字段信息').fillna(0).to_dict(orient='records')

    table_description = []
    data_dictionary=[]

    for schema_i in df1:
        schema = schema_i['库名英文']
        table = []
        if not any(d['数据库'] == schema for d in data_dictionary):
            table = []
        else:
            for data_dictionary_i in data_dictionary:
                if data_dictionary_i['数据库'] == schema:
                    table = data_dictionary_i['表']
        for table_i in df1:
            if table_i['库名英文'] == schema:
                table_name = table_i['表英文']
                state = table_i['表描述']+"\n"
                description = ""
                column = []
                for column_i in df2:
                    if column_i['table_name'] == table_name:
                        if column_i['注释'] != 0:
                            description += column_i['column_description'] + '('+ column_i['column_name'] +"): " + column_i['注释'] + '\n'
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

    os.makedirs(data_dict_path, exist_ok=True)
    for data_dict in data_dictionary:
        file_path = os.path.join(data_dict_path, f"{data_dict['数据库']}.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, ensure_ascii=False, indent=4)

    os.makedirs(os.path.dirname(table_description_path), exist_ok=True)
    with open(table_description_path, 'w', encoding='utf-8') as f:
        json.dump(table_description, f, ensure_ascii=False, indent=4)

# if __name__ == "__main__":
#     all_tables_schema_file_path = '../../data/all_tables_schema.txt'
#     all_tables_schema_file = '../out/data/all_tables_schema.json'
#     data_dictionary_path = '../../data/数据字典.xlsx'
#     out_data_base_path = '../out/data/'
#     data_init(all_tables_schema_file_path, all_tables_schema_file, data_dictionary_path, out_data_base_path)