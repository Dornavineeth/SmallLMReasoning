from datasets import load_dataset, Dataset
import requests, json

def get_dataset(config):
    if config['dataset_name'] == 'gsm8k':
        # Loading the hugging face dataset
        dataset = load_dataset(**config['dataset_kwargs'])
    elif config['dataset_name'] == 'bbh':
        dataset = []
        # Extract the sub-task name
        task = config['dataset_kwargs']['name']
        # Link to the JSON files
        BASE_URL = "https://github.com/suzgunmirac/BIG-Bench-Hard/raw/main/bbh/"
        # Load the JSON files 
        loaded_dataset = json.loads(requests.get(f"{BASE_URL}{task}.json").text)
        # Extract the question and answers from the file
        loaded_dataset = loaded_dataset["examples"]
        for item in loaded_dataset:
            pair = {'question': item['input'], 'answer': item['target']}
            dataset.append(pair)
        # Create a dataset from the list of dictionaries
        dataset = Dataset.from_list(dataset)
    else:
        raise NotImplementedError
    # return the loaded dataset (stored in cache)
    numbered_dataset = dataset.map(add_numbering, with_indices=True)
    return numbered_dataset
    

def add_numbering(example, idx):
    example_new = {}
    example_new['doc_id'] = idx
    example_new.update(example)
    return example_new