import sys


def is_candidate(counts, allele):
    allele_count = counts[allele]



def main():
    if len(sys.argv) <= 2:
        print "Usage %s <filename prefix> <alt allele>" % (sys.argv[0])
        exit()
    filename = sys.argv[1]
    with open(filename+".fa") as f:
        ref = f.read().translate(None,"\n")
    with open(filename+".sam") as f:
        sam = f.read().splitlines()
    
    alt_allele = sys.argv[2]

    print ref[0]

if __name__ == "__main__":
    main()