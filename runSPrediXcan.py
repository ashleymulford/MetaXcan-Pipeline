import os

model = ""           	     # this is the path to the model transcriptome (.db file)
covariance = ""     	     # account for related individuals <- we won't use?
gwas = ""           	     # path to the .assoc file from the GWAS
gwas_pattern = ""            # string representing what files to use <- might want to zip the files
snp_column = "rs"            # header of the column containing the SNP ids
effect_allele = "allele1"    # header of the column containing the effect allele ???
noneffect_allele = "allele0" # header of the column containing the non-effect allele ???
phenotype = "beta" 	     # header of the column containing phenotype data
pval = "p_wald"            	     # header of the column containing p-values
output = ""          	     # path to output (.csv file)

os.system("SPrediXcan.py --model_db_path "+model+" --covariance "+covariance+" --gwas_folder "+gwas+ \
" --gwas_file_pattern "+gwas_pattern+" --snp_column "+snp_column+" --effect_allele_column "+effect_allele+ \
" --non_effect_allele_column "+noneffect_allele+ " --beta_column "+phenotype+" --pvalue_column "+pval"+ \
" --output_file "+output)
