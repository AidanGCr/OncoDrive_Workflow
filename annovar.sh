#!/bin/bash
#SBATCH --time=24:00:00
#SBATCH --account=def-ioannisr
#SBATCH --mem=50G

module load annovar

table_annovar.pl /home/aidangc/scratch/data/allSamples.hc.vqsr.vt.mil.snpId.snpeff.dbnsfp.vcf.gz /home/aidangc/scratch/humandb -buildver hg38 -out allSamples -remove -protocol refGene,clinvar_20221231 -operation g,f -nastring . -vcfinput -polish
