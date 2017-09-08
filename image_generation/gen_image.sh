#!/bin/bash
if [[ $# -lt 6 ]]; then
    echo "Usage: $0 <chr> <pos> <alt allele> <bam> <ref> <genotype>"
    exit 1
fi
name=`basename -s .bam $4`
name=$name"_chr$1_$2_$3"
echo "$name has been generated as a image [$6]"
~/samtools-1.5/samtools view $4 $1:$2-$2 > $name.sam
~/samtools-1.5/samtools faidx $5 $1:$(($2-110))-$(($2+110)) | tail -n +2 > $name.fa
python ~/git/deepvariant/image_generation/draw.py $name $2 $3 $6
rm $name.sam
rm $name.fa

