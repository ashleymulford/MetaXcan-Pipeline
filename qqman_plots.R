#Import necessary libraries
library(data.table)
library(dplyr)
library(qqman)
library(colorspace)

#function to paste
"%&%" = function(a,b) paste(a,b,sep="")

#Create color vector
colors<-qualitative_hcl(3,"Dark3")

input_files<-fread("input_file_names_qqman.txt", header = FALSE)

assoc_dir<-input_files$V1[1]
multi_dir<-input_files$V1[2]
out_prefix<-input_files$V1[3]
chrom_anno_path<-input_files$V1[4]
if (exists(input_files$V1[5])){
  pheno_prefix<-input_files$V1[5]
}


sig_files<-fread("sig_file_names.txt", header = FALSE)

fnames<-sig_files$V1

chrom<-fread(chrom_anno_path)

for (fname in fnames){
  sig_hits <- fread(fname)
  
  if("tiss" %in% names(sig_hits)) {
    tiss<-sig_hits$tiss[1]
    assoc_model_path<-assoc_dir %&% tiss
    model<-fread(assoc_model_path)
  } else {
    multi_name<-sub("_sig", "", fname)
    multi_model_path<-multi_dir %&% multi_name
    model<-fread(multi_model_path)
  }

  if("gene_name" %in% names(sig_hits)) {
    model_chrom<- left_join(model, chrom, by = c("gene" = "ensg_ids", "gene_name" = "gene_name"))
  } else {
    model_chrom<-left_join(model, chrom, by = c("gene" = "ensg_ids"))
  }
  
  if("status" %in% names(model_chrom)) {
    model_chrom<-select(model_chrom, - "status")
  }

  model_chrom_small<-model_chrom[complete.cases(model_chrom), ]
  
  fname_small<-sub("_sig.txt", "", fname)
  
  png(filename = fname_small %&% ".qqplot.png", res=100)
  qq(model_chrom$pvalue)
  dev.off()

  if(dim(model_chrom_small)[1] != 0) {
    png(filename = fname_small %&% ".manplot.png", res=100)
    manhattan(model_chrom_small, chr = "chr", bp = "pos", p = "pvalue", col = colors)
    dev.off()
  }
  
}
  


