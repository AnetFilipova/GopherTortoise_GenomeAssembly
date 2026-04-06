#!/bin/bash

#SBATCH --job-name=GT_7.4_B_alignment
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --partition=general
#SBATCH --time=12:00:00
#SBATCH --output=/scratch/amf0120/GT_7.4_B/logs/job-%j_alignment_%a.out
#SBATCH --error=/scratch/amf0120/GT_7.4_B/logs/job-%j_alignment_%a.err
#SBATCH --mail-type=ALL
#SBATCH --mail-user=amf0120@auburn.edu

# Load required modules
module load minimap2
module load samtools

# Check that a subset argument was provided
if [ -z "$1" ]; then
    echo "Usage: sbatch submit_alignment.sh small"
    echo "       sbatch submit_alignment.sh large"
    exit 1
fi

SUBSET=$1

echo "Starting alignment for ${SUBSET} subset..."
echo "Running on node: $(hostname)"

# Run the alignment script
python3 /home/amf0120/Nanopore_Projects/GopherTortoise_GenomeAssembly/GT_7.4_B/scripts/02_align_reads.py ${SUBSET}

echo "Job complete!"
