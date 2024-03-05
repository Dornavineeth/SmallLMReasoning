from models import get_model
from dataset import get_dataset
from prompts import get_prompts
from util import seed_everything, load_config, prompt_infilling_batch_skeleton, prompt_infilling_batch_reasoning, prompt_infilling_batch_answer, tok_batch_encode, stop_sequences_criteria, tok_decode, save_json

from tqdm import tqdm
from argparse import ArgumentParser
from torch.utils.data import DataLoader
# Passing the YAML config file as an input
def main(config):
    # Loading the model and the tokenizer
    model, tokenizer = get_model(config['model_config'])
    # Load the dataset - a list of dictionary - question and answer pairs
    dataset = get_dataset(config['dataset_config'])
    # Having prompts defined for the model input 
    skeleton_prompt, reasoning_prompt, answer_prompt = get_prompts(config['prompt_config'])
    
    limit = config.get('limit', None)
    if limit:
        # If there is a limit, we select top n questions from the dataset
        dataset = dataset.select(range(limit))
    # Loading the question answer pairs from the dataset
    data_loader = DataLoader(dataset, batch_size=config['batch_size'], shuffle=False)
    # Padding and truncation
    left_truncate_len = config.get('left_truncate_len', None)
    padding_side = config.get('padding_side', 'left')
    truncation = config.get('truncation', False)
    # Get all the different parameters used in model.generate() function
    generation_kwargs = config.get('generation_kwargs')
    # These are the list of tokens that stops further generation when encountered 
    until = config.get('until', [])
    # CPU/GPU
    device = config.get('device')
    results = []
    # a batch is generated. It is a dictionary having question and answer as keys, and corresponding values as a list
    for batch in tqdm(data_loader):
        # Replacing the variables with actual values/questions in prompt
        inputs = prompt_infilling_batch_skeleton(batch, skeleton_prompt)
        # Tokenizing the input
        input_ids, attention_mask = tok_batch_encode(inputs, tokenizer, padding_side, left_truncate_len, truncation)
        # Create a stopping criteria - stop generation once encounters a token specified in the list
        stopping_criteria = stop_sequences_criteria(
            tokenizer, until, input_ids.shape[1], input_ids.shape[0]
        )

        # Generating tokens
        output = model.generate(
            input_ids=input_ids.to(device),
            attention_mask=attention_mask.to(device),
            stopping_criteria=stopping_criteria,
            pad_token_id=tokenizer.pad_token_id,
            use_cache=True,
            **generation_kwargs,
        )
        out_toks_list = output.tolist()

        
        res = []
        for cont_toks in out_toks_list:
            # Extracting the generation
            cont_toks = cont_toks[input_ids.shape[1] :]
            s = tok_decode(cont_toks, tokenizer)
            # Spltting at points where the stopping tokens occur
            for term in until:
                if len(term) > 0:
                    s = s.split(term)[0]
            res.append(s)
        batch.update({'input_skeleton': inputs,'skeleton':res})

        # Done skeleton generation, now starting with reasoning
        reasoning_inputs = prompt_infilling_batch_reasoning(batch, reasoning_prompt)
        input_ids, attention_mask = tok_batch_encode(reasoning_inputs, tokenizer, padding_side, left_truncate_len, truncation)
        stopping_criteria = stop_sequences_criteria(
            tokenizer, until, input_ids.shape[1], input_ids.shape[0]
        )
        output = model.generate(
            input_ids=input_ids.to(device),
            attention_mask=attention_mask.to(device),
            stopping_criteria=stopping_criteria,
            pad_token_id=tokenizer.pad_token_id,
            use_cache=True,
            **generation_kwargs,
        )
        out_toks_list = output.tolist()
        res = []
        for cont_toks in out_toks_list:
            cont_toks = cont_toks[input_ids.shape[1] :]
            s = tok_decode(cont_toks, tokenizer)
            for term in until:
                if len(term) > 0:
                    s = s.split(term)[0]
            res.append(s)
        batch.update({'inputs_reasoning': reasoning_inputs,'reasoning':res})

        # Done with reasoning generation, now starting answer extraction
        answer_inputs = prompt_infilling_batch_answer(batch, answer_prompt)
        input_ids, attention_mask = tok_batch_encode(answer_inputs, tokenizer, padding_side, left_truncate_len, truncation)
        stopping_criteria = stop_sequences_criteria(
            tokenizer, until, input_ids.shape[1], input_ids.shape[0]
        )
        output = model.generate(
            input_ids=input_ids.to(device),
            attention_mask=attention_mask.to(device),
            stopping_criteria=stopping_criteria,
            pad_token_id=tokenizer.pad_token_id,
            use_cache=True,
            **generation_kwargs,
        )
        out_toks_list = output.tolist()
        res = []
        for cont_toks in out_toks_list:
            cont_toks = cont_toks[input_ids.shape[1] :]
            s = tok_decode(cont_toks, tokenizer)
            for term in until:
                if len(term) > 0:
                    s = s.split(term)[0]
            res.append(s)
        batch.update({'input_ans': answer_inputs ,'prediction':res})

        res = [{k: v[i] for k, v in batch.items()} for i in range(len(list(batch.values())[0]))]
        results += res
    # TODO: Resolve issues in reasoning and answer extraction where only one token is being generated. 
    results_fn = config['results_fn']
    # Write the list to a JSON file
    save_json(results, results_fn)
    

def parse_args():
    parser = ArgumentParser(description='Simple : Question Answer Chain')
    parser.add_argument('--config', type=str, required=True)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    config = load_config(args.config)
    seed_everything(config.get('seed', 0))
    # Calling the main function
    main(config)
