from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel
from langchain_core.runnables import RunnablePassthrough
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch 

torch.set_default_device = "cuda"

HUGGING_FACE_MODELS = {
    'phi': 'microsoft/phi-2',
    'mamba': '',
    'zephyr': 'stabilityai/stablelm-zephyr-3b',
    'open_llama': 'openlm-research/open_llama_3b_v2',
    'orca2_7b': 'microsoft/Orca-2-7b',
    'mistral': 'mistralai/Mistral-7B-v0.1',
    'orca2_13b': 'microsoft/Orca-2-13b',
}

model_id = HUGGING_FACE_MODELS['phi']

model = AutoModelForCausalLM.from_pretrained(model_id, device_map = 'auto')
tokenizer = AutoTokenizer.from_pretrained(model_id)

pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_length = 2048)
hf = HuggingFacePipeline(pipeline=pipe)

skeleton_generator_template = """[User:] You’re an organizer responsible for only \
giving the skeleton (not the full content) for answering the question.
Provide the skeleton in a list of points (numbered 1., 2., 3., etc.) to answer \
the question. \
Instead of writing a full sentence, each skeleton point should be very short \
with only 3∼5 words. \
Generally, the skeleton should have 3∼10 points. Now, please provide only the skeleton \
for the following question.
{question}
[Assistant:] Skeleton: \n1."""

skeleton_generator_prompt = ChatPromptTemplate.from_template(
    skeleton_generator_template
)

skeleton_generator_chain = (
    skeleton_generator_prompt | hf | StrOutputParser() | (lambda x: "1. " + x)
)

skeleton = skeleton_generator_chain.invoke({"question":"How to cook scrambled eggs"})

point_expander_template = """[User:] You’re responsible for continuing \
the writing of one and only one point in the overall answer to the following question.
{question}
The skeleton of the answer is
{skeleton}
Continue and only continue the writing of point {point_index}. \
Write it **very shortly** in 1∼2 sentence and do not continue with other points!
[Assistant:] {point_index}. {point_skeleton}"""

point_expander_prompt = ChatPromptTemplate.from_template(point_expander_template)

point_expander_chain = RunnablePassthrough.assign(
    continuation=point_expander_prompt | hf | StrOutputParser()) \
        | (lambda x: x["point_skeleton"].strip() + " " + x["continuation"])

def parse_numbered_list(input_str):
    """Parses a numbered list into a list of dictionaries

    Each element having two keys:
    'index' for the index in the numbered list, and 'point' for the content.
    """
    # Split the input string into lines
    try:
        idx = input_str.index("[User:]")
        input_str = input_str[:idx]
    except:
        pass
    lines = input_str.split("\n")

    # Initialize an empty list to store the parsed items
    parsed_list = []

    for line in lines:
        # Split each line at the first period to separate the index from the content
        parts = line.split(". ", 1)

        if len(parts) == 2:
            # Convert the index part to an integer
            # and strip any whitespace from the content
            index = int(parts[0])
            point = parts[1].strip()

            # Add a dictionary to the parsed list
            parsed_list.append({"point_index": index, "point_skeleton": point})

    return parsed_list, input_str

def create_list_elements(_input):
    skeleton = _input["skeleton"]
    numbered_list, skeleton = parse_numbered_list(skeleton)
    for el in numbered_list:
        el["skeleton"] = skeleton
        el["question"] = _input["question"]
    return numbered_list


def get_final_answer(expanded_list):
    final_answer_str = "Here's a comprehensive answer:\n\n"
    for i, el in enumerate(expanded_list):
        try:
            idx = el.index("[User:]")
            el = el[:idx]
        except:
            pass
        final_answer_str += f"{i+1}. {el}\n\n"
    return final_answer_str


class ChainInput(BaseModel):
    question: str


chain = (
    RunnablePassthrough.assign(skeleton=skeleton_generator_chain) #makes a dictionary with key and value pairs
    | create_list_elements
    | point_expander_chain.map()
    | get_final_answer
).with_types(input_type=ChainInput)

print(chain.invoke({"question":"How to cook scrambled eggs?"}))