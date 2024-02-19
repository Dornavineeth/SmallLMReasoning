lm_eval --model hf \
    --model_args pretrained=openlm-research/open_llama_3b_v2,parallelize=True \
    --tasks mmlu_flan_cot_fewshot_stem \
    --batch_size auto:1 \
    --output_path results/open_llama/mmlu/stem/ \
    --log_samples \
    --seed 0 \