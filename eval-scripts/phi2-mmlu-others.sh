lm_eval --model hf \
    --model_args pretrained=microsoft/phi-2,parallelize=True \
    --tasks mmlu_flan_cot_fewshot_other \
    --batch_size auto:1 \
    --output_path results/phi-2/mmlu/other/ \
    --log_samples \
    --seed 0 \