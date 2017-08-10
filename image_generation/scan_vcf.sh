#!/bin/bash

if [[ $# -lt 3 ]]; then
    echo "Usage: $0 <vcf> <bam> <ref>"
    exit 1
fi

while read line; do
    read -r -a split <<< $line
    chr=${split[0]}
    pos=${split[1]}
    ref=${split[3]}
    alt=${split[4]}
    if [[ ${#ref} -eq 1 && ${#alt} -eq 1 ]]; then
        ~/yifan/tensor/gen_image.sh $chr $pos $alt $2 $3
    fi
done < $1
