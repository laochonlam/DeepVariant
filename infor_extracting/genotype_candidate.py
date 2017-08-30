import sys
import subprocess
import shlex

def main():
    if len(sys.argv) < 2:
        print "Usage %s <vcf> <candidate_variant>" % (sys.argv[0])
        exit()
    vcf_filename = sys.argv[1]
    candidate_filename = sys.argv[2]

    variant_count = 0
    ref_count = 0
    bam = "../data/elsa.bam"
    fa = "../data/ucsc.hg19.fasta"


    with open(vcf_filename) as f:
        vcf = f.read().splitlines()
    with open(candidate_filename) as f:
        candidate = f.read().splitlines()


    #  Normal Version

    # for candidate_line in candidate:
    #     line = candidate_line.split(" ")
        # chromosome = line[2][3]
        # print chromosome

        # for vcf_line in vcf:
        #     line_vcf = vcf_line.split("\t")
        #     if line_vcf[0][0] != '#':
        #         # if chromosome == line_vcf[0]:
        #         # if (line[0] == line_vcf[4]):
        #         #     print "yo"
        #         if int(line_vcf[1]) < int(line[1]):
        #             continue
        #         if (int(line[1]) == int(line_vcf[1])) & (line_vcf[4]  == line[0]):
        #             # print line[1]
        #             # print "vcf : %s and candidate : %s" % (line_vcf[4], line[0])
        #             bingo = bingo + 1
        #             break
        #         if int(line_vcf[1]) > int(line[1]):
        #             ref = ref + 1
        #             break
    



    # Filter Version
    i = 0
    SNPS = [0]* 824
    for vcf_line in vcf:
        line_vcf = vcf_line.split("\t")
        if line_vcf[0][0] != '#':
            if (int(line_vcf[1]) <= 2000000 + 200) & (int(line_vcf[1]) >= 1000000 - 200):
                if (len(line_vcf[3]) == 1) & (len(line_vcf[4]) == 1):
                    if int(line_vcf[0]) == 1:
                        SNPS[i] = vcf_line
                        i = i + 1

    print "[Bounding Completed]"


    for candidate_line in candidate:
        line = candidate_line.split(" ")
        timer = 0
        for SNP_line in SNPS:
            timer = timer + 1
            if SNP_line != "0":
                line_SNP = SNP_line.split("\t")

                ref = line_SNP[3]
                alt = line_SNP[4]
                pos = line_SNP[1]
                chrom = "chr" + line_SNP[0]

                if (line_SNP[0][0] != '#') & (line_SNP[0] != "0"):
                    # if chromosome == line_SNP[0]:
                    # if (line[0] == line_SNP[4]):
                    #     print "yo"
                    if int(line_SNP[1]) < int(line[1]):
                        continue

                    # het or hom
                    if (int(line[1]) == int(line_SNP[1])) & (line_SNP[4]  == line[0]):
                        # print line[1]
                        # print "vcf : %s and candidate : %s" % (line_SNP[4], line[0])
                    
                        if (line_SNP[9][0] == "1") & (line_SNP[9][2] == "1"):
                            genotype = "hom-alt"
                            print "hom-alt"
                        else:
                            genotype = "het"
                            print "het"
                        command = "../image_generation/gen_image.sh %s %s %s %s %s %s" % (chrom, pos, alt, bam, fa, genotype)
                        subprocess.call(shlex.split(command))

                        variant_count = variant_count + 1
                        break


                    # Ref
                    if int(line_SNP[1]) > int(line[1]):
                        ref_count = ref_count + 1
                        genotype = "ref"
                        print "ref"
                        command = "../image_generation/gen_image.sh %s %s %s %s %s %s" % (chrom, pos, alt, bam, fa, genotype)
                        subprocess.call(shlex.split(command))
                        break






    # for SNPS_line in SNPS:
    #     print SNPS_line

    print variant_count
    print ref_count

if __name__ == "__main__":
    main()
