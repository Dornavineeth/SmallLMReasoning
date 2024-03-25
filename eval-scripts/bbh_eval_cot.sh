module load cuda/11.8.0
module load miniconda/22.11.1-1
conda activate harness

cd /work/pi_dhruveshpate_umass_edu/achauhan_umass_edu/SmallLMReasoning/ChainEval
export PYTHONPATH=".":$PYTHONPATH

config="configs/bbh/zephyr/cot_fewshot_"
directory="results/zephyr/bbh/"

tasks=("boolean_expressions" \
"causal_judgement" \
"date_understanding" \
"disambiguation_qa" \
"dyck_languages" \
"formal_fallacies" \
"geometric_shapes" \
"hyperbaton" \
"logical_deduction_five_objects" \
"logical_deduction_seven_objects" \
"logical_deduction_three_objects" \
"movie_recommendation" \
"multistep_arithmetic_two" \
"navigate" \
"object_counting" \
"penguins_in_a_table" \
"reasoning_about_colored_objects" \
"ruin_names" \
"salient_translation_error_detection" \
"snarks" \
"sports_understanding" \
"temporal_sequences" \
"tracking_shuffled_objects_five_objects" \
"tracking_shuffled_objects_seven_objects" \
"tracking_shuffled_objects_three_objects" \
"web_of_lies" \
"word_sorting")

for task in "${tasks[@]}"; do
    task_directory="$directory$task"/
    task_config="$config$task".yaml

    python chains/qa.py --config $task_config --outdir $task_directory
    python eval/eval.py --config configs/bbh/zephyr/eval.yaml --outdir $task_directory
done