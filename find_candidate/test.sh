echo [Start chr1]
./find_candidate.sh chr1 10000 A ../data/elsa.bam ../data/ucsc.hg19.fasta > candidate.txt
echo [Start chr2]
./find_candidate.sh chr1 3000000 A ../data/elsa.bam ../data/ucsc.hg19.fasta >> candidate.txt
echo [Start chr3]
./find_candidate.sh chr1 5000000 A ../data/elsa.bam ../data/ucsc.hg19.fasta >> candidate.txt
echo [Start chr4]
./find_candidate.sh chr1 7000000 A ../data/elsa.bam ../data/ucsc.hg19.fasta >> candidate.txt
echo [Start chr5]
./find_candidate.sh chr1 9000000 A ../data/elsa.bam ../data/ucsc.hg19.fasta >> candidate.txt
echo [Completed]