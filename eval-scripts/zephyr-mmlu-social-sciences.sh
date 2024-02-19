lm_eval --model hf \
    --model_args pretrained=stabilityai/stablelm-zephyr-3b,parallelize=True,trust_remote_code=True \
    --tasks mmlu_flan_cot_fewshot_social_sciences \
    --batch_size auto:1 \
    --output_path results/zephyr/mmlu/social_sciences/ \
    --log_samples \
    --seed 0 \