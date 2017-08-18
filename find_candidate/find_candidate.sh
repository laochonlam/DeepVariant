if [[ $# -lt 5 ]]; then
    echo "Usage: $0 <chr> <alt allele> <bam> <ref>"
    exit 1
if
name=`basename -s .bam $3`
name=$name"_chr$1_$3"

~/samtools-1.5/samtools view $3 $1 > tmp/$name.sam
~/samtools-1.5/samtools faidx $4 $1 | tail -n +2 > tmp/$name.faidx
python ~/git/deepvariant/find_candidate/find.py tmp/$name $2