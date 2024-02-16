# SmallLMReasoning
Enhancing reasoning capabilities in small LMs

# Installation
```
# Conda Setup
conda create -n harness python=3.10.13
conda activate harness

# Install Harness
cd lm-evaluation-harness
pip install -e .
```

# Evaluation

### [Phi-2 3B](https://huggingface.co/microsoft/phi-2) 

GSM8K
```
bash eval-scripts/phi2-gsm8k.sh
```
