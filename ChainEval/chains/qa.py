from models import get_model
from dataset import get_dataset
from prompts import get_prompts
from util import seed_everything, load_config, prompt_infilling_batch, tok_batch_encode, stop_sequences_criteria, tok_decode, save_json

from tqdm import tqdm
from argparse import ArgumentParser
from torch.utils.data import DataLoader

def main(config):
    model, tokenizer = get_model(config['model_config'])
    dataset = get_dataset(config['dataset_config'])
    prompt = get_prompts(config['prompt_config'])
    
    limit = config.get('limit', None)
    if limit:
        dataset = dataset.select(range(limit))
    data_loader = DataLoader(dataset, batch_size=config['batch_size'], shuffle=False)
    left_truncate_len = config.get('left_truncate_len', None)
    padding_side = config.get('padding_side', 'left')
    truncation = config.get('truncation', False)
    generation_kwargs = config.get('generation_kwargs')
    until = config.get('until', [])
    device = config.get('device')
    results = []
    for batch in tqdm(data_loader):
        inputs = prompt_infilling_batch(batch, prompt)
        input_ids, attention_mask = tok_batch_encode(inputs, tokenizer, padding_side, left_truncate_len, truncation)
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
        batch.update({'input':inputs, 'response':res})
        res = [{k: v[i] for k, v in batch.items()} for i in range(len(list(batch.values())[0]))]
        results += res
    
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
    main(config)
