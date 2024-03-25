module load cuda/11.8.0
module load miniconda/22.11.1-1
conda activate harness

cd /work/pi_dhruveshpate_umass_edu/achauhan_umass_edu/SmallLMReasoning/ChainEval
export PYTHONPATH=".":$PYTHONPATH

config="configs/bbh/phi2/sot_fewshot_"
directory="results/phi2/bbh/sot/"

tasks=("word_sorting" "logical_deduction_three_objects")

for task in "${tasks[@]}"; do
    task_directory="$directory$task"/
    task_config="$config$task".yaml

    python chains/sot.py --config $task_config --outdir $task_directory
    python eval/eval.py --config configs/bbh/phi2/eval.yaml --outdir $task_directory
done