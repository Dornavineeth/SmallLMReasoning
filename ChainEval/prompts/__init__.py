from prompts.src import *

def get_prompts(config):
    # returns the constant defined in the src
    if config['prompt_name'] == 'GSM8K_COT_FEWSHOT':
        return GSM8K_COT_FEWSHOT
    if config['prompt_name'] == 'GSM8K_COT_STEP_FEWSHOT':
        return GSM8K_COT_STEP_FEWSHOT
    elif config['prompt_name'] == 'GSM8K_SOT':
        return GSM8K_SKELETON, GSM8K_REASONING, GSM8K_ANSWER
    elif config['prompt_name'] == 'BBH_COT_FEWSHOT':
        return BBH_COT_FEWSHOT[config['task_name']]
    elif config['prompt_name'] == 'BBH_SOT_FEWSHOT':
        return BBH_SKELETON[config['task_name']], BBH_REASONING[config['task_name']], BBH_ANSWER[config['task_name']] 
    else:
        raise NotImplementedError
    