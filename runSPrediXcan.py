import os

givenGWASFile = "/data/amulford/GWAS_sum_stats/YRI_GWAS_capecitabine.assoc.txt.gz"
givenModelFolder = "/data/amulford/gtex_v8_elastic_net/eqtl_dbs/"

snp_column = "rs"            # header of the column containing the SNP ids
effect_allele = "allele1"    # header of the column containing the effect allele ???
noneffect_allele = "allele0" # header of the column containing the non-effect allele ???
phenotype = "beta" 	     # header of the column containing phenotype data
pval = "p_wald"            	                     # header of the column containing p-values
output = "S-results/cap"          	     # path to output (.csv file)

#os.system("python3 /data/amulford/MetaXcan/software/SPrediXcan.py --model_db_path "+model+" --covariance "+covariance+" --gwas_file "+givenGWASFile+" --snp_column "+snp_column+" --effect_allele_column "+effect_allele+" --non_effect_allele_column "+noneffect_allele+ " --beta_column "+phenotype+" --pvalue_column "+pval+" --output_file "+output)

os.system("bash SPrediPipe.sh -s /data/amulford/MetaXcan/software/SPrediXcan.py -m "+givenModelFolder+" --gwas "+givenGWASFile+" -o "+output)