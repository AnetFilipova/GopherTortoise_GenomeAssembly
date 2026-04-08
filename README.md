## Gopher tortoise (*Gopherus polyphemus*) Genome Mapping

## Background

This project is part of a larger effort to assemble the genome of the 
gopher tortoise (*Gopherus polyphemus*) using long-read Oxford Nanopore sequencing data. A reproducible pipeline was developed to demonstrate the importance of sequencing coverage depth in reference-guided genome mapping.

## Objective

Map Nanopore reads from individual GT_7.4_B against the Bolson (Mexican) tortoise (*Gopherus flavomarginatus*) reference genome ([BioProject:PRJNA794188] (https://www.ncbi.nlm.nih.gov/bioproject/PRJNA794188/) at two different coverage depths. We are going to map 10% of the data (small dataset) versus 100% of the data (large dataset) and will compare the results.

## Scripts

| Script | Description |
|--------|-------------|
| `genome_mapping_utils.py` | Utility module with reusable functions for running shell commands, validating files, extracting sample names, and parsing alignment statistics |
| `01_subsample.py` | Selects a small (13 files, ~10%) and large (135 files, 100%) subset of FASTQ files |
| `02_align_reads.py` | Aligns selected FASTQ files to the reference genome using minimap2 |
| `03_summarize_results.py` | Runs samtools stats on BAM files and generates a comparison summary |
| `04_plot_results.py` | Calculates estimated coverage depth and generates a bar chart |
| `submit_alignment.sh` | SLURM submission script for running alignment on the HPC cluster |


