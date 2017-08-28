import sys


def is_candidate(counts, allele):
    allele_count = counts[allele]

def expand_cigar(cigar):
    num = 0
    if cigar == '*':
        return cigar
    ret = ""
    for c in cigar:
        if c.isdigit():
            num = num * 10 + int(c)
        else:
            ret = ret + c * num
            num = 0
    return ret

def main():
    if len(sys.argv) <= 2:
        print "Usage %s <filename prefix> <pos> <alt allele>" % (sys.argv[0])
        exit()
    filename = sys.argv[1]
    with open(filename+".fa") as f:
        ref = f.read().translate(None,"\n")
    with open(filename+".sam") as f:
        sam = f.read().splitlines()
    timer = 0
    alt_allele = sys.argv[3]
    call_pos = int(sys.argv[2])

    count_A = [0]*1000
    count_G = [0]*1000
    count_C = [0]*1000
    count_T = [0]*1000

    for sam_line in sam:
        line = sam_line.split("\t")
        pos = int(line[3])
        mapq = line[4]
        seq = line[9]
        qual = line[10]
        flag = int(line[1])
        cigar = expand_cigar(line[5])


        ref_pos = pos - call_pos + 200
        read_pos = 0
        timer = timer + 1
        print "SAM!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1"
        for cigar_index in range(len(cigar)):
            this_cigar = cigar[cigar_index]
            # print "INDEX NUMBER : %d" % cigar_index
            # print "CIGAR INDEX : " + cigar[cigar_index]
            if this_cigar == 'M':
                # print "COMPARING %s and %s" % (seq[read_pos], ref[ref_pos]) 
                if seq[read_pos] == ref[ref_pos].upper():
                    continue
                else:
                    # print "GG"
                    if seq[read_pos] == "A":
                        count_A[ref_pos] = count_A[ref_pos] + 1
                        # print ref_pos
                    if seq[read_pos] == "C":
                        count_C[ref_pos] = count_C[ref_pos] + 1
                        # print ref_pos
                    if seq[read_pos] == "G":
                        count_G[ref_pos] = count_G[ref_pos] + 1
                        # print ref_pos
                    if seq[read_pos] == "T":
                        count_T[ref_pos] = count_T[ref_pos] + 1
                        # print ref_pos
                read_pos = read_pos + 1
                ref_pos = ref_pos + 1
                continue
            elif this_cigar == 'I' or this_cigar == 'S':
                read_pos = read_pos + 1
                continue
            elif this_cigar == 'D':
                ref_pos = ref_pos + 1
                continue
            elif this_cigar == 'H':
                continue
            else:
                continue

        # if timer == 50:

            # return 0

    print "A"
    for i in range(0,1000):
        if count_A[i] != 0:
            print i
    print "G"
    for i in range(0,1000):
        if count_G[i] != 0:
            print i
    print "C"
    for i in range(0,1000):
        if count_C[i] != 0:
            print i
    print "T"
    for i in range(0,1000):
        if count_T[i] != 0:
            print i
                    

if __name__ == "__main__":
    main()