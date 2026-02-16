#!/bin/bash
##########################
# SLURM Job Submission for Dorado Basecalling
##########################

#SBATCH --job-name=Dorado_GT_7.5_B            # job name
#SBATCH --nodes=1                             # node(s) required for job
#SBATCH --ntasks=32                           # number of tasks across all nodes
#SBATCH --partition=bigmem2                   # name of partition to submit job
#SBATCH --time=7-10:00:00                     # run time (D-HH:MM:SS)
#SBATCH --output=~/Nanopore_Projects/GopherTortoise_GenomeAssembly/GT_7.5_B/logs/job-%j_Dorado_GT_7.5_B.out           # Output file. %j is replaced with job ID
#SBATCH --error=~/Nanopore_Projects/GopherTortoise_GenomeAssembly/GT_7.5_B/logs/job-%j_Dorado_GT_7.5_B.err           # Error file. %j is replaced with job ID
#SBATCH --mail-type=ALL                       # will send email for begin, end, fail
#SBATCH --mail-user=amf0120@auburn.edu        # replace email address for the user

# Load singularity
module load singularity/3.8.4

# Print debugging info
echo "Running on node: $(hostname)"
echo "Running on CPU mode"

###### Define variables and container path
CONTAINER="/mmfs1/hosted/biosc/SchwartzLab/NanoporePrograms/dorado_latest.sif"
EXEC_SCRIPT="/home/amf0120/Nanopore_Projects/GopherTortoise_GenomeAssembly/GT_7.5_B/scripts/run_dorado.sh"
OUTPUT_DIR="/mmfs1/scratch/amf0120/GT_7.5_B/Dorado_basecalled"

# Create output directory
mkdir -p ${OUTPUT_DIR}

# Run the container and execute the dorado script inside it
singularity exec --bind /mmfs1:/mmfs1 ${CONTAINER} ${EXEC_SCRIPT}
