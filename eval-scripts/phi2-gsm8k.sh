lm_eval --model hf \
    --model_args pretrained=microsoft/phi-2,parallelize=True \
    --tasks gsm8k \
    --batch_size auto:1 \
    --output_path results/phi-2/gsm8k/ \
    --log_samples \
    --seed 0
