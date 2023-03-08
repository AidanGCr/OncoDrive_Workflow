#!/bin/bash
#SBATCH --time=24:00:00
#SBATCH --account=def-ioannisr
#SBATCH --mem=125G

if [ -f "OncoDrive.samples.db" ]; then 
	rm OncoDrive.samples.db 
else 
	touch OncoDrive.samples.db
fi 

module load python
python myvcflib_samples.py OncoDrive.samples.db < allSamples_v2.hg38_multianno.sed_replace.pasamples.vcf

