from utils.rw_json import process_questions

input_filename = "../data/question_test.json"
output_filename = "out/EtaTech_result.json"

if __name__ == "__main__":
    process_questions(input_filename, output_filename)