#!/bin/bash
#SBATCH --time=24:00:00
#SBATCH --account=def-ioannisr 
#SBATCH --mem=125G 

module load bcftools

bcftools view allSamples.hg38_multianno.sed_replace.vcf -S samples.txt > allSamples.hg38_multianno.sed_replace.pasamples.vcf
