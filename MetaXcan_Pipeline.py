import os, argparse

### Parse args
p = argparse.ArgumentParser("Run the proper MetaXcan pipeline based upon input given")
# Argumets required for dosage and GWAS
gen = p.add_argument_group(title="General use flags")
gen.add_argument("-s", "-software", required=True, help="Path to the 'software' directory within the MetaXcan package (see Wiki for download instrucitons)")   # I want to make this default="MetaXcan/software"
gen.add_argument("-d", "--db_dir", required=True, help="Path to the model directory (containing *.db files) upon which to predict")
gen.add_argument("-o", "--output", default="MetaXcan_output", help="Path for output files")
gen.add_argument("--out_prefix", default='', help="Text to add to the beginning of every file name produced by this run")
force = gen.add_mutually_exclusive_group()
force.add_argument("--force_dosage", action="store_true", help="Forces the use of the dosage pipeline")
force.add_argument("--force_gwas", action="store_true", help="Forces the use of the GWAS pipeline")
## No MulTiXcan?
## Verbosity/throw?

# Arguments for dosage
dos = p.add_argument_group(title="Dosage",description="Flags for running MetaXcan based on a individual genotypes")
model = dos.add_mutually_exclusive_group()
model.add_argument("--mashr", action="store_true", help="Specify if mashr models are being used")
model.add_argument("--mesa", action="store_true", help="Specify if MESA models are being used")
dos.add_argument("--geno_dir", help="Path to the directory containing genotype files in dosage format")   # Required
dos.add_argument("--geno_file_pattern", help="Regular expression decribing how the genotype files, esparated by chromosome, are named")   # Required
dos.add_argument("--sample_path", help="Path to the samples file")   # Required
dos.add_argument("--pheno_path", help="Path to the phenotype file")   # Required
dos.add_argument("--pheno_col", help="Name of the column in the phenotype file with the phenotype data")  #	TODO Default?
dos.add_argument("--pheno_prefix", default='', help="Name of the phenotype to be added to the beginning of the association output file names")
dos.add_argument("--pred_out_dir", help="Output for the prediction, if different from --output")   # TODO don't these arg names seem backwards?
dos.add_argument("--assoc_out_dir", help="Output for the PrediXcan association, if different from --output")
dos.add_argument("--multi_out_dir", help="Output for the MultiXcan association, if different from --output")

# Arguments for GWAS
gwas = p.add_argument_group(title="GWAS",description="Flags for running MetaXcan based on GWAS summary statistics")
gwas.add_argument("-g", "--gwas_path", help="File containing the GWAS summary statistics")
gwas.add_argument("--snp_cov", help="File containing the SNP covariance. This normally comes with the model download and usually ends with _covariance.txt)")
cutoff = gwas.add_mutually_exclusive_group()   # TODO Which does Dr. Wheeler use?
cutoff.add_argument("--cutoff_condition_number", help="Condition number of eigen values to use when truncated SVD components")
cutoff.add_argument("--cutoff_eigen_ratio", help="Ratio of eigenvalues to the max eigenvalue, as threshold to use when truncating SVD components")
cutoff.add_argument("--cutoff_threshold", help="Threshold of variance eigenvalues when truncating SVD")
cutoff.add_argument("--cutoff_trace_ratio", help="Ratio of eigenvalues to trace, to use when truncating SVD")
gwas.add_argument("--snp_col", default="variant_id", help="Name of the column in the GWAS summary statistics with the SNP data")
gwas.add_argument("--effect_col", default="effect_allele", help="Name of the column in the GWAS summary statistics with the effect allele")
gwas.add_argument("--noneffect_col", default="noneffect_allele", help="Name of the column in the GWAS summary statistics with the noneffect allele")
gwas.add_argument("--phenotype", "--beta", default="beta", help="Name of the column in the GWAS summary statistics with the phenotype data")
gwas.add_argument("-p", "--p_val", default="p_value", help="Name of the column in the GWAS summary statistics with the p-values")

arg=p.parse_args()
### Test for valid input
if arg.force_dosage and arg.force_gwas:
	raise ValueError("Use of both --force_dosage and --force_gwas is illegal")
# Warn if -software doesn't end with software

def run_dosage():
	os.system("dosage_pipeline.py ")
