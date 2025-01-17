import os

from data_init import data_init

all_tables_schema_file_path = '../../data/all_tables_schema.txt'
data_dictionary_path = '../../data/数据字典.xlsx'
out_data_base_path = '../out/data/'
all_tables_schema_file = os.path.join(out_data_base_path, "all_tables_schema.json")

if __name__ == '__main__':
    # 数据初始化
    data_init(all_tables_schema_file_path, all_tables_schema_file, data_dictionary_path, out_data_base_path)
    # 意图分析和实体识别