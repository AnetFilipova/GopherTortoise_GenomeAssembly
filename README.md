# Gopher tortoise (*Gopherus polyphemus*) Genome Assembly

### Aim: There is no genome available for the gopher tortoise so here we aim to assemble two separate genomes from two individuals that have either experienced a cold-dormancy winter or have not.

## Background
This project is part of the bigger project: **Exploring molecular memory: investigating the short-term impact of first-year cold dormancy on the transcriptomic responses and epigenetic regulation in head-started gopher tortoises.
The gopher tortoise is a keystone species endemic to the southeastern United States and has been a subject to conservation programs that aim to facilitate early life survival. However, current conservation initiatives such as head-starting do not include cold-dormancy as part of the raising process. This raises the following question: By trying to help these individuals reach a size that will ultimately benefit survival, are we unintentioanlly changing the way their genes respond to different thermal conditions? Gopher tortoises in Alabama, USA have naturally evolved to experience cold-dormancy in the winter which helps them to prioritize energy saving.**

Here we will test the transcriptomic and epigenetic responses to skipping or experiencing cold-dormancy by looking at protein coding genes from blood. In our experiment we split hatchling tortoises into two treatments 1)Cold-dormancy and 2)Constant-warmth, and raised the animals in captivity for one year. We took blood samples from both treatments at four different timepoints: 1) Before dormancy, 2)At the end of dormancy, 3)3-Weeks Post-dormancy, and 4)3-Months Post-dormancy.
We will be looking at differential gene expression and DNA methylation to address the following goals:
1. To determine how first-year cold dormancy alters blood gene expression during the dormancy period and whether these transcriptional changes persist after experiencing dormancy.
2. To test whether cold dormancy changes DNA methylation of differentially expressed genes involved in energy saving and metabolic efficiency, and whether methylation persists post-dormancy.


## Whole Genome Sequencing

Long-read Oxford Nanopore MinION data was generated from 2 individuals (Cold-dormancy and Constant-warmth). These individuals are siblings and are supposedly the same sex in order to minimize the variation attributed to other factors besides treatment effects.
This serves three purposes:

1. To produce a reference-based assembly of the gopher tortoise genome for mapping RNAseq data;
2. To characterize the cold-dormancy blood methylome vs. the constant-warmth blood methylome;
3. To produce pilot data on potential differentially methylated regions associated with differentially expressed genes for targeted enzymatic conversion methyl-seq.

### Rationale for producing a reference-based asembly

With only ~5X coverage generated from the long-read data, we had to use a reference-based approach using a high-quality reference genome of a closely related species. In this case, we used the Bolson (Mexican) tortoise (*Gopherus flavomarginatus*)([BioProject:PRJNA794188] (https://www.ncbi.nlm.nih.gov/bioproject/PRJNA794188/)

## Genome Assembly Bioinformatic Pipeline Steps

**1.HAC Basecalling:** Convert MinION raw data to FASTQ (Dorado)  
**2.Quality filtering:** Filter low-quality long reads (Filtlong)   
**3.Reference genome indexing:** (Samtools and Minimap2)  
**4.Mapping:** Align the gopher tortoise long-read  data to the bolson tortoise reference genome (Minimap2)  
**5.Call variants:** Identify where gopher tortoise differs from bolson tortoise (SNPS, indels, etc.) (Medaka)  
**6.Replace variants:** Substitute those variant positions into the bolson tortoise genome to create a gopher tortoise-specific version (BCFtools)    
**7.Transfer annotation:** Copy gene annotations from the bolson tortoise to the new gopher tortoise genome (Liftoff or TOGA)
