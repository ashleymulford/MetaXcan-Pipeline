import argparse

#Create flags:
parser = argparse.ArgumentParser()
parser.add_argument("--assoc_out_dir", required=True, help = "directory the PrediXcan Association output will go into")
parser.add_argument("--multi_out_dir", required=True, help = "directory the MulTiXcan output will go into")
parser.add_argument("--out_prefix", required=True, help = "prefix for output files")
parser.add_argument("--pheno_prefix", default = "", help = "Optional, name of phenotype")
parser.add_argument("--chrom_anno_path", required=True, help = "path to bp chromosome annotation file")


#Parse arguments inputted by user:
p = parser.parse_args()
assoc_out_dir = p.assoc_out_dir
multi_out_dir = p.multi_out_dir
out_prefix = p.out_prefix
pheno_prefix = p.pheno_prefix
chrom_anno_path = p.chrom_anno_path


file = open("input_file_names_qqman.txt", "w")

file.write(assoc_out_dir + "\n")
file.write(multi_out_dir + "\n")
file.write(out_prefix + "\n")
file.write(chrom_anno_path + "\n")
file.write(pheno_prefix)
