#Import necessary libraries
library(data.table)
library(dplyr)
library(ggplot2)

#function to paste
"%&%" = function(a,b) paste(a,b,sep="")

input_files<-fread("input_file_names_pred.txt", header = FALSE)

pheno_path<-input_files$V1[1]
pred_dir<-input_files$V1[2]
out_prefix<-input_files$V1[3]
pheno_col<-input_files$V1[4]
model_type<-input_files$V1[5]
pheno_prefix<-input_files$V1[6]

#Pheno file:
x_pheno<-fread(pheno_path)
x_pheno<-select(x_pheno, pheno_col)

sig_files<-fread("sig_file_names.txt", header = FALSE)

names<-sig_files$V1

for (name in names){
  
  sig_hits <- fread(name)
  top_hit <- sig_hits[1, ]
  
  is_assoc<-grepl("assoc", name, fixed = TRUE)
  is_multi<-grepl("multi", name, fixed = TRUE)
  
  if (is_assoc) {
    tiss<-top_hit$tiss
    pred_file<-sub("association", "predict", tiss)
    pred_file<-sub(pheno_prefix %&% "_" , "", pred_file)
  }
  
  
  if (is_multi) {
    tiss<-top_hit$m_i_best
    pred_file<-paste(out_prefix, "_", model_type, "_", tiss, "_predict.txt", sep = "")
  }
  
  
  gene_id<-top_hit$gene
  
  #Predicted Expression file:
  y_pred_matrix<-fread(pred_dir %&% pred_file)
  
  gene_exp<-select(y_pred_matrix, gene_id)
  
  xy_info<-cbind(x_pheno, gene_exp)
  
  
  #Make Plot:
  pdf(out_prefix %&% "_" %&% pheno_prefix %&% "_" %&% gene_id %&% "_predicted_expression.pdf")
  print(ggplot(xy_info, aes_string(x = pheno_col , y = gene_id)) +
    geom_jitter(size = 0.75, color = "#ec328c") + 
    geom_density_2d(color = "#1EA1E7") + 
    stat_smooth(method="lm", se = TRUE, fullrange = TRUE, color = "#4DB94D") + 
    scale_x_continuous(name = "Predicted gene expression") + 
    scale_y_continuous(name = pheno_col) + 
    theme_bw() + 
    theme(text = element_text(size = 12), plot.title = element_text(hjust = 0.5)) +
    ggtitle(out_prefix %&% " " %&% pheno_prefix %&% " " %&% gene_id %&% " Predicted Expression"))
  dev.off()
  
}
