from datasets import load_dataset

def get_dataset(config):
    if config['dataset_name'] == 'gsm8k':
        dataset = load_dataset(**config['dataset_kwargs'])
    else:
        raise NotImplementedError
    
    return dataset