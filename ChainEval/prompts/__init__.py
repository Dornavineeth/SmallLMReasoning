from prompts.src import *

def get_prompts(config):
    if config['prompt_name'] == 'GSM8K_SOT':
        # returns the constant defined in the src file for GSM8K
        return GSM8K_SKELETON, GSM8K_REASONING, GSM8K_ANSWER
    else:
        raise NotImplementedError
    