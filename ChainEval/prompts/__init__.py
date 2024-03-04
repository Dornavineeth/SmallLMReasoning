from prompts.src import *

def get_prompts(config):
    if config['prompt_name'] == 'GSM8K_FEWSHOT':
        return GSM8K_FEWSHOT
    else:
        raise NotImplementedError
    