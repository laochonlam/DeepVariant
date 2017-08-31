# Chr1 Only 
# Find Candidate Variants 
# Classification into 3 labels and generate corresponding images


for (( i=1010000; i<=249000000; i=i+1000000 ))
do
    ../find_candidate/find_candidate.sh chr1 ${i} A ../data/elsa.bam ../data/ucsc.hg19.fasta >> ../find_candidate/candidate.txt
    echo "$i find candidate completed!"
    python genotype_candidate.py ../data/NA12878_GIAB_highconf_CG-IllFB-IllGATKHC-Ion-Solid-10X_CHROM1-X_v3.3_highconf.vcf ../find_candidate/candidate.txt
    echo "$i generate img completed!"
done
echo "Completed"
