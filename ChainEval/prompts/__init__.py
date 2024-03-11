from prompts.src import *

def get_prompts(config):
    # returns the constant defined in the src
    if config['prompt_name'] == 'GSM8K_FEWSHOT':
        return GSM8K_FEWSHOT
    elif config['prompt_name'] == 'GSM8K_SOT':
        return GSM8K_SKELETON, GSM8K_REASONING, GSM8K_ANSWER
    elif config['prompt_name'] == 'BBH_FEWSHOT':
        return BBH_FEWSHOT[config['task_name']]
    else:
        raise NotImplementedError
    