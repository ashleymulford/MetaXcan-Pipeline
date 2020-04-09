# MetaXcan Pipeline
MetaXcan Pipeline is designed to automate the scripts made by the Im lab at UChicago based on the user input. This pipeline consists of a series of python and R scripts, all of which are run through one main python wrapper script. This pipeline takes either raw genotype and phenotype data or GWAS summary stats and allows users to run (S-)PrediXcan and (S-)MulTiXcan all at once with the model type they prefer. The pipeline will output all dataframes generated by MetaXcan scripts as well as various plots if plotting is specified. 

# Requirments to Run
### Python3 with packages:
- numpy (>=1.11.1)
- scipy (>=0.18.1)
- pandas (>=0.18.1)
- sqlalchemy is needed at some unit tests.
- patsy (>=0.5.0)
- statsmodels (>=0.8.0)
- h5py (>=2.7.1)
- h5py-cache (>=1.0.0)
- bgen_reader (>=3.0.3)
- cyvcf2 (>=0.8.0)

### R 3.6.3 with packages:
- dplyr
- ggplot2
- qqman

### Download MetaXcan Scripts:
 
       git clone https://github.com/hakyimlab/MetaXcan
       
### Download Models:
#### http://predictdb.org/
We are using:
- gtex v8 mashr expression prediction models
- gtex v8 elastic net expression prediction models
- elastic net mesa expression prediction models

After downloading these models make sure to unzip the folders they come in using:

      tar -xvzf folder_name.tar.gz
      
Additionally, be sure to leave the models in the folders them come in once those folders are unzipped. For MESA models, please put them all into one folder (both dbs and covariances). Please leave all covariance files gzipped. 

### Download our MetaXcan Pipeline and test data:

     git clone https://github.com/ashleymulford/MetaXcan-Pipeline

    
# How to Run
### Key Assumption:
This script assumes that outputs will be stored in corresponing directories. Predict.py outputs, PrediXcanAssociation.py outputs, S-PrediXcan.py outputs, MulTiXcan.py output, and S-MulTiXcan.py output must be each be stored in different directories for subsequent plotting to be successful. Please make these directories prior to running and specify them as arugments using the corresponding flags, see wiki for details.

## Using Test Data:


#### For more information on how to run, please refer to our wiki.


