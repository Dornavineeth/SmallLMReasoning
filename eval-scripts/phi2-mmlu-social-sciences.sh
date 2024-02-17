lm_eval --model hf \
    --model_args pretrained=microsoft/phi-2,parallelize=True \
    --tasks mmlu_flan_cot_fewshot_social_sciences \
    --batch_size auto:1 \
    --output_path results/phi-2/mmlu/social_sciences/ \
    --log_samples \
    --seed 0 \