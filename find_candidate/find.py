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

    count_A = [0]*20000
    count_G = [0]*20000
    count_C = [0]*20000
    count_T = [0]*20000
    total_counts = [0]*20000
    min_count = 2
    candidate_count = 0

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
        # print "-----"
        # print timer

        for cigar_index in range(len(cigar)):
            this_cigar = cigar[cigar_index]
            # print "INDEX NUMBER : %d" % cigar_index
            # print "CIGAR INDEX : " + cigar[cigar_index]
            if this_cigar == 'M':
                # print "COMPARING %s and %s" % (seq[read_pos], ref[ref_pos]) 
                if seq[read_pos] == ref[ref_pos].upper():
                    # print "right"
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

        # if timer == 1000:
                # print i
        # print "A"
        # if count_A[i] != 0:
        #     print "%d %d" % (i, count_A[i])
        # print "G"
        # if count_G[i] != 0:
        #     print "%d %d" % (i, count_G[i])
        # print "C"
        # if count_C[i] != 0:
        #     print "%d %d" % (i, count_C[i])
        # print "T"
        # if count_T[i] != 0:
        #     print "%d %d" % (i, count_T[i])
    for i in range(0,1000):
        total_counts[i] = count_A[i] + count_C[i] + count_G[i] + count_T[i]
        if total_counts != 0:
            if count_A[i] >= min_count:
                if count_A[i] / total_counts[i] >= 0.25:
                    # print "A %d" % i
                    candidate_count = candidate_count + 1
            if count_G[i] >= min_count:
                if count_G[i] / total_counts[i] >= 0.25:
                    # print "G %d" % i
                    candidate_count = candidate_count + 1
            if count_C[i] >= min_count:
                if count_C[i] / total_counts[i] >= 0.25:
                    # print "C %d" % i
                    candidate_count = candidate_count + 1
            if count_T[i] >= min_count:
                if count_T[i] / total_counts[i] >= 0.25:
                    # print "T %d" % i
                    candidate_count = candidate_count + 1

    print candidate_count
        
                
                
                
                
                # print total_counts[i]
            # return 0


        
                    

if __name__ == "__main__":
    main()