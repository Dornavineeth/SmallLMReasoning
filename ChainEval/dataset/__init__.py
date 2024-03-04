from datasets import load_dataset

def get_dataset(config):
    if config['dataset_name'] == 'gsm8k':
        # Loading the hugging face dataset
        dataset = load_dataset(**config['dataset_kwargs'])
    else:
        raise NotImplementedError
    # return the loaded dataset (stored in cache)
    return dataset