import json

file = open('results/phi-2/mmlu/humanities/pretrained__microsoft__phi-2,parallelize__True_mmlu_flan_cot_fewshot_formal_logic.jsonl')

data = json.load(file)

incorrect_solutions = ""

for test_case in data:
    if test_case['exact_match'] == 0.0:
        incorrect_solutions+= "Question: " + test_case['doc']['question'] + "\nChoices:\n" + '\n'.join(test_case['doc']['choices']) + "\nCorrect Answer: " + test_case['target'] + "\nGenerated Reasoning: " + test_case['resps'][0][0] + "\n\n\n" 

folder_path = "inference/mmlu/humanities/"
file_name = 'formal_logic.txt'

with open(f"{folder_path}{file_name}", 'w') as f:
    f.write(incorrect_solutions)
    f.close()