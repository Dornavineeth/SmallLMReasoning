from langchain.prompts.prompt import PromptTemplate
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch 

examples = [
    {
        "question": "Who lived longer, Muhammad Ali or Alan Turing?",
        "answer": """
Are follow up questions needed here: Yes.
Follow up: How old was Muhammad Ali when he died?
Intermediate answer: Muhammad Ali was 74 years old when he died.
Follow up: How old was Alan Turing when he died?
Intermediate answer: Alan Turing was 41 years old when he died.
So the final answer is: Muhammad Ali
""",
    },
    {
        "question": "When was the founder of craigslist born?",
        "answer": """
Are follow up questions needed here: Yes.
Follow up: Who was the founder of craigslist?
Intermediate answer: Craigslist was founded by Craig Newmark.
Follow up: When was Craig Newmark born?
Intermediate answer: Craig Newmark was born on December 6, 1952.
So the final answer is: December 6, 1952
""",
    },
    {
        "question": "Who was the maternal grandfather of George Washington?",
        "answer": """
Are follow up questions needed here: Yes.
Follow up: Who was the mother of George Washington?
Intermediate answer: The mother of George Washington was Mary Ball Washington.
Follow up: Who was the father of Mary Ball Washington?
Intermediate answer: The father of Mary Ball Washington was Joseph Ball.
So the final answer is: Joseph Ball
""",
    },
    {
        "question": "Are both the directors of Jaws and Casino Royale from the same country?",
        "answer": """
Are follow up questions needed here: Yes.
Follow up: Who is the director of Jaws?
Intermediate Answer: The director of Jaws is Steven Spielberg.
Follow up: Where is Steven Spielberg from?
Intermediate Answer: The United States.
Follow up: Who is the director of Casino Royale?
Intermediate Answer: The director of Casino Royale is Martin Campbell.
Follow up: Where is Martin Campbell from?
Intermediate Answer: New Zealand.
So the final answer is: No
""",
    },
]

sample_prompt = PromptTemplate(input_variables=['question', 'answer'], template="Question: {question}\n{answer}")
question="Who was the father of Mary Ball Washington?"


def zephyr_prompt():
    few_shot_prompt_template = FewShotPromptTemplate(examples=examples, example_prompt=sample_prompt, prefix= "|<user>| \n", suffix="Question: {question} |<endoftext>| \n |<assistant>|", input_variables=['input'])
    return few_shot_prompt_template

def orca_prompt():
    few_shot_prompt_template = FewShotPromptTemplate(examples=examples, example_prompt=sample_prompt, prefix= "|<im-start>| user \n", suffix="Question: {question} |<im_end>| \n |<im_start>| assistant", input_variables=['input'])
    return few_shot_prompt_template

def default_prompt():
    few_shot_prompt_template = FewShotPromptTemplate(examples=examples, example_prompt=sample_prompt, suffix="Question: {question}", input_variables=['input'])
    return few_shot_prompt_template

HUGGING_FACE_MODELS = {
    'phi': 'microsoft/phi-2',
    'mamba': '',
    'zephyr': 'stabilityai/stablelm-zephyr-3b',
    'open_llama': 'openlm-research/open_llama_3b_v2',
    'orca2_7b': 'microsoft/Orca-2-7b',
    'mistral': 'mistralai/Mistral-7B-v0.1',
    'orca2_13b': 'microsoft/Orca-2-13b',
}


torch.set_default_device = "cuda"

model_id = HUGGING_FACE_MODELS['orca2_7b']

if model_id == 'stabilityai/stablelm-zephyr-3b':
    model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True, device_map = 'auto')
    few_shot_prompt = zephyr_prompt()
else:
    model = AutoModelForCausalLM.from_pretrained(model_id, device_map = 'auto')
    if model_id in ['microsoft/Orca-2-7b', 'microsoft/Orca-2-13b']:
        few_shot_prompt = orca_prompt()
    else:
        few_shot_prompt = default_prompt()

tokenizer = AutoTokenizer.from_pretrained(model_id)
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_length = 5000)
hf = HuggingFacePipeline(pipeline=pipe)

llm_chain = few_shot_prompt | hf

print(llm_chain.invoke({"question" : question}))
