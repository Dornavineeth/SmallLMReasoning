import json
import os

metrics = 0
count = 0

BASE_DIR = 'results/zephyr/bbh/'
for task_folder in os.listdir(BASE_DIR):
    f = open(f"{BASE_DIR}{task_folder}/metrics.json")
    metrics+= json.load(f)['exact_match']    
    count+=1

print(metrics/count)