lm_eval --model hf \
    --model_args pretrained=microsoft/phi-2,parallelize=True \
    --tasks mmlu_flan_cot_fewshot_abstract_algebra,mmlu_flan_cot_fewshot_anatomy \
    --batch_size auto:1 \
    --output_path results/phi-2/mmlu/ \
    --log_samples \
    --seed 0 \
    --limit 10