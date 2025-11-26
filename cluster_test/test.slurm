#!/bin/bash -l
#SBATCH --job-name=test
#SBATCH --time=00:05:00
#SBATCH --cpus-per-task=1
#SBATCH -p low
#SBATCH --account=thanksgrp
#SBATCH --qos=cnsdept-low-qos
#SBATCH -o /group/thanksgrp/code/modeling/cluster/log/testBatch_%j.txt
#SBATCH --mail-type=ALL

module load conda
conda activate /group/thanksgrp/envs/ml_env

# Move to working directory
cd /group/thanksgrp/code/modeling/cluster

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
python Test_Cluster.py $CUSTOMSTRING $CUSTOMNUM