from transformers import AutoModelForCausalLM, AutoTokenizer


def get_model(config):
    # Check if the model name is in the predefined list or not
    if config['model_name'] in ['microsoft/phi-2', 'stabilityai/stablelm-zephyr-3b', 'openlm-research/open_llama_3b_v2']:
        model = AutoModelForCausalLM.from_pretrained(**config['model_kwargs'])
        tokenizer = AutoTokenizer.from_pretrained(config['model_kwargs']['pretrained_model_name_or_path'])
    else:
        raise NotImplementedError
    
    # Setting the padding token for tokenizer (has to be done manually - not taken care by Hugging face library)
    if tokenizer.pad_token:
        pass
    elif tokenizer.unk_token:
        tokenizer.pad_token_id = tokenizer.unk_token_id
    elif tokenizer.eos_token:
        tokenizer.pad_token_id = tokenizer.eos_token_id
    else:
        raise ValueError("Unable to set the pad token for the model")
    
    # returns model and the tokenizer
    return model, tokenizer