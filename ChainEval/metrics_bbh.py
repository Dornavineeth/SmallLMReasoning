import json
import os

metrics = 0
count = 0

BASE_DIR = 'results/zephyr/bbh/'

# BBH Score
for task_folder in os.listdir(BASE_DIR):
    f = open(f"{BASE_DIR}{task_folder}/metrics.json")
    metrics+= json.load(f)['exact_match']    
    count+=1

# Tasks with below average performance
for task_folder in os.listdir(BASE_DIR):
    f = open(f"{BASE_DIR}{task_folder}/metrics.json")
    match = json.load(f)['exact_match']
    if match>0.25 and match<0.5:
        print(task_folder, match)