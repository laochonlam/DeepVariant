# Chr1 Only 
# Find Candidate Variants 
# Classification into 3 labels and generate corresponding images


for (( i=1010000; i<=249000000; i=i+1000000 ))
do
    # Usage find_candidate <chr> <pos> A <bam> <fasta>
    find_candidate/find_candidate.sh chr1 ${i} A data/elsa.bam data/ucsc.hg19.fasta > candidate.txt
    echo "$i find candidate completed!"
    # Usage label_classification.py <vcf> <candidate>
    python label_classification/label_classification.py data/NA12878_GIAB_highconf_CG-IllFB-IllGATKHC-Ion-Solid-10X_CHROM1-X_v3.3_highconf.vcf candidate.txt
    echo "$i generate img completed!"
done
echo "Completed"
