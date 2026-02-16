#!/bin/bash
##########################
# Dorado Basecalling Commands
# This script runs INSIDE the singularity container
##########################


######## Define variables and make directories

# INPUT_DIR = raw POD5 input files in hosted
# OUTPUT_DIR = working directory in scratch for basecalled outputs

INPUT_DIR="/mmfs1/hosted/biosc/SchwartzLab/Nanopore/GopherTortoise/GT_7.5_B"
OUTPUT_DIR="/mmfs1/scratch/amf0120/GT_7.5_B/Dorado_basecalled"

# Create output directory
mkdir -p ${OUTPUT_DIR}

echo "==================================================="
echo "Starting regular basecalling for GT_7.5_B..."
echo "Input: ${INPUT_DIR}"
echo "Output: ${OUTPUT_DIR}"
echo "==================================================="

# Regular basecalling
dorado basecaller sup ${INPUT_DIR} \
     --device cpu \
     --recursive \
    > ${OUTPUT_DIR}/calls_regular.bam

echo "Regular basecalling complete!"

echo "==================================================="
echo "Starting methylation basecalling for GT_7.5_B..."
echo "==================================================="

# Methylation basecalling
dorado basecaller sup ${INPUT_DIR} \
    --device cpu \
    --modified-bases 5mCG_5hmCG \
    --recursive \
    > ${OUTPUT_DIR}/calls_methylation.bam

echo "Methylation basecalling complete!"
echo "==================================================="
echo "All basecalling jobs finished successfully!"
echo "==================================================="
