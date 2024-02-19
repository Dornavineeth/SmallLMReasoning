import json
import os

for file_name in os.listdir('results/phi-2/mmlu/humanities/'):
    if file_name == 'results.json':
        continue
    folder_path = "inference/mmlu/humanities/"
    end_idx = file_name.index('.jsonl')
    inference_file_name = file_name[69:end_idx] + '.txt'
    file = open(f'results/phi-2/mmlu/humanities/{file_name}')

    data = json.load(file)

    incorrect_solutions = ""

    for test_case in data:
        if test_case['exact_match'] == 0.0:
            incorrect_solutions+= "Question: " + test_case['doc']['question'] + "\nChoices:\n" + '\n'.join(test_case['doc']['choices']) + "\nCorrect Answer: " + test_case['target'] + "\nGenerated Reasoning: " + test_case['resps'][0][0] + "\n\n\n" 

    with open(f"{folder_path}{inference_file_name}", 'w') as f:
        f.write(incorrect_solutions)
        f.close()