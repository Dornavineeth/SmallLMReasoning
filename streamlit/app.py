import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from prompts import *
import torch


st.set_page_config(
    page_title="Small LM Reasoning",
    page_icon="🤖",
    layout="wide"
)
st.title("Small LM Reasoning")

_PIPELINE = {
    'microsoft/phi-2': None,
    'stabilityai/stablelm-zephyr-3b': None,
    'openlm-research/open_llama_3b_v2': None
    
}
@st.cache_resource(max_entries=len(_PIPELINE))
def get_pipeline(model_name):
    if model_name == 'stabilityai/stablelm-zephyr-3b':
        model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True, device_map = 'auto')
    else:
        model = AutoModelForCausalLM.from_pretrained(model_name, device_map = 'auto')
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)
    return pipe

def get_prompts(benchmark):
    if benchmark == 'GSM8K':
        return GSM8K_PROMPT
    elif benchmark == 'GSM8K_SOT':
        return GSM8K_SOT_PROMPT
    elif benchmark == 'MMLU':
        return MMLU_PROMPT
    elif benchmark == "BBH":
        return BBH_PROMPT
    else:
        st.error("Benchmark not available")

def generate_response(pipe, text, stop_texts=[], **generation_kwargs):
    output = pipe(
        [text],
        return_full_text=False,
        **generation_kwargs
    )
    # st.write(output)
    num_return_sequences = generation_kwargs.get("num_return_sequences", 1)
    generated_texts = [output[0][i]['generated_text'] for i in range(num_return_sequences)]
    for s in stop_texts:
        generated_texts = [generated_text.split(s)[0]for generated_text in generated_texts]
    return generated_texts

def generate_cot_decoding_response(pipe, text, stop_texts=["Q:","Question:"], generation_kwargs={}, generation_kwargs_first={}):
    top_k = generation_kwargs.get("top_k", 10)
    first_output = pipe(
        [text],
        return_full_text=False,
        **generation_kwargs_first
    )
    st.write(first_output)
    generated_texts = [text+first_output[0][i]['generated_text'] for i in range(top_k)]
    output = pipe(
        generated_texts,
        return_full_text=False,
        **generation_kwargs
    )
    st.write(output)
    generated_texts = [first_output[0][i]['generated_text'] + output[i][0]['generated_text'] for i in range(top_k)]
    for s in stop_texts:
        generated_texts = [generated_text.split(s)[0]for generated_text in generated_texts]
    return generated_texts

model_names = st.multiselect('Select an Model:', list(_PIPELINE.keys()), [])
for model_name in list(_PIPELINE.keys()):
    if model_name not in model_names:
        del _PIPELINE[model_name]
        _PIPELINE[model_name] = None
for model_name in model_names:
    pipe = get_pipeline(model_name)
    _PIPELINE[model_name] = pipe

self_consistency = st.sidebar.number_input("Self Consistency K", min_value=1, value=2, step=1, help="K in self Consistency")
cot_decoding = st.sidebar.checkbox("CoT Decoding", value=False, help="Whether to use CoT Decoding")
do_sample = st.sidebar.checkbox("Do Sample", value=True, help="Whether to use sampling for generating text")
num_beams = st.sidebar.number_input("Number of Beams", min_value=1, value=1, step=1, help="Beam size for the beam search")
num_return_sequences = st.sidebar.number_input("Number of Sequences", min_value=1, value=1, step=1, help="Number of generated sequences")
max_new_tokens = st.sidebar.number_input("Max new Tokens", min_value=1, value=200, step=1, help="Maximum length of generated text")
top_k = st.sidebar.number_input("Top K", min_value=0, value=40, step=1, help="Number of top tokens considered during sampling")
top_p = st.sidebar.number_input("Top P", min_value=0.01, max_value=1.0, value=0.95, step=0.01, help="Cumulative probability for top-p sampling")
temperature = st.sidebar.number_input("Temperature", min_value=0.01, value=0.5, step=0.01, help="Sampling temperature")

    
try:
    generation_kwargs = {
        "num_beams": int(num_beams),
        "num_return_sequences": int(num_return_sequences),
        "do_sample": bool(do_sample),
        "max_new_tokens": int(max_new_tokens),
        "top_k": int(top_k),
        "top_p": float(top_p),
        "temperature": float(temperature)
    }
    
    if cot_decoding:
        if top_k>10:
            st.warning("Made top_k as 10")
        generation_kwargs_first ={
            "num_beams": min(int(top_k),10),
            "num_return_sequences": min(int(top_k),10),
            "max_new_tokens": 1,
            "top_k": int(top_k),
        }
        generation_kwargs = {
            "do_sample": False,
            "num_return_sequences": 1,
            "max_new_tokens": max_new_tokens,
            "top_k": int(top_k),
        }
except:
    st.error("Something wrong in generation config")

benchmark =  st.selectbox('Select an Benchmark:', 
                            [
                              "GSM8K",
                              "MMLU",
                              "BBH",
                              "GSM8K_SOT"
                            ]
                        )
benchmark_prompt = get_prompts(benchmark)

with st.form('my_form'):
    text = st.text_area('input_text', benchmark_prompt, height=1000)
    submitted = st.form_submit_button('Submit')
    if submitted:
        # st.write(generation_kwargs)
        if len(model_names)==0:
            st.error("Please select atleast one model")
        for model_name in model_names:
            torch.manual_seed(1234)
            pipe = _PIPELINE[model_name]
            st.header(f"{model_name}")
            for k in range(self_consistency):
                if cot_decoding:
                    generated_texts = generate_cot_decoding_response(pipe, text, ["Q:","Question:"], generation_kwargs, generation_kwargs_first)
                else:
                    generated_texts = generate_response(pipe, text, stop_texts=["Q:","Question:"], **generation_kwargs)
                for it, generated_text in enumerate(generated_texts):
                    st.subheader(f"Self Conistency {k}\tSequence {it}")
                    st.text(generated_text)
                
