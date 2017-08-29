#!/bin/bash
if [[ $# -lt 5 ]]; then
    echo "Usage: $0 <chr> <pos> <alt allele> <bam> <ref>"
    exit 1
fi
name=`basename -s .bam $4`
name=$name"_$1_$2"
# echo $name
~/samtools-1.5/samtools view $4 $1:$2-$(($2+1000000)) > $name.sam
~/samtools-1.5/samtools faidx $5 $1:$(($2-200))-$(($2+1000200)) | tail -n +2 > $name.fa
#100dp?
python ~/git/deepvariant/find_candidate/find.py $1 $name $2 $3