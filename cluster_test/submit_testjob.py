#%%

import init
from os import path
import cluster_utils as clust
import utils
from datetime import datetime
import json

#%% create and push unique config file to cluster

current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
config_name = f"bandit_config_{current_datetime}.json"

# Create the config dictionary that stores data
config_data = {'test': True}
# define local and cluster path
local_path = path.join(utils.get_user_home(), 'bandit_modeling', 'configs')
remote_path= '/group/thanksgrp/code/modeling/cluster/configs'

# save config file locally
config_path = path.join(local_path, config_name)
utils.check_make_dir(config_path)
with open(config_path, "w") as f:
    json.dump(config_data, f, indent=4)
    
clust.push_to_cluster(config_path, remote_path)

#%% Run sbatch command

slurm_path = '/group/thanksgrp/code/modeling/cluster/test.slurm'
args = 'CUSTOMSTRING=\'{}\''.format(config_name)

# 3. Run sbatch on the cluster
print("Submitting job to SLURM")
status, output = clust.run_slurm_job(slurm_path, custom_args=args)
if status == 0:
    print("Job submitted successfully.")
    print(output)
else:
    print("Job submission failed!")
    print(output)

    
        
