lm_eval --model hf \
    --model_args pretrained=openlm-research/open_llama_3b_v2,parallelize=True \
    --tasks mmlu_flan_cot_fewshot_social_sciences \
    --batch_size auto:1 \
    --output_path results/open_llama/mmlu/social_sciences/ \
    --log_samples \
    --seed 0 \