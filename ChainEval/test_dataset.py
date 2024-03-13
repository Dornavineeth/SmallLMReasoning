from dataset import get_dataset
from util import seed_everything, load_config, prompt_infilling_batch, tok_batch_encode, stop_sequences_criteria, tok_decode, save_json, collate_fn

from tqdm import tqdm
from argparse import ArgumentParser
from torch.utils.data import DataLoader

def main(config):
    dataset = get_dataset(config['dataset_config'])
    # limit = config.get('limit', None)
    # if limit:
    #     dataset = dataset.select(range(limit))
    data_loader = DataLoader(dataset, batch_size=config['batch_size'], shuffle=False, collate_fn= collate_fn)
    for batch in tqdm(data_loader):
        print(batch.keys())
        print(batch)
        break


def parse_args():
    parser = ArgumentParser(description='Simple : Question Answer Chain')
    parser.add_argument('--config', type=str, required=True)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    config = load_config(args.config)
    seed_everything(config.get('seed', 0))
    main(config)