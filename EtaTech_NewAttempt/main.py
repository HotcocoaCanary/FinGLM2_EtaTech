import json
import os

from EtaTech_NewAttempt.tool.data_init import data_init
from EtaTech_NewAttempt.tool.sql_bulider import get_answer_data

all_tables_schema_file_path = '../data/all_tables_schema.txt'
data_dictionary_path = '../data/数据字典.xlsx'
out_data_base_path = 'out/data/'

# question_data_path = r'../../data/question.json'
question_data_path = r'../data/question_test.json'

if __name__ == '__main__':
    table_description_path, data_dict_path = data_init(all_tables_schema_file_path, data_dictionary_path, out_data_base_path)
    question = json.load(open(question_data_path, 'r', encoding='utf-8'))
    get_answer_data(question, table_description_path, data_dict_path)
