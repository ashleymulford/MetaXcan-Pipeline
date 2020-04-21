import os, argparse, warnings

# #################################
# ### Argument defining/parsing ###
# #################################
p = argparse.ArgumentParser("Run the proper MetaXcan pipeline based upon input given")
# Argumets required for dosage and GWAS
gen = p.add_argument_group(title="General use flags")
gen.add_argument("-s", "--software", required=True, help="Path to the 'software' directory within the MetaXcan package (see Wiki for download instrucitons)")
gen.add_argument("-d", "--db_dir", required=True, help="Path to the model directory (containing *.db files) upon which to predict")
gen.add_argument("--out_prefix", default='', help="Text to add to the beginning of every file name produced by this run")
model = gen.add_mutually_exclusive_group()
model.add_argument("--mashr", action="store_true", help="Specify if mashr models are being used")
model.add_argument("--mesa", action="store_true", help="Specify if MulTiXcan.py and SMulTiXcan.py should not be run, such as when MESA models are being used")
gen.add_argument("--assoc_out_dir", required=True, help="Output from PrediXcan.py or SPrediXcan.py")
gen.add_argument("--multi_out_dir", help="Output from MulTiXcan.py or SMulTiXcan.py")
gen.add_argument("--pval", type=float, help="P-value cutoff for use in graphing results")
gen.add_argument("--no_plot", action="store_true", help="Prevents the pipeline from generating plots")
gen.add_argument("--chrom_anno_path", default='', help="Path to chrom_anno_gtexv*.txt for plotting")

# Arguments for dosage
dos = p.add_argument_group(title="Dosage",description="Flags for running MetaXcan based on a individual genotypes")
dos.add_argument("--geno_dir", default='', help="Path to the directory containing genotype files in dosage format")
dos.add_argument("--geno_file_pattern", help="Regular expression decribing how the genotype files, esparated by chromosome, are named")
dos.add_argument("--sample_path", default='', help="Path to the samples file")
dos.add_argument("--pheno_path", default='', help="Path to the phenotype file")
dos.add_argument("--pheno_col", help="Name of the column in the phenotype file with the phenotype data")
dos.add_argument("--pheno_prefix", default='', help="Name of the phenotype to be added to the beginning of the association output file names")
dos.add_argument("--predi_out_dir", help="Output from Predict.py")

# Arguments for GWAS
gwas = p.add_argument_group(title="GWAS",description="Flags for running MetaXcan based on GWAS summary statistics")
gwas.add_argument("--gwas", action="store_true", help="Run SPrediXcan and SMulTiXcan using GWAS summary statistics")
gwas.add_argument("--gwas_file", default='', help="File containing the GWAS summary statistics")
gwas.add_argument("--snp_cov", default='', help="File containing the SNP covariance. This normally comes with the model download and usually ends with _covariance.txt)")
cutoff = gwas.add_mutually_exclusive_group()
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


# #####################################
# ### Test for valid general inputs ###
# #####################################
## File paths shouldn't end in / ##
if arg.software[-1] == "/":
    arg.software = arg.software[:-1]
if arg.db_dir[-1] == "/":
    arg.db_dir = arg.db_dir[:-1]
if arg.assoc_out_dir[-1] == "/":
    arg.assoc_out_dir = arg.assoc_out_dir[:-1]
if arg.multi_out_dir[-1] == "/":
    arg.multi_out_dir = arg.multi_out_dir[:-1]
if arg.geno_dir and arg.geno_dir[-1] == "/":
    arg.geno_dir = arg.geno_dir[:-1]
if arg.predi_out_dir and arg.predi_out_dir[-1] == "/":
    arg.predi_out_dir = arg.predi_out_dir[:-1]

## Exceptions ##
# software doesn't contain PrediXcan.py, Predict.py, MulTiXcan.py, SPrediXcan.py, SMultiXcan.py
if not all(elem in os.listdir(arg.software) for elem in ["PrediXcanAssociation.py", "Predict.py", "MulTiXcan.py", "SPrediXcan.py", "SMulTiXcan.py"]):
    raise FileNotFoundError("Folder defined by --software does not contain the necessary files. It must be pointing to the software folder from the MetaXcan: https://github.com/hakyimlab/MetaXcan/tree/master/software")
# no dbs
if not any(file.endswith(".db") for file in os.listdir(arg.db_dir)):
    raise FileNotFoundError("Model folder defined by --db_dir does not contain *.db files")
# invalid output dir
if not os.path.exists(arg.assoc_out_dir):
    raise NotADirectoryError("PrediXcan.py output folder defined by --assoc_out_dir does not exist")
# if you're not running mesa, and you didn't define a valid multi_out_dir
if not arg.mesa and not os.path.exists(arg.multi_out_dir):
    raise IOError("MulTiXcan.py output folder defined by --multi_out_dir does not exist. If you don't want to run MulTiXcan, use --mesa.")

## Warnings
# Warn if --software doesn't end with software
if arg.software[-8:] != "software":
    warnings.warn("Folder defined by --software is not named 'software'. If your code doesn't run, re-fork the MetaXcan github and point --software at the software folder in the MetaXcan folder")
# Warn if --mesa and --multi_out_dir were used
if arg.mesa and arg.multi_out_dir:
    warnings.warn("--mesa flag used and --multi_out_dir defined. Due to the --mesa flag, MulTiXcan won't be run. Therefore, --multi_out_dir won't be used")

# ###################################
# ### Run PrediXcan and MulTiXcan ###
# ###################################
if arg.gwas:
    ## Generate exceptions if proper flags were not defined
    # invalid arg.gwas_file
    if not os.path.isfile(arg.gwas_file):
        raise FileNotFoundError("File defined by --gwas_file does not exist while using --gwas")
    # arg.snp_cov
    if not os.path.isfile(arg.snp_cov):
        raise FileNotFoundError("File defined by --snp_cov does not exist while using --gwas")

    ## Generate warnings if dosage flags were provided when GWAS is run ##
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
    if arg.mashr:
        warnings.warn("Model type (--mashr) specified, but will not be used")
    if arg.predi_out_dir:
        warnings.warn("Predict.py output (--predi_out_dir) specified, but will not be used")
    if arg.pheno_prefix:
        warnings.warn("Phenotype prefix (--pheno_prefix) specified, but will not be used")

    cutoff = " --cutoff_condition_number "+str(arg.cutoff_condition_number) if arg.cutoff_condition_number else \
             " --cutoff_threshold "+str(arg.cutoff_threshold) if arg.cutoff_threshold else \
             " --cutoff_trace_ratio "+str(arg.cutoff_trace_ratio) if arg.cutoff_trace_ratio else \
             " --cutoff_eigen_ratio "+str(arg.cutoff_eigen_ratio)
    mesa = " --mesa" if arg.mesa else ""
    
    os.system("python3 GWAS_pipeline.py --db_dir "+arg.db_dir+" --scripts_dir "+arg.software+" --gwas_file "+arg.gwas_file+cutoff+
              " --snp_cov "+arg.snp_cov+" --snp_col "+arg.snp_col+" --effect "+arg.effect_col+" --noneffect "+arg.noneffect_col+
              " --beta "+arg.phenotype_col+" --p_val "+arg.p_val_col+" --assoc_out_dir "+arg.assoc_out_dir+" --multi_out_dir "+arg.multi_out_dir+
              " --out_prefix '"+arg.out_prefix+"'"+mesa)
else:
    ## Generate exceptions if proper flags were not defined
    # not valid arg.geno_dir
    if not os.path.exists(arg.geno_dir):
        raise NotADirectoryError("Genotype file folder (--geno_dir) is invalid while not using --gwas")
    # arg.geno_file_pattern
    if not arg.geno_file_pattern:
        raise ValueError("Genotype file pattern (--geno_file_pattern) is undefined while not using --gwas")
    # arg.sample_path
    if not os.path.isfile(arg.sample_path):
        raise FileNotFoundError("Sample file (--sample_path) is invalid while not using --gwas")
    # arg.pheno_path
    if not os.path.isfile(arg.pheno_path):
        raise FileNotFoundError("Phenotype file (--pheno_path) is invalid while not using --gwas")
    # arg.pheno_col
    if not arg.pheno_col:
        raise ValueError("Phenotype column (--pheno_col) is undefined while not using --gwas")
    # arg.predi_out_dir
    if not os.path.exists(arg.predi_out_dir):
        raise NotADirectoryError("Predict.py output folder (--predi_out_dir) is invalid while not using --gwas")

    ## Generate warnings if genotype flags were provided when dosage is run ##
    if arg.gwas:
         warnings.warn("GWAS file (--gwas_file) specified, but will not be used")
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
    if arg.phenotype_col:
         warnings.warn("Phenotype column name (--phenotype_col, --beta_col) specified, but will not be used")
    if arg.p_val_col:
        warnings.warn("P-value column name (-p, --p_val_col) specified, but will not be used")

    ## Format flags and run dosage_pipeline.py ##
    model_type = " --mashr" if arg.mashr else " --mesa" if arg.mesa else ""

    os.system("python3 dosage_pipeline.py --db_dir "+arg.db_dir+" --scripts_dir "+arg.software+" --geno_dir "+arg.geno_dir+
              " --geno_file_pattern '"+arg.geno_file_pattern+"' --sample_path "+arg.sample_path+" --out_prefix "+arg.out_prefix+
              " --pheno_path "+arg.pheno_path+" --pheno_col "+arg.pheno_col+" --pheno_prefix "+arg.pheno_col+" --pred_out_dir "+arg.pred_out_dir+
              " --assoc_out_dir "+arg.assoc_out_dir+" --multi_out_dir "+arg.multi_out_dir+model_type)


# #################################
# ### Prep outputs for plotting ###
# #################################
gwas_flag = " --gwas" if arg.gwas else ""
pval = " --pval "+arg.pval if arg.pval else ""
os.system("python3 prep_outputs.py --assoc_out_dir "+arg.assoc_out_dir+" --multi_out_dir "+arg.multi_out_dir+
          " --out_prefix '"+arg.out_prefix+"' --pheno_prefix '"+arg.pheno_prefix+"'"+pval+gwas_flag)


# ####################
# ### Run plotting ###
# ####################
if not arg.no_plot:
    if not os.path.isfile(arg.chrom_anno_path):
        raise FileNotFoundError("Chrom_anno file (--chrom_anno_path) is invalid while attempting to plot")
    os.system("python3 get_qqman_plot_inputs.py --assoc_out_dir "+arg.assoc_out_dir+" --multi_out_dir "+arg.multi_out_dir+
              " --out_prefix "+arg.out_prefix+" --pheno_prefix "+arg.pheno_prefix+" --chrom_anno_path "+arg.chrom_anno_path)
    os.system("Rscript qqman_plots.R")

    if not arg.gwas:
        os.system("python3 get_pred_plot_inputs.py --pheno_path "+arg.pheno_path+" --pheno_col "+arg.pheno_col+
                  " --pred_out_dir "+arg.pred_out_dir+" --pheno_prefix "+arg.pheno_prefix+" --out_prefix"+arg.out_prefix)
        os.system("Rscript pred_express_plots.R")
