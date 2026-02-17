#!/bin/bash
##########################
# SLURM Job Submission for Dorado Basecalling
##########################

#SBATCH --job-name=Dorado_GT_7.4_B
#SBATCH --nodes=1
#SBATCH --cpus-per-task=32
#SBATCH --partition=bigmem2
#SBATCH --time=10-00:00:00
#SBATCH --output=~/Nanopore_Projects/GopherTortoise_GenomeAssembly/GT_7.5_B/logs/job-%j_Dorado_GT_7.4_B.out
#SBATCH --error=~/Nanopore_Projects/GopherTortoise_GenomeAssembly/GT_7.5_B/logs/job-%j_Dorado_GT_7.4_B.err
#SBATCH --mail-type=ALL
#SBATCH --mail-user=amf0120@auburn.edu


# Load singularity
module load singularity/3.8.4

# Print debugging info
echo "Running on node: $(hostname)"
echo "Running on CPU mode"

# Define variables and container path
CONTAINER="/mmfs1/hosted/biosc/SchwartzLab/NanoporePrograms/dorado_latest.sif"
EXEC_SCRIPT="/home/amf0120/Nanopore_Projects/GopherTortoise_GenomeAssembly/GT_7.4_B/scripts/run_dorado.sh"
OUTPUT_DIR="/mmfs1/scratch/amf0120/GT_7.4_B/Dorado_basecalled"

# Create output directory
mkdir -p ${OUTPUT_DIR}

# Run the container and execute the dorado script inside it
singularity exec --bind /mmfs1:/mmfs1 ${CONTAINER} ${EXEC_SCRIPT}
