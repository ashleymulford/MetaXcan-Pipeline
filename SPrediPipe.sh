software="~/MetaXcan/software"
model_path=
GWAS_file=
snp_col="rs"
effect="allele1"
noneffect="allele0"
phenotype="beta"
p_val="p_wald"
output="~"
other_flags=""


while [ "$1" != "" ]; do
    case $1 in
        -m | --model )          shift
                                model_path=${1%/*}
                                ;;
        --gwas )                shift
				GWAS_file=$1
                                ;;
        --snp )			shift
				snp_col=$1
				;;
	--effect )		shift
				effect=$1
				;;
	--noneffect )		shift
				noneffect=$1
				;;
	--phenotype )		shift
				phenotype=$1
				;;
	--p_val )		shift
				p_val=$1
				;;
	-o | --output )		shift
				output=${1%/*}
				;;
	-s | --software)	shift
				software=${1%/*}
				;;
	-h | --help )           usage
                                exit
                                ;;
        * )                     shift
				other_flags="$other_flags $1 $2"
				shift
                                ;;
    esac
    shift
done

# Check inputs
if [[ ${GWAS_file:(-13)} != ".assoc.txt.gz" ]]; then
	echo "--gwas must point to a .assoc.txt.gz file"
  echo "Given ${GWAS_file##*/}"
	exit 1
elif [[ ! -d $output ]]; then
  echo "Output folder must be a valid, writable destination"
  exit 1
fi

for db in $model_path/*.db; do
  db_file=${db##*/}
  tissue_Name=${db_file%.db}
	covariance=${db%.db}.txt.gz
	python3 $software/SPrediXcan.py --model_db_path $db --covariance $covariance --gwas_file $GWAS_file --snp_column $snp_col --effect_allele_column $effect --non_effect_allele_column $noneffect --beta_column $phenotype --pvalue_column $p_val --output_file $output/$tissue_Name.csv $other_flags
done
