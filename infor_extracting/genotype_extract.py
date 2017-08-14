import sys
import subprocess
import shlex

def main():
    if len(sys.argv) < 1:
        print "Usage %s <vcf>" % (sys.argv[0])
        exit()
    filename = sys.argv[1]
    with open(filename) as f:
        vcf = f.read().splitlines()

    for vcf_line in vcf:
        line = vcf_line.split("\t")
        # excluding header
        if line[0][0] != '#':
            # SNPs only
            if (len(line[3]) == 1) & (len(line[4]) == 1):
                # chr1 only
                if (line[0] == "1"):
                    ref = line[3]
                    alt = line[4]
                    pos = line[1]
                    chrom = "chr" + line[0]

                    if (line[9][0] == "1") & (line[9][2] == "1"):
                        genotype = "hom-alt"
                    else:
                        genotype = "het"


                    bam = "../data/lane1.sorted.bam"
                    fa = "../data/ucsc.hg19.fasta"
                    command = "../image_generation/gen_image.sh %s %s %s %s %s" % (chrom, pos, alt, bam, fa)
                    # print command
                    subprocess.call(shlex.split(command))
if __name__ == "__main__":
    main()