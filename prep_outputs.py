#Import necessary packages
import pandas as pd
import argparse
from os import listdir
from os.path import isfile, join

#combine (S)PrediXcan outputs into single dataframe
def combine_assoc(assoc_out_dir, gwas):
  files = [f for f in listdir(assoc_out_dir) if isfile(join(assoc_out_dir, f))]
  full_paths = []
  for f in files:
    path = assoc_out_dir+f
    full_paths.append(path)
  df_list = []
  for i in range(0, len(full_paths)):
    file = full_paths[i]
    tiss = files[i]
    if (gwas):
      assoc = pd.read_csv(file, delimiter = ",")
    else:
      assoc = pd.read_csv(file, delimiter = "\t")
    #add column for tissue
    assoc["tiss"] = tiss
    df_list.append(assoc)
  combo = pd.concat(df_list)
  return combo

#read in (S)MulTiXcan output
def get_multi(multi_out_dir):
  files = [f for f in listdir(multi_out_dir) if isfile(join(multi_out_dir, f))]
  for file in files:
    path = multi_out_dir+file
    multi = pd.read_csv(path, delimiter = "\t")
  return multi
  
#create new data frame with only significant genes, filtered by pval threshold
def get_sig(combo, pval):
  sig = combo.loc[combo['pvalue'] <= float(pval)]
  return sig


#Create flags:
parser = argparse.ArgumentParser()
parser.add_argument("--assoc_out_dir", required=True, help = "directory the PrediXcan association output will go into")
parser.add_argument("--multi_out_dir", required=True, help = "directory the MulTiXcan assocation output will go into")
parser.add_argument("--out_prefix", required=True, help = "prefix for output files")
parser.add_argument("--pheno_prefix", required=True, help = "name of phenotype, will be added to association output file names")
parser.add_argument("--pval", required=True, help = "p-value threshold, will only analyze genes with p-values that meet this threshold")
parser.add_argument("--gwas", action="store_true", help = "optional; specify if gwas_pipeline.py was used")


#parse arguments
p = parser.parse_args()
assoc_out_dir = p.assoc_out_dir
multi_out_dir = p.multi_out_dir
out_prefix = p.out_prefix
pheno_prefix = p.pheno_prefix
pval = p.pval
gwas = p.gwas

#run methods
assoc_combo = combine_assoc(assoc_out_dir, gwas)
multi = get_multi(multi_out_dir)
assoc_sig = get_sig(assoc_combo, pval)
multi_sig = get_sig(multi, pval)

#output dataframes with signifcant genes:
if (gwas):
  assoc_sig.to_csv(out_prefix+"_"+pheno_prefix+"_sassoc_sig.txt", sep = "\t", index = None)
  multi_sig.to_csv(out_prefix+"_"+pheno_prefix+"_smulti_sig.txt", sep = "\t", index = None)
else:
  assoc_sig.to_csv(out_prefix+"_"+pheno_prefix+"_assoc_sig.txt", sep = "\t", index = None)
  multi_sig.to_csv(out_prefix+"_"+pheno_prefix+"_multi_sig.txt", sep = "\t", index = None)

