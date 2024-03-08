from datasets import load_dataset

def get_dataset(config):
    if config['dataset_name'] == 'gsm8k':
        # Loading the hugging face dataset
        dataset = load_dataset(**config['dataset_kwargs'])
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