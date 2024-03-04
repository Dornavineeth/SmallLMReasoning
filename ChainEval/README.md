## Installation
```
pip install datasets 
```

## Setup

```
cd SmallLMReasoning/ChainEval
export PYTHONPATH=".":$PYTHONPATH
```

## Sample Run
If testing on Phi-2 (or any model whose weights are in the form of safetensors). First need to run `module load cuda/11.8.0`. 

```
python chains/qa.py --config configs/phi2_gsm8k.yaml
```
