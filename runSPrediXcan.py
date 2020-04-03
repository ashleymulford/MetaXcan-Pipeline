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

os.system("python3 GWAS_pipeline.py --snp_cov /data/amulford/gtex_v8_elastic_net/gtex_v8_expression_elastic_net_snp_smultixcan_covariance.txt --snp_col rs --effect allele1 --noneffect allele0 --p_val p_wald -s /data/amulford/MetaXcan/software/ -d "+givenModelFolder+" --gwas "+givenGWASFile+" -o "+output)
