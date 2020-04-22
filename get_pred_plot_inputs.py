import argparse

#Create flags:
parser = argparse.ArgumentParser()
parser.add_argument("--pheno_path", required=True, help = "path to phenotype file")
parser.add_argument("--pred_out_dir", required=True, help = "directory the prediction output will go into")
parser.add_argument("--out_prefix", required=True, help = "prefix for output files")
parser.add_argument("--pheno_col", required=True, help = "name of column in phenotype file with phenotype data")
parser.add_argument("--pheno_prefix", required=True, help = "name of phenotype, will be added to association output file names")
parser.add_argument("--mashr", action="store_true", help = "specify if mashr models were used")
parser.add_argument("--mesa", action="store_true", help = "specify if mesa models were used")


#Parse arguments inputted by user:
p = parser.parse_args()
pheno_path = p.pheno_path
pred_out_dir = p.pred_out_dir
out_prefix = p.out_prefix
pheno_col = p.pheno_col
pheno_prefix = p.pheno_prefix
if p.mashr:
  model_type = "mashr"
elif p.mesa:
  model_type = "mesa"
else:
  model_type = "en"


print("running get_pred_inputs")


file = open("input_file_names_pred.txt", "w")

file.write(pheno_path + "\n")
file.write(pred_out_dir + "\n")
file.write(out_prefix + "\n")
file.write(pheno_col + "\n")
file.write(model_type + "\n")
file.write(pheno_prefix)
