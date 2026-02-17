#!/bin/bash
##########################
# Index the Gopherus flavomarginatus Reference Genome
##########################

#SBATCH --job-name=Index_RefGenome           # job name
#SBATCH --nodes=1                            # node(s) required for job
#SBATCH --ntasks=4                           # number of tasks across all nodes
#SBATCH --partition=bigmem2                  # name of partition to submit job
#SBATCH --mem=20GB                           # requesting memory size
#SBATCH --time=02:00:00                      # Run time (D-HH:MM:SS)
#SBATCH --output=~/Nanopore_Projects/GopherTortoise_GenomeAssembly/Gopherus_flavomarginatus_Reference/job-%j_Index_RefGenome.out           # Output file. %j is replaced with job ID
#SBATCH --error=~/Nanopore_Projects/GopherTortoise_GenomeAssembly/Gopherus_flavomarginatus_Reference/job-%j_Index_RefGenome.err            # Error file. %j is replaced with job ID
#SBATCH --mail-type=ALL                      # will send email for begin,end,fail
#SBATCH --mail-user=amf0120@auburn.edu       # replace with user email address

# Load required modules
module load samtools/1.17    # required for variant calling with bcftools later
module load minimap2/2.26    # will be used for aligning the reads against the reference genome

##########  Define variables
REFDIR="/hosted/biosc/SchwartzLab/Nanopore/GopherTortoise/Gopherus_flavomarginatus_Ref_Genome"
REFGENOME="GCF_025201925.1_rGopFla2.mat.asm_genomic.fna"

# Change to reference directory
cd ${REFDIR}

echo "Indexing reference genome for alignment"
echo "Reference: ${REFGENOME}"

# Create samtools index (.fai)
echo "Creating samtools index"
samtools faidx ${REFGENOME}

# Create minimap2 index (.mmi)
echo "Creating minimap2 index"
minimap2 -t 4 -d ${REFGENOME%.fna}.mmi ${REFGENOME}

echo "Indexing complete!"
echo "Created files:"
ls -lh ${REFGENOME}*
