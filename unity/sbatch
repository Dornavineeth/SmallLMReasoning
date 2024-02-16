#!/bin/bash
#
# change mail-user to your email and run by command: sbatch abc.sbatch
#
#SBATCH --job-name=phi-2
#SBATCH --output=unity/logs/phi-2.txt       # output file
#SBATCH -c 18                               # Number of Cores per Task
#SBATCH -p gpu                              # Partition to submit to (serial_requeue), see here for all avaible resource: https://docs.unity.rc.umass.edu/technical/nodelist.html
#SBATCH -G 4                                # Number of GPUs
#SBATCH --mem=20G                           # Memory pool for all cores (see also --mem-per-cpu)
#SBATCH -e unity/logs/phi-2.err             # File to which STDERR will be written
#SBATCH --mail-user=vdorna@umass.edu        # Email to which notifications will be sent
#SBATCH --mail-type=ALL                     # Email for all types of Actions
#SBATCH -t 1-00:00:0                        # Job time limit 7-10:00:00 
#SBATCH --account=pi_dhruveshpate_umass_edu # PI account

module load miniconda/22.11.1-1
conda activate harness

nvidia-smi
cd /work/pi_dhruveshpate_umass_edu/vdorna_umass_edu/SmallLMReasoning

# bash eval-scripts/phi2-gsm8k-fewshot-cot.sh
bash eval-scripts/phi2-gsm8k.sh

echo "Done"