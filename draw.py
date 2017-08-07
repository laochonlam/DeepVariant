WIDTH = 221
HEIGHT = 100
MID = int(WIDTH/2)


def fill_reference_pixels(ref, pixels):
    for row in range(5):
        for col in range(WIDTH):
            alpha = 0.4
            red = get_base_color(ref[col])
            green = get_quality_color(60) # The reference is high quality
            blue = get_strand_color(True) # The reference is on the positive strand
            pixels[row, col] = make_pixel(red, green, blue, alpha)
def get_base_color(base):
        base_to_color = {'A': 250, 'G': 180, 'T': 100, 'C': 30}
        return base_to_color.get(base, 0)
def get_quality_color(quality):
        return int(254.0 * (min(40, quality) / 40.0))
def get_strand_color(on_positive_strand):
        return 70 if on_positive_strand else 240
def make_pixel(red, green, blue, alpha):
        return (255-int(alpha * red), 255-int(alpha * green), 255-int(alpha * blue))

def in_canvas(x):
    return x>=0 and x<WIDTH

def expand_cigar(cigar):
    num = 0
    ret = ""
    for c in cigar:
        if c.isdigit():
            num = num * 10 + int(c)
        else:
            ret = ret + c * num
            num = 0
    return ret


def base_qual_poor(qual, cigar, pos):
    cigar_idx = 0
    seq_idx = 0
    mypos = 0
    while seq_idx < len(qual):
        this_cigar = cigar[cigar_idx]
        cigar_idx = cigar_idx + 1
        if this_cigar == 'M':
            if mypos == pos: return qual[seq_idx] < 10
            mypos = mypos+1
            seq_idx = seq_idx+1 
        elif this_cigar == 'I' or this_cigar == 'S':
            seq_idx = seq_idx+1
        elif this_cigar == 'D':
            if mypos == pos: return False
            mypos = mypos+1
        elif this_cigar == 'H':
            pass
        else:
            raise Exception
            

def main():
    import sys
    if len(sys.argv) <= 3:
        print "Usage %s <filename prefix> <pos> <alt allele> " % (sys.argv[0])
        exit()
    filename = sys.argv[1]
    with open(filename+".fa") as f:
        ref = f.read().translate(None,"\n")
    with open(filename+".sam") as f:
        sam = f.read().splitlines()

    call_pos = int(sys.argv[2])
    alt_allele = sys.argv[3]

    from PIL import Image
    img = Image.new("RGB",(HEIGHT, WIDTH), "black")
    pixels = img.load()


    # fill 5 copies of reference
    fill_reference_pixels(ref, pixels)
    pixels[0,MID] = (255,255,255)
    pixels[2,MID] = (255,255,255)
    pixels[4,MID] = (255,255,255)

    row_idx = 5
    weight = dict.fromkeys(range(5,HEIGHT))
    for sam_line in sam:
        if row_idx >= HEIGHT: break
        line = sam_line.split("\t")
        pos = int(line[3])
        mapq = int(line[4])
        seq = line[9]
        qual = line[10]
        flag = int(line[1])
        revcomp = bool(flag & 16)
        fail = bool((flag & 256) or (flag & 2048) or (flag & 2 == 0) or (flag & 512) or (flag & 4) or (flag & 1024)) 
        if fail: continue
        cigar = expand_cigar(line[5])

        # check base qual at call position
        if base_qual_poor(qual, cigar, call_pos - pos): continue

        cigar_idx = 0
        read_pos = 0
        ref_pos = pos
        while read_pos < len(seq):
            if ref_pos-call_pos+MID >= WIDTH: break
            this_cigar = cigar[cigar_idx]
            cigar_idx = cigar_idx + 1
            if this_cigar == "M":
                # draw this pixel
                if in_canvas(ref_pos-call_pos+MID):
                    this_qual = min(qual[read_pos],qual)
                    this_base = seq[read_pos]
                    alpha2 = 0.2 if this_base==ref[ref_pos-call_pos+MID] else 1.0
                    alpha1 = 1.0 if ref_pos==call_pos and this_base==alt_allele else 0.6
                    if ref_pos==call_pos: weight[row_idx] = "A" if this_base==alt_allele else "Z"
                    alpha = alpha1 * alpha2
                    red = get_base_color(this_base)
                    green = get_quality_color(this_qual)
                    blue = get_strand_color(not revcomp)
                    pixels[row_idx, ref_pos-call_pos+MID] = make_pixel(red, green, blue, alpha)

                #if ref_pos==call_pos: print row_idx, red, green, blue, alpha1, alpha2
                read_pos = read_pos+1
                ref_pos = ref_pos+1
            elif this_cigar == "I" or this_cigar == "S":
                read_pos = read_pos+1
                continue
            elif this_cigar == "D":
                ref_pos = ref_pos+1
                continue
            elif this_cigar == "H":
                continue
            else:
                raise Exception

        if weight[row_idx] is None:
            weight[row_idx] = "Z"
        weight[row_idx] += "A" if revcomp else "Z"
        row_idx = row_idx+1
                
        
    out = Image.new("RGB",(HEIGHT, WIDTH), "black")
    pix = out.load()
    for i in range(5):
        for j in range(WIDTH):
            pix[i,j] = pixels[i,j]
    newidx = 5
    for key,value in sorted(weight.iteritems(), key=lambda (k,v):(v,k)):
        oldidx = int(key)
        for j in range(WIDTH): pix[newidx,j] = pixels[oldidx, j]
        newidx = newidx+1
    out.save(filename+".bmp");


if __name__ == "__main__":
    main()
