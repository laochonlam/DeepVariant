#!/bin/bash
if [[ $# -lt 4 ]]; then
    echo "Usage: $0 <chr> <pos> <bam> <ref>"
    exit 1
fi
name=`basename -s .bam $3`
name=$name"_$1_$2"

# Generate range = 1000000 sam and fa, then delete it
~/samtools-1.5/samtools view $3 $1:$2-$(($2+1000000)) > $name.sam
~/samtools-1.5/samtools faidx $4 $1:$(($2-200))-$(($2+1000200)) | tail -n +2 > $name.fa
python ~/git/deepvariant/find_candidate/find.py $1 $name $2
rm $name.sam
rm $name.fa
