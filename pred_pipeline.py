import os
import argparse

#Method to run Predict.py, loops through all dbs specified
def predict(db_dir, mashr, scripts_dir, geno_path, dos_type, sample_path, out_prefix):
  os.system("for db in " + db_dir + "*.db;   do    prefix=${db#" + db_dir + "};   prefix=${prefix%.db};   python3 " + scripts_dir + "Predict.py --model_db_path $db   " + mashr + "   --vcf_genotypes " + geno_path + "   --vcf_mode " + dos_type + "   --text_sample_ids " + sample_path + "   --prediction_output predict_output/" + out_prefix + "_${prefix}_predict.txt   --prediction_summary_output predict_output/" + out_prefix + "_${prefix}_summary.txt   --verbosity 9   --throw; done")
  
db_dir = "/data/amulford/gtex_v8_elastic_net/eqtl_dbs/"
scripts_dir = "/data/amulford/MetaXcan/software/"
geno_path = "/data/amulford/genotypes/YRI_pred_dosages.txt.gz"
dos_type = "genotyped"
sample_path = "/data/amulford/genotypes/samples.txt"
out_prefix = "YRI"

#Method to run  PrediXcanAssociation.py, loops through all predict output files (based on dbs)
def associate(db_dir, scripts_dir, out_prefix, pheno_path, pheno_col, pheno_prefix):
  os.system("for db in " + db_dir + "*.db;   do    prefix=${db#" + db_dir + "};   prefix=${prefix%.db};   python3 " + scripts_dir + "PrediXcanAssociation.py   --expression_file predict_output/" + out_prefix + "_${prefix}_predict.txt   --input_phenos_file " + pheno_path + "   --input_phenos_column " + pheno_col + "   --output assoc_output/" + out_prefix + pheno_prefix + "_${prefix}_association.txt   --verbosity 9   --throw;    done")

pheno_path = "/data/amulford/phenotypes/YRI_cape_bestpheno_noids.txt"
pheno_col = "pheno"
pheno_prefix = "cape"

#Method to run MulTiXcan.py
def multi(scripts_dir, out_prefix, pheno_path, pheno_col, pheno_prefix):
  pattern = "\" " + out_prefix + "_(.*)_predict.txt\""
  os.system("python3 " + scripts_dir + "MulTiXcan.py --expression_folder predict_output --expression_pattern " + pattern + " --input_phenos_file " + pheno_path + " --input_phenos_column " + pheno_col + " --mode linear --output multi_output/" + out_prefix + "_" + pheno_prefix + "_multi.txt")


#Create flags  
parser = argparse.ArgumentParser()
parser.add_argument("--db_dir", required=True, help = "directory the db files are in")
parser.add_argument("--mashr", action="store_true", help = "optional; specify if mashr models are used")
parser.add_argument("--scripts_dir", required=True, help = "directory all MetaXcan scripts are in")
parser.add_argument("--geno_path", required=True, help = "path to genotype file, must be in dosage format")
parser.add_argument("--dosage_genotyped", action="store_true", help = "optional; specify if dosages are genotyped instead of imputed")
parser.add_argument("--sample_path", required=True, help = "path to samples file")
parser.add_argument("--out_prefix", required=True, help = "prefix for output files")
parser.add_argument("--pheno_path", required=True, help = "path to phenotype file")
parser.add_argument("--pheno_col", required=True, help = "name of column in phenotype file with phenotype data")
parser.add_argument("--pheno_prefix", required=True, help = "name of phenotype, will be added to association output file names")

#Parse Arguments
p = parser.parse_args()
#db_dir = p.db_dir
#if p.mashr:
#  mashr = "--model_db_snp_key varID"
#else:
#  masher = ""
#scripts_dir = p.scripts_dir
#geno_path = p.geno_path
#if not p.dosage_genotyped:
#  dos_type = "imputed"
#else:
#  dos_type = "genotyped"
#sample_path = p.sample_path
#out_prefix = p.out_prefix
#pheno_path = p.pheno_path
#pheno_col = p.pheno_col
#pheno_prefix = p.pheno_prefix


#Run methods:
predict(db_dir, mashr, scripts_dir, geno_path, dos_type, sample_path, out_prefix)
associate(db_dir, scripts_dir, out_prefix, pheno_path, pheno_col, pheno_prefix)
multi(scripts_dir, out_prefix, pheno_path, pheno_col, pheno_prefix)



