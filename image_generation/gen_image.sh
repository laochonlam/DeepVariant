#!/bin/bash
if [[ $# -lt 6 ]]; then
    echo "Usage: $0 <chr> <pos> <alt allele> <bam> <ref> <genotype>"
    exit 1
fi
name=`basename -s .bam $4`
name=$name"_$1_$2_$3_$6"
echo "$name has been generated as a image [$6]" >> log_$1
samtools view $4 $1:$2-$2 > $name.sam
samtools faidx $5 $1:$(($2-110))-$(($2+110)) | tail -n +2 > $name.fa
python image_generation/draw.py $name $2 $3 $6
rm $name.sam
rm $name.fa

