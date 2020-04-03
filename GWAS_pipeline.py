import os, argparse

# Parse args
p = argparse.ArgumentParser()
p.add_argument("-d","--db_dir", required=True, help="directory for the model to predict against (both *.db and *.txt.gz files")
p.add_argument("-s","--scripts_dir", default="~/MetaXcan/Software", help="directory containing the MetaXcan scripts, called 'software' in the MetaXcan package")
p.add_argument("-g","--gwas_path", required=True, help="file containing the GWAS summary statistics (*.assoc.txt.gz)")
p.add_argument("-o","--output", default="~/out", help="directory for output files (*.csv and SMultiXcan.txt")
p.add_argument("--snp_col", default="variant_id", help="name of the column containing SNP data in the GWAS summary statistics")
p.add_argument("--effect","--effect_col", default="effect_allele", help="name of the column containing the effect allele data in the GWAS summary statistics")
p.add_argument("--noneffect","--noneffect_col", default="noneffect_allele", help="name of the column containing the noneffect allele in the GWAS summary statistics")
p.add_argument("--phenotype", "--beta", default="beta", help="name of the column containing the phenotype data in the GWAS summary statistics")
p.add_argument("-p","--p_val", default="p_value", help="name of the column containing the p-value in the GWAS summary statistics")
p.add_argument("--snp_cov", required=True, help="file containing SNP covariance which comes in the model download (*_covariance.txt)")

a = p.parse_args()
# Needed args
software = a.scripts_dir
model = a.db_dir
GWAS = a.gwas_path
snp_col = a.snp_col
effect = a.effect
noneffect = a.noneffect
phenotype = a.phenotype
p_val = a.p_val
output = a.output
snp_cov = a.snp_cov

# TODO check paths & files

# Make sure file paths don't end in a /
if software[-1] == "/":
	software = software[:-1]
if model[-1] == "/":
	model = model[:-1]
if output[-1] == "/":
	output = output[:-1]

# Call SPrediXcan
#for file in os.listdir(model):
#	if file.endswith(".db"):
#		tissue = file[:-3]
#		os.system("python3 "+software+"/SPrediXcan.py --model_db_path "+model+"/"+tissue+".db --covariance "+model+"/"+tissue+".txt.gz --gwas_file "+GWAS+" --snp_column "+snp_col+" --effect_allele_column "+effect+" --non_effect_allele_column "+noneffect+" --beta_column "+phenotype+" --pvalue_column "+p_val+" --output_file "+output+"/"+tissue+".csv")

# Call SMultiXcan
os.system("python3 "+software+"/SMulTiXcan.py --models_folder "+model+" --models_name_pattern 'en_(.*).db' --snp_covariance "+snp_cov+" --gwas_file "+GWAS+" --snp_column "+snp_col+" --effect_allele_column "+effect+" --non_effect_allele_column "+noneffect+" --beta_column "+phenotype+" --pvalue_column "+p_val+" --metaxcan_folder "+output+" --metaxcan_filter '.*csv' --snp_covariance "+snp_cov+" --output "+output+"/SMulTiXcan.txt")
