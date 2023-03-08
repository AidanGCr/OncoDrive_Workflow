#!/bin/bash
#SBATCH --time=24:00:00
#SBATCH --account=def-ioannisr
#SBATCH --mem=125G

module load bcftools

bcftools concat -O z0 -o allSamples.hc.vqsr.vt.mil.snpId.snpeff.dbnsfp.vcf.gz \
	allSamples.hc.vqsr.vt.mil.snpId.snpeff.dbnsfp0.vcf \
	allSamples.hc.vqsr.vt.mil.snpId.snpeff.dbnsfp1.vcf \
	allSamples.hc.vqsr.vt.mil.snpId.snpeff.dbnsfp2.vcf \
	allSamples.hc.vqsr.vt.mil.snpId.snpeff.dbnsfp3.vcf \
	allSamples.hc.vqsr.vt.mil.snpId.snpeff.dbnsfp4.vcf \
	allSamples.hc.vqsr.vt.mil.snpId.snpeff.dbnsfp5.vcf \
	allSamples.hc.vqsr.vt.mil.snpId.snpeff.dbnsfp6.vcf \
	allSamples.hc.vqsr.vt.mil.snpId.snpeff.dbnsfp7.vcf \
	allSamples.hc.vqsr.vt.mil.snpId.snpeff.dbnsfp8.vcf \
	allSamples.hc.vqsr.vt.mil.snpId.snpeff.dbnsfp9.vcf \
	allSamples.hc.vqsr.vt.mil.snpId.snpeff.dbnsfp10.vcf \
	allSamples.hc.vqsr.vt.mil.snpId.snpeff.dbnsfp11.vcf \
	allSamples.hc.vqsr.vt.mil.snpId.snpeff.dbnsfp12.vcf \
	allSamples.hc.vqsr.vt.mil.snpId.snpeff.dbnsfp13.vcf \
	allSamples.hc.vqsr.vt.mil.snpId.snpeff.dbnsfp14.vcf \
	allSamples.hc.vqsr.vt.mil.snpId.snpeff.dbnsfp15.vcf \
	allSamples.hc.vqsr.vt.mil.snpId.snpeff.dbnsfp16.vcf \
	allSamples.hc.vqsr.vt.mil.snpId.snpeff.dbnsfp17.vcf \
	allSamples.hc.vqsr.vt.mil.snpId.snpeff.dbnsfp18.vcf \
	allSamples.hc.vqsr.vt.mil.snpId.snpeff.dbnsfp19.vcf \
	allSamples.hc.vqsr.vt.mil.snpId.snpeff.dbnsfp20.vcf \
	allSamples.hc.vqsr.vt.mil.snpId.snpeff.dbnsfp21.vcf
