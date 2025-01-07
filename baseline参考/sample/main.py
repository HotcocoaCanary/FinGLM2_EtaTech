import argparse
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from utils import call_large_model


def process_question_with_llm(question, api_key, model, thread_id):
    """
    Call large model to generate answer field for each question.
    :param question: dictionary object containing question data
    :param api_key: API key for large model
    :param model: name of the large model to use
    :param thread_id: current thread number (for debugging)
    :return: question dictionary containing answer field
    """
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Please generate a random number between 1 and 10. output with english number likes 'one','two', only without other word.",
        },
    ]
    random_number = call_large_model(messages, api_key=api_key, model=model, temperature=1.0, max_tokens=1024)
    question["answer"] = f"Thread {thread_id} generated: {random_number}" if random_number else "LLM failed"
    return question


def process_team_with_llm(team, api_key, model, thread_id):
    """
    Process all questions in team, call large model to generate answer.
    :param team: list containing questions
    :param api_key: API key for large model
    :param model: name of the large model to use
    :param thread_id: current thread number
    :return: processed team list
    """
    return [process_question_with_llm(q, api_key, model, thread_id) for q in team]


def process_task_with_llm(task, api_key, model, thread_id):
    """
    Process a single task, call large model to generate answer.
    :param task: dictionary containing team
    :param api_key: API key for large model
    :param model: name of the large model to use
    :param thread_id: current thread number
    :return: processed task dictionary

    """
    task["team"] = process_team_with_llm(task["team"], api_key, model, thread_id)
    return task


def main():
    input = "data/question_en.json"
    output = "out/EtaTech_result.json"
    access_token = 'e904a3cadd95478296e90c6bb954f614'
    model = "glm-4-air"
    api_key = '2f252bef2ec446719359d4457574fee1.JOfVYlXzamOs2Qwc'
    threads = 4

    with open(input, "r", encoding="utf-8") as infile:
        tasks = json.load(infile)

    results = []
    total_questions = sum(len(task["team"]) for task in tasks)
    os.makedirs(os.path.dirname(output), exist_ok=True)
    with tqdm(total=total_questions, desc="Processing Questions", unit="question") as pbar:
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            for idx, task in enumerate(tasks):
                futures.append(
                    executor.submit(process_task_with_llm, task, api_key, model, idx % threads)
                )

            for future in as_completed(futures):
                results.append(future.result())
                pbar.update(sum(len(task["team"]) for task in results[-1:]))

    with open(output, "w", encoding="utf-8") as outfile:
        json.dump(results, outfile, ensure_ascii=False, indent=4)

    print(f"Processing completed. Results saved to {output}")


if __name__ == "__main__":
    main()
