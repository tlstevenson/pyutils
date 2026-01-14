# -*- coding: utf-8 -*-
"""
Contains methods to work with clusters

Created on Thu Apr 24 10:14:47 2025

@author: tanne
"""

from os import path
import json
import subprocess
import sys

# %% Commands to interact with cluster through python instead of the command line

def on_cluster():
    return sys.platform == 'linux'

def clean_cluster_path(cluster_path):
    return cluster_path.replace('\\', '/')

def push_to_cluster(local_path, cluster_path):
    '''
    Push files to cluster. To copy all contents of a folder without creating a folder of that name on the cluster, 
    include a '/' at the end of local_path. To create a new folder to match the name of the folder being copied,
    do not include a trailing '/'

    Parameters
    ----------
    local_path : The local path to the folder/files to be copied
    cluster_path : The path on the cluster where the folder/files will be copied

    '''
    config = __get_cluster_config()
    
    cluster_path = clean_cluster_path(cluster_path)
    
    if not folder_exists(cluster_path):
        run_command('mkdir -p {}'.format(cluster_path), print_out=False)

    print('Pushing from {} to {}'.format(local_path, cluster_path))
    

    cmd = 'rsync --archive --one-file-system --progress {} {}:{}'.format(local_path, config['con'], cluster_path)

    
    status, output = run_local_command(cmd, print_out=False)
    if status != 0:
        print('status: {}. output: {}'.format(status, output))

def pull_from_cluster(cluster_path, local_path):
    '''
    Pull files from the cluster. To copy all contents of a folder without creating a folder of that name locally, 
    include a '/' at the end of cluster_path. To create a new folder to match the name of the folder being copied,
    do not include a trailing '/'

    Parameters
    ----------
    cluster_path : The path on the cluster where the folder/files will be copied from
    local_path : The local path where the folder/files will be copied

    '''
    config = __get_cluster_config()
    
    cluster_path = clean_cluster_path(cluster_path)
    
    print('Pushing from {} to {}'.format(local_path, cluster_path))
    

    cmd = 'rsync --archive --one-file-system --info=progress2 {} {}:{}'.format(local_path, config['con'], cluster_path)
    status, output = run_local_command(cmd)

    if status != 0:
        print('status: {}. output: {}'.format(status, output))

def file_exists(file_path):
    
    file_path = clean_cluster_path(file_path)
    
    cmd = 'test -f {} && echo true || echo false'.format(file_path)
    status, output = run_command(cmd, print_out=False)
    output = output.strip()
    if output == 'true':
        return True
    elif output == 'false':
        return False
    else:
        print('Error: {}'.format(output))
        return 'error'

def folder_exists(folder_path):
    
    folder_path = clean_cluster_path(folder_path)
    
    cmd = 'test -d {} && echo true || echo false'.format(folder_path)
    status, output = run_command(cmd, print_out=False)
    output = output.strip()
    if output == 'true':
        return True
    elif output == 'false':
        return False
    else:
        print('Error: {}'.format(output))
        return 'error'
    
def get_all_files(folder_path):
    
    folder_path = clean_cluster_path(folder_path)
    
    cmd = 'ls {}'.format(folder_path)
    status, output = run_command(cmd, print_out=False)
    output = output.strip().split('\n')
    
    if status == 0:
        return output
    else:
        print('Error: {}'.format(output))
        return 'error'

def run_slurm_job(slurm_path, sbatch_options='', custom_args=None, print_out=True):
    
    slurm_path = clean_cluster_path(slurm_path)
    
    config = __get_cluster_config()
    if custom_args is None:
        cmd = "bash --login -c 'sbatch --mail-user={} {} {}'".format(config['email'], sbatch_options, slurm_path)
    else:
        cmd = "bash --login -c 'sbatch --mail-user={} {} --export={} {}'".format(config['email'], sbatch_options, custom_args, slurm_path)
    return run_command(cmd, print_out)

def run_command(cmd, print_out=True):
    config = __get_cluster_config()
    cmd = 'ssh {} "{}"'.format(config['con'], cmd)
    return run_local_command(cmd, print_out)

def run_local_command(cmd, print_out=True):
    try:
        result = subprocess.run(cmd, shell=True, check=False, capture_output=True, text=True)
        if print_out:
            print(result.stdout)
        
        return result.returncode, result.stdout + '\n' + result.stderr
    except Exception as e:
        print(str(e))
        return 1, str(e)

# %% Cluster connection manager

def __get_cluster_config():
    '''Private method to get the cluster credentials'''

    config_path = path.join(path.expanduser('~'), '.clustconf')

    if path.exists(config_path):
        # read db connection information from file
        with open(config_path, 'r') as f:
            cluster_info = json.load(f)

    else:
        # create a new cluster config
        cluster_info = {}
        
        # get values from user
        val = ''
        while val == '':
            val = input('Enter cluster connection (username@hostname): ')
        cluster_info['con'] = val

        val = ''
        while val == '':
            val = input('Enter email (for run updates): ')
        cluster_info['email'] = val

        # write file
        with open(config_path, 'w') as f:
            json.dump(cluster_info, f)

    return cluster_info

