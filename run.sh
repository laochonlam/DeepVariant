# Chr1 Only 
# Find Candidate Variants 
# Classification into 3 labels and generate corresponding images

if [[ $# -lt 2 ]]; then
    echo "Usage: $0 <chr> <start pos> <end pos>"
    exit 1
fi

mkdir -p img
mkdir -p img/het
mkdir -p img/hom-alt
mkdir -p img/ref
echo "[Start]" > log_$1
for (( i=$2; i<$3; i=i+1000000 ))
do
    # Usage find_candidate <chr> <pos> A <bam> <fasta>
    find_candidate/find_candidate.sh $1 ${i} data/elsa.bam data/ucsc.hg19.fasta > candidate_$1.txt
    echo "$i find candidate completed!" >> log_$1
    # Usage label_classification.py <vcf> <candidate> <start position>
    python label_classification/label_classification.py data/NA12878_GIAB_highconf_CG-IllFB-IllGATKHC-Ion-Solid-10X_CHROM1-X_v3.3_highconf.vcf candidate_$1.txt ${i} $1
    echo "$i generate img completed!" >> log_$1
done
echo "Completed" >> log_$1
