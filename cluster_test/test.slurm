#!/bin/bash -l
#SBATCH --job-name=test
#SBATCH --time=00:05:00
#SBATCH --cpus-per-task=1
#SBATCH -p low
#SBATCH --account=thanksgrp
#SBATCH --qos=cnsdept-low-qos
#SBATCH -o /group/thanksgrp/python/test/log/testBatch_%A.txt
#SBATCH --mail-type=ALL
#SBATCH --array=1-2

LOGDIR=/group/thanksgrp/python/test/log/$SLURM_ARRAY_JOB_ID
mkdir -p $LOGDIR

if test -z "$CUSTOMSTRING"
then
   CUSTOMSTRING=\'internal\'
else
   CUSTOMSTRING="${CUSTOMSTRING}"
fi

if test -z "$CUSTOMNUM"
then
   CUSTOMNUM=0
else
   CUSTOMNUM="${CUSTOMNUM}"
fi

echo "CUSTOMSTRING = " $CUSTOMSTRING
echo "CUSTOMNUM = " $CUSTOMNUM

# Run Python script

module load conda
conda activate /group/thanksgrp/envs/neuropy

# save absolute path to python executable
PYTHON=$(which python)

srun -n 1 -o $LOGDIR/test_%a.txt $PYTHON /group/thanksgrp/python/code/pyutils/cluster_test/test_cluster.py --config_path $CUSTOMSTRING --custom_num $CUSTOMNUM