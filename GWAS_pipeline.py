import os, argparse

# Method for running both
def runGWAS_pipeline(software, model, GWAS, snp_col, effect, noneffect, phenotype, p_val, snp_cov, cutoff, out_prefix, mesa, assoc_out_dir, multi_out_dir):
	# Call SPrediXcan
	for file in os.listdir(model):
        	if file.endswith(".db"):
                	tissue = file[:-3]
                	os.system("python3 "+software+"/SPrediXcan.py --model_db_path "+model+"/"+tissue+".db --covariance "+model+"/"+tissue+".txt.gz"+
                            " --gwas_file "+GWAS+" --snp_column "+snp_col+" --effect_allele_column "+effect+" --non_effect_allele_column "+noneffect+
                          	" --beta_column "+phenotype+" --pvalue_column "+p_val+" --output_file "+assoc_out_dir+"/"+out_prefix+tissue+"_predict.csv"+
                     				" --verbosity 9 --throw")
	if not mesa:
		# Call SMultiXcan
		os.system("python3 "+software+"/SMulTiXcan.py --models_folder "+model+" --models_name_pattern '(.*).db' --snp_covariance "+snp_cov+
			        " --gwas_file "+GWAS+" --snp_col "+snp_col+" --effect_allele_column "+effect+" --non_effect_allele_column "+noneffect+
			        " --beta_column "+phenotype+" --pvalue_column "+p_val+" --metaxcan_folder "+predi_out_dir+" --verbosity 9 --throw"+
			        " --metaxcan_filter '"+out_prefix+"(.*)_predict.csv' --metaxcan_file_name_parse_pattern '"+out_prefix+"()(.*)_predict.csv'"+
			        " --output "+multi_out_dir+"/SMulTiXcan.txt"+cutoff)

# Parse args
p = argparse.ArgumentParser()
p.add_argument("-d","--db_dir", required=True, help="Directory for the model to predict against (both *.db and *.txt.gz files")
p.add_argument("-s","--scripts_dir", default="MetaXcan/software", help="Directory containing the MetaXcan scripts, called 'software' in the MetaXcan package")
p.add_argument("-g","--gwas_file", required=True, help="File containing the GWAS summary statistics (*.assoc.txt.gz)")
p.add_argument("--assoc_out_dir", default="MetaPipeOut", help="Output folder for SPrediXcan.py")
p.add_argument("--multi_out_dir", default="MetaPipeOut", help="Output folder for SMultiXcan.py")
p.add_argument("--snp_col", default="variant_id", help="Name of the column containing SNP data in the GWAS summary statistics")
p.add_argument("--effect","--effect_col", default="effect_allele", help="Name of the column containing the effect allele data in the GWAS summary statistics")
p.add_argument("--noneffect","--noneffect_col", default="noneffect_allele", help="Name of the column containing the noneffect allele in the GWAS summary statistics")
p.add_argument("--phenotype", "--beta", default="beta", help="Name of the column containing the phenotype data in the GWAS summary statistics")
p.add_argument("-p","--p_val", default="p_value", help="Name of the column containing the p-value in the GWAS summary statistics")
p.add_argument("--snp_cov", help="File containing SNP covariance which comes in the model download (*_covariance.txt)")
cutoff = p.add_mutually_exclusive_group()
cutoff.add_argument("--cutoff_condition_number", type=int, help="Condition number of eigen values to use when truncated SVD components")
cutoff.add_argument("--cutoff_eigen_ratio", default=None, type=float, help="Ratio of eigenvalues to the max eigenvalue, as threshold to use when truncating SVD components")   # Default
cutoff.add_argument("--cutoff_threshold", type=float, help="Threshold of variance eigenvalues when truncating SVD")
cutoff.add_argument("--cutoff_trace_ratio", type=float, help="Ratio of eigenvalues to trace, to use when truncating SVD")
p.add_argument("--out_prefix", default='', help="Text to add to the beginning of every file name produced by this run")
p.add_argument("--mesa", action="store_true", help="Flag should be used if mesa models are given. MulTiXcan will not be run.")

a = p.parse_args()
# Needed args
software = a.scripts_dir
model = a.db_dir
GWAS = a.gwas_file
snp_col = a.snp_col
effect = a.effect
noneffect = a.noneffect
phenotype = a.phenotype
p_val = a.p_val
snp_cov = a.snp_cov
cutoff = a.cutoff_threshold
out_prefix = a.out_prefix
mesa = a.mesa
assoc_out_dir = a.assoc_out_dir if a.assoc_out_dir else a.output if a.output else None
multi_out_dir = a.multi_out_dir if a.multi_out_dir else a.output if a.output else None
cutoff = " --cutoff_condition_number "+str(a.cutoff_condition_number) if a.cutoff_condition_number else \
	 " --cutoff_threshold "+str(a.cutoff_threshold) if a.cutoff_threshold else \
	 " --cutoff_trace_ratio "+str(a.cutoff_trace_ratio) if a.cutoff_trace_ratio else \
	 " --cutoff_eigen_ratio "+str(a.cutoff_eigen_ratio)

# Check paths & files
if assoc_out_dir is None:
	raise ValueError("SPrediXcan.py output destination must be defined by --assoc_out_dir")
if not mesa:
	if multi_out_dir is None:
		raise ValueError("SMultiXcan.py output destination must be defined by --multi_out_dir")
	if not snp_cov:
		raise ValueError("If SMultiXcan.py is going to be run, --snp_cov must be defined. Use --mesa if SMulTiXcan.py should not be run")
	if cutoff[-4:] == "None":
		print("Cutoff was not defined, 0.4 eigen ratio cutoff will be used")
		cutoff = " --cutoff_eigen_ratio 0.4"
# TODO check if software is there
# TODO check output paths
# TODO check GWAS file?
# TODO check column names?

# Make sure file paths don't end in a /
if software[-1] == "/":
	software = software[:-1]
if model[-1] == "/":
	model = model[:-1]
if assoc_out_dir[-1] == "/":
	assoc_out_dir = assoc_out_dir[:-1]
if multi_out_dir[-1] == "/":
	multi_out_dir = multi_our_dir[:-1]

if __name__ == "__main__":
	runGWAS_pipeline(software=software, model=model, snp_cov=snp_cov, GWAS=GWAS, snp_col=snp_col, effect=effect, noneffect=noneffect, \
			 phenotype=phenotype, p_val=p_val, cutoff=cutoff, mesa=mesa, assoc_out_dir=assoc_out_dir, multi_out_dir=multi_out_dir, \
			 out_prefix=out_prefix)
