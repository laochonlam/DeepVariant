#!/bin/bash
if [[ $# -lt 5 ]]; then
    echo "Usage: $0 <chr> <pos> <alt allele> <bam> <ref>"
    exit 1
fi
name=`basename -s .bam $4`
name=$name"_chr$1_$2_$3"

samtools view $4 $1:$2-$2 > $name.sam
samtools faidx $5 $1:$(($2-110))-$(($2+110)) | tail -n +2 > $name.fa
python ~/yifan/tensor/draw.py $name $2 $3

