#!/bin/bash
##########################
# Dorado Basecalling Commands
# This script runs INSIDE the singularity container
##########################

########## Define variables and make directories

# INPUT_DIR = raw POD5 input files from hosted
# OUTPUT_DIR = working directory in scratch for basecalled outputs

INPUT_DIR="/mmfs1/hosted/biosc/SchwartzLab/Nanopore/GopherTortoise/GT_7.4_B"
OUTPUT_DIR="/mmfs1/scratch/amf0120/GT_7.4_B/Dorado_basecalled"

# Create output directory
mkdir -p ${OUTPUT_DIR}

echo "==================================================="
echo "Starting both regular and methylation basecalling for GT_7.4_B..."
echo "Input: ${INPUT_DIR}"
echo "Output: ${OUTPUT_DIR}"
echo "==================================================="

# Basecalling
dorado basecaller sup ${INPUT_DIR} \
     --device cpu \
     --modified-bases 5mCG_5hmCG
     --recursive \
     --threads 32 \
    > ${OUTPUT_DIR}/calls_methylation.bam

echo "Basecalling complete!"
