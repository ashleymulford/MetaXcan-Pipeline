import os
import argparse

#Method for Predict.py
def predict(db_dir, mashr, scripts_dir, geno_path, sample_path, pred_out_dir, out_prefix):
  os.system("for db in " + db_dir + "*.db;   do    prefix=${db#" + db_dir + "};   prefix=${prefix%.db};   python3 " + scripts_dir + "Predict.py --model_db_path $db   " + mashr + "   --text_genotypes " + geno_path + "   --text_sample_ids " + sample_path + "   --prediction_output " + pred_out_dir + out_prefix + "_${prefix}_predict.txt   --prediction_summary_output " + pred_out_dir + out_prefix + "_${prefix}_summary.txt   --verbosity 9   --throw; done")
  
#Testing:
#db_dir = "/data/amulford/gtex_v8_elastic_net/eqtl_dbs/"
#mashr = ""
#scripts_dir = "/data/amulford/MetaXcan/software/"
#geno_path = "/data/amulford/dosages/chr*.txt.gz"
#sample_path = "/data/amulford/genotypes/samples.txt"
#out_prefix = "YRI"
#pred_out_dir = "predict_output/"


#Method for PrediXcanAssociation.py
def associate(db_dir, scripts_dir, pred_out_dir, out_prefix, pheno_path, pheno_col, pheno_prefix, assoc_out_dir):
  os.system("for db in " + db_dir + "*.db;   do    prefix=${db#" + db_dir + "};   prefix=${prefix%.db};   python3 " + scripts_dir + "PrediXcanAssociation.py   --expression_file " + pred_out_dir + out_prefix + "_${prefix}_predict.txt   --input_phenos_file " + pheno_path + "   --input_phenos_column " + pheno_col + "   --output " + assoc_out_dir + out_prefix + "_" + pheno_prefix + "_${prefix}_association.txt   --verbosity 9   --throw;    done")

#Testing:
#pheno_path = "/data/amulford/phenotypes/YRI_cape_pheno_edit.txt"
#pheno_col = "PHENO_CAPE"
#pheno_prefix = "cape"
#assoc_out_dir = "assoc_output/"
#multi_out_dir = "multi_output/"


#Method for MulTiXcan.py
def multi(scripts_dir, pred_out_dir, out_prefix, pheno_path, pheno_col, pheno_prefix, multi_out_dir):
  pattern = "\" " + out_prefix + "_(.*)_predict.txt\""
  os.system("python3 " + scripts_dir + "MulTiXcan.py --expression_folder " + pred_out_dir + " --expression_pattern " + pattern + " --input_phenos_file " + pheno_path + " --input_phenos_column " + pheno_col + " --mode linear --output " + multi_out_dir + out_prefix + "_" + pheno_prefix + "_multi.txt")



#Create flags:
parser = argparse.ArgumentParser()
parser.add_argument("--db_dir", required=True, help = "directory the db files are in")
parser.add_argument("--mashr", action="store_true", help = "optional; specify if mashr models are used")
parser.add_argument("--scripts_dir", required=True, help = "directory all MetaXcan scripts are in")
parser.add_argument("--geno_path", required=True, help = "path to genotype file, must be in dosage format")
parser.add_argument("--sample_path", required=True, help = "path to samples file")
parser.add_argument("--out_prefix", required=True, help = "prefix for output files")
parser.add_argument("--pheno_path", required=True, help = "path to phenotype file")
parser.add_argument("--pheno_col", required=True, help = "name of column in phenotype file with phenotype data")
parser.add_argument("--pheno_prefix", required=True, help = "name of phenotype, will be added to association output file names")
parser.add_argument("--pred_out_dir", required=True, help = "directory the prediction output will go into")
parser.add_argument("--assoc_out_dir", required=True, help = "directory the predixcan association output will go into")
parser.add_argument("--multi_out_dir", required=True, help = "directory the multixcan assocation output will go into")


#Parse arguments inputted by user:
p = parser.parse_args()
db_dir = p.db_dir
if p.mashr:
  mashr = "--model_db_snp_key varID"
else:
  mashr = ""
scripts_dir = p.scripts_dir
geno_path = p.geno_path
sample_path = p.sample_path
out_prefix = p.out_prefix
pheno_path = p.pheno_path
pheno_col = p.pheno_col
pheno_prefix = p.pheno_prefix
pred_out_dir = p.pred_out_dir
assoc_out_dir = p.assoc_out_dir
multi_out_dir = p.multi_out_dir


#Run scripts:
predict(db_dir, mashr, scripts_dir, geno_path, sample_path, pred_out_dir, out_prefix)
associate(db_dir, scripts_dir, pred_out_dir, out_prefix, pheno_path, pheno_col, pheno_prefix, assoc_out_dir)
multi(scripts_dir, pred_out_dir, out_prefix, pheno_path, pheno_col, pheno_prefix, multi_out_dir)

