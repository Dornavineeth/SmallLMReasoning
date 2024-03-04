import transformers
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    Iterator,
    List,
    Literal,
    Optional,
    Tuple,
    Type,
    Union,
)


def prompt_infilling_dataset(dataset, prompt):
    def infill(examples):
        inputs = []
        keys = list(examples.keys())
        for i in range(len(examples[keys[0]])):
            example = {k:examples[k][i] for k in keys}
            inputs.append(prompt.format(**example))
        examples.update({'input':inputs})
        return examples
    dataset = dataset.map(infill, batched=True)
    return dataset

def prompt_infilling_batch(batch, prompt):
    inputs = []
    keys = list(batch.keys())
    for i in range(len(batch[keys[0]])):
        example = {k:batch[k][i] for k in keys}
        inputs.append(prompt.format(**example))
    return inputs

def tok_batch_encode(
        strings,
        tokenizer,
        padding_side: str = "left",
        left_truncate_len: int = None,
        truncation: bool = False,
    ):
    # encode a batch of strings. converts to tensors and pads automatically, unlike tok_encode.
    old_padding_side = tokenizer.padding_side
    tokenizer.padding_side = padding_side
    encoding = tokenizer(
        strings,
        truncation=truncation,
        padding="longest",
        return_tensors="pt",
    )
    # TODO: handle differently for gemma models , we need ot add bos_token
    
    if left_truncate_len:
        encoding["input_ids"] = encoding["input_ids"][:, -left_truncate_len:]
        encoding["attention_mask"] = encoding["attention_mask"][
            :, -left_truncate_len:
        ]
    tokenizer.padding_side = old_padding_side

    return encoding["input_ids"], encoding["attention_mask"]


def tok_decode(tokens, tokenizer):
    return tokenizer.decode(tokens, skip_special_tokens=True)

class MultiTokenEOSCriteria(transformers.StoppingCriteria):
    """Criteria to stop on the specified multi-token sequence."""

    def __init__(
        self,
        sequence: str,
        tokenizer: transformers.PreTrainedTokenizer,
        initial_decoder_input_length: int,
        batch_size: int,
    ) -> None:
        self.initial_decoder_input_length = initial_decoder_input_length
        self.done_tracker = [False] * batch_size
        self.sequence = sequence
        self.sequence_ids = tokenizer.encode(sequence, add_special_tokens=False)
        # print(sequence, self.sequence_ids)
        # we look back for 2 more tokens than it takes to encode our stop sequence
        # because tokenizers suck, and a model might generate `['\n', '\n']` but our `sequence` is `['\n\n']`
        # and we don't want to mistakenly not stop a generation because our
        # (string) stop sequence was output in a different tokenization

        # NOTE: there is a minor danger that this will end up looking back 2 tokens into the past, into the inputs to the model,
        # and stopping generation immediately as a result. With only 2 extra tokens of lookback, this risk is minimized
        # Additionally, in lookback_ids_batch we should prevent ever looking back into the inputs as described.
        self.sequence_id_len = len(self.sequence_ids) + 2
        self.tokenizer = tokenizer

    def __call__(self, input_ids, scores, **kwargs) -> bool:
        # For efficiency, we compare the last n tokens where n is the number of tokens in the stop_sequence
        lookback_ids_batch = input_ids[:, self.initial_decoder_input_length :]

        lookback_ids_batch = lookback_ids_batch[:, -self.sequence_id_len :]

        lookback_tokens_batch = self.tokenizer.batch_decode(lookback_ids_batch)

        for i, done in enumerate(self.done_tracker):
            if not done:
                self.done_tracker[i] = self.sequence in lookback_tokens_batch[i]
        return False not in self.done_tracker


def stop_sequences_criteria(
    tokenizer: transformers.PreTrainedTokenizer,
    stop_sequences: List[str],
    initial_decoder_input_length: int,
    batch_size: int,
) -> transformers.StoppingCriteriaList:
    return transformers.StoppingCriteriaList(
        [
            *[
                MultiTokenEOSCriteria(
                    sequence, tokenizer, initial_decoder_input_length, batch_size
                )
                for sequence in stop_sequences
            ],
        ]
    )