def to_bin_list(b, pad = 0):
    output = [int(x) for x in b[2:]]
    if(len(output) < pad):
        output = [0 for x in range(pad-len(output))] + output
    return output

def list_to_int(l):
    sum = 0
    mult = 1
    for i in range(len(l)-1,0,-1):
        sum += l[i] * mult
        mult *= 2
    return(sum)

def pad(b,pad):
    output = b
    if(len(b) < pad):
        output = output + [0 for x in range(pad-len(output))]
    return(output)