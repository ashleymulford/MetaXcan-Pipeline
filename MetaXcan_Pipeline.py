import os, argparse, GWAS_pipeline

### Parse args
p = argparse.ArgumentParser("Run the proper MetaXcan pipeline based upon input given")
# Argumets required for dosage and GWAS
gen = p.add_argument_group(title="General use flags")
gen.add_argument("-s", "-software", required=True, help="Path to the 'software' directory within the MetaXcan package (see Wiki for download instrucitons)")   # I want to make this default="MetaXcan/software"
gen.add_argument("-d", "--db_dir", required=True, help="Path to the model directory (containing *.db files) upon which to predict")
gen.add_argument("--out_prefix", default='', help="Text to add to the beginning of every file name produced by this run")
model = gen.add_mutually_exclusive_group()
model.add_argument("--mashr", action="store_true", help="Specify if mashr models are being used")
model.add_argument("--mesa", action="store_true", help="Specify if MulTiXcan.py and SMulTiXcan.py should not be run, such as when MESA models are being used")
gen.add_argument("--predi_out_dir", required=True, help="Output from PrediXcan.py or SPrediXcan.py")
gen.add_argument("--multi_out_dir", help="Output from MulTiXcan.py or SMulTiXcan.py")   # Required if not MESA

# Arguments for dosage
dos = p.add_argument_group(title="Dosage",description="Flags for running MetaXcan based on a individual genotypes")
dos.add_argument("--geno_dir", help="Path to the directory containing genotype files in dosage format")   # Required
dos.add_argument("--geno_file_pattern", help="Regular expression decribing how the genotype files, esparated by chromosome, are named")   # Required
dos.add_argument("--sample_path", help="Path to the samples file")   # Required
dos.add_argument("--pheno_path", help="Path to the phenotype file")   # Required
dos.add_argument("--pheno_col", help="Name of the column in the phenotype file with the phenotype data")  # Required
dos.add_argument("--pheno_prefix", default='', help="Name of the phenotype to be added to the beginning of the association output file names")
dos.add_argument("--assoc_out_dir", help="Output from Predict.py, if different from --output") # TODO Required

# Arguments for GWAS
gwas = p.add_argument_group(title="GWAS",description="Flags for running MetaXcan based on GWAS summary statistics")
gwas.add_argument("-g", "--gwas", help="Run SPrediXcan and SMulTiXcan using GWAS summary statistics")
gwas.add_argument("--gwas_file", help="File containing the GWAS summary statistics")
gwas.add_argument("--snp_cov", help="File containing the SNP covariance. This normally comes with the model download and usually ends with _covariance.txt)")
cutoff = gwas.add_mutually_exclusive_group()   # TODO Which does Dr. Wheeler use?
cutoff.add_argument("--cutoff_condition_number", type=int, help="Condition number of eigen values to use when truncated SVD components")
cutoff.add_argument("--cutoff_eigen_ratio", default=0.4, type=float, help="Ratio of eigenvalues to the max eigenvalue, as threshold to use when truncating SVD components")
cutoff.add_argument("--cutoff_threshold", type=float, help="Threshold of variance eigenvalues when truncating SVD")
cutoff.add_argument("--cutoff_trace_ratio", type=float, help="Ratio of eigenvalues to trace, to use when truncating SVD")
gwas.add_argument("--snp_col", default="variant_id", help="Name of the column in the GWAS summary statistics with the SNP data")
gwas.add_argument("--effect_col", default="effect_allele", help="Name of the column in the GWAS summary statistics with the effect allele")
gwas.add_argument("--noneffect_col", default="noneffect_allele", help="Name of the column in the GWAS summary statistics with the noneffect allele")
gwas.add_argument("--phenotype_col", "--beta_col", default="beta", help="Name of the column in the GWAS summary statistics with the phenotype data")
gwas.add_argument("-p", "--p_val_col", default="p_value", help="Name of the column in the GWAS summary statistics with the p-values")

arg=p.parse_args()
### Test for valid input
# Warn if -software doesn't end with software
# Raise exception if not GWAS summary stat
# Raise exception if not dosage format

### Methods for running next script
# Gets input ready and runs dosage_pipeline.py
def runDosage():
	pred_out_dir = arg.pred_out_dir if arg.pred_out_dir else arg.output
	assoc_out_dir = arg.assoc_out_dir if arg.assoc_out_dir else arg.output
	multi_out_dir = arg.multi_out_dir if arg.multi_out_dir else arg.output
	model_type = " --mashr" if arg.mashr else " --mesa" if arg.mesa else ""

	# TODO Mesa can't run MultiXcan or SMultiXcan

	os.system("python3 dosage_pipeline.py --db_dir "+arg.db_dir+" --scripts_dir "+arg.software+" --geno_dir "+arg.geno_dir+
            " --geno_file_pattern '"+arg.geno_file_pattern+"' --sample_path "+arg.sample_path+" --out_prefix "+arg.out_prefix+
            " --pheno_path "+arg.pheno_path+" --pheno_col "+arg.pheno_col+" --pheno_prefix "+arg.pheno_col+" --pred_out_dir "+pred_out_dir+
            " --assoc_out_dir "+assoc_out_dir+" --multi_out_dir "+multi_out_dir+model_type)

# Gets input ready and runs GWAS_pipeline.py
def runGWAS():
	cutoff = "--cutoff_condition_number "+str(arg.cutoff_condition_number) if arg.cutoff_condition_number else \
		 "--cutoff_threshold "+str(arg.cutoff_threshold) if arg.cutoff_threshold else \
		 "--cutoff_trace_ratio "+str(arg.cutoff_trace_ratio) if arg.cutoff_trace_ratio else \
		 "--cutoff_eigen_ratio "+str(arg.cutoff_eigen_ratio)

	os.system("python3 GWAS_pipeline.py --db_dir "+arg.db_dir+" --scripts_dir "+arg.software+" -g "+arg.gwas_file+cutoff+
            " --snp_cov "+arg.snp_cov+" --snp_col "+arg.snp_col+" --effect "+arg.effect_col+" --noneffect "+arg.noneffect_col+
            " --beta "+arg.beta_col+" -p "+arg.p+" -o "+arg.o+" --out_prefix "+arg.out_prefix)

if arg.force_dosage or (arg.geno_dir and arg.geno_file_pattern and arg.sample_path and arg.pheno_path and arg.pheno_col):
	if arg.g:
		warnings.warn("GWAS file (-g, --gwas_file) specified, but will not be used")
	if arg.snp_cov:
		warnings.warn("SNP covariance file (--snp_cov) speficied, but will not be used")
	if arg.cutoff_condition_number or arg.cutoff_eigen_ratio or arg.cutoff_threshold or arg.cutoff_trace_ratio:
		warnings.warn("Cutoff (--cutoff_...) speficied, but will not be used")
	if arg.snp_col:
		warnings.warn("SNPs column name (--snp_col) specified, but will not be used")
	if arg.effect_col:
		warnings.warn("Effect allele column name (--effect_col) specified, but will not be used")
	if arg.noneffect_col:
		warnings.warn("Non-effect allele column name (--noneffect_col) specified, but will not be used")
	if arg.beta_col:
		warnings.warn("Phenotype column name (--phenotype_col, --beta_col) specified, but will not be used")
	if arg.p:
		warnings.warn("P-value column name (-p, --p_val_col) specified, but will not be used")

	runDosage()

elif arg.force_gwas or (arg.g and arg.snp_cov and (arg.cutoff_condition_number or arg.cutoff_eigen_ratio or arg.cutoff_threshold or arg.cutoff_trace_ratio)):
	if arg.geno_dir:
		warnings.warn("Genotypes file (--geno_dir) specified, but will not be used")
	if arg.geno_file_pattern:
		warnings.warn("Genotypes file pattern (--geno_file_pattern) specified, but will not be used")
	if arg.sample_path:
		warnings.warn("Samples file (--sample_path) specified, but will not be used")
	if arg.pheno_path:
		warnings.warn("Phenotype file (--pheno_path) specified, but will not be used")
	if arg.pheno_col:
		warnings.warn("Phenotype column name (--pheno_col) specified, but will not be used")
	if arg.mashr or arg.mesa:
		warnings.warn("Model type (--mashr, --mesa) specified, but will not be used")
	# TODO warn about other output options or add other options to GWAS_pipeline.py

	runGWAS()

if __name__ == "__main__":
	
