from transformers import AutoModelForCausalLM, AutoTokenizer


def get_model(config):
    if config['model_name'] in ['microsoft/phi-2', 'stabilityai/stablelm-zephyr-3b', 'openlm-research/open_llama_3b_v2']:
        model = AutoModelForCausalLM.from_pretrained(**config['model_kwargs'])
        tokenizer = AutoTokenizer.from_pretrained(config['model_kwargs']['pretrained_model_name_or_path'])
    else:
        raise NotImplementedError
    
    if tokenizer.pad_token:
        pass
    elif tokenizer.unk_token:
        tokenizer.pad_token_id = tokenizer.unk_token_id
    elif tokenizer.eos_token:
        tokenizer.pad_token_id = tokenizer.eos_token_id
    else:
        raise ValueError("Unable to set the pad token for the model")
    
    return model, tokenizer