import json

from 最初版本.utils.answer_tool import get_answer


def process_questions(input_filename, output_filename):
    """
    读取问题列表，为每个问题添加答案，并将结果保存到新的JSON文件。
    """
    try:
        # 读取JSON数据
        with open(input_filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []  # 如果文件不存在，则初始化为空列表

    # 遍历每个问题并添加答案
    for team in data:
        try:
            # 检查team_json中的问题是否有答案
            team_json = team["team"]
            check = all("answer" in question and question["answer"] != "" for question in team_json)
            if not check:
                team["team"] = get_answer(team["team"])
        except Exception as e:
            print(f"处理团队 {team['tid']} 时出错: {e}")

    # 将修改后的JSON数据保存到文件中
    with open(output_filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    print(f"问题答案已保存{output_filename}")