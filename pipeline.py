import os
import argparse


def predict(db_dir, scripts_dir, geno_path, sample_path, out_prefix):
  os.system("for db in " + db_dir + "*.db;   do    prefix=${db#" + db_dir + "};   prefix=${prefix%.db};   python3 " + scripts_dir + "Predict.py --model_db_path $db   --vcf_genotypes " + geno_path + "   --vcf_mode genotyped   --text_sample_ids " + sample_path + "   --prediction_output predict_output/" + out_prefix + "_${prefix}_predict.txt   --prediction_summary_output predict_output/" + out_prefix + "_${prefix}_summary.txt   --verbosity 9   --throw; done")
  

db_dir = "/data/amulford/gtex_v8_elastic_net/eqtl_dbs/"
scripts_dir = "/data/amulford/MetaXcan/software/"
geno_path = "/data/amulford/genotypes/YRI_pred_dosages.txt.gz"
sample_path = "/data/amulford/genotypes/samples.txt"
out_prefix = "YRI"




#def associate():
  #os.system()

pheno_prefix = "pheno"





#def multi():
  #os.system()








#Parse arguments  
parser = argparse.ArgumentParser()
parser.add_argument("--db_dir", required=True, help = "directory the db files are in")
parser.add_argument("--scripts_dir", required=True, help = "directory all MetaXcan scripts are in")
parser.add_argument("--geno_path", required=True, help = "path to genotype file, must be in dosage format")
parser.add_argument("--sample_path", required=True, help = "path to samples file")
parser.add_argument("--out_prefix", required=True, help = "prefix for output files")
parser.add_argument("--pheno_prefix", required=True, help = "name of phenotype, will be added to association output file names")

p = parser.parse_args()

#db_dir = p.db_dir
#scripts_dir = p.scripts_dir
#geno_path = p.geno_path
#sample_path = p.sample_path
#out_prefix = p.out_prefix
#pheno_prefix = p.pheno_prefix


predict(db_dir, scripts_dir, geno_path, sample_path, out_prefix)
#assoc()
#multi()

