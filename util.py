def to_bin_list(b, pad = 0):
    output = [int(x) for x in b[2:]]
    if(len(output) < pad):
        output = [0 for x in range(pad-len(output))] + output
    return output

def list_to_int(l):
    #print("list: ", l)
    sum = 0
    mult = 1
    i = len(l)-1
    while(i >= 0):
        sum += l[i] * mult
        mult *= 2
        i -= 1
    #print("sum: ",sum)
    return(sum)

def pad(b,pad):
    output = b
    if(len(b) < pad):
        output = output + [0 for x in range(pad-len(output))]
    return(output)

def list_to_string(l):
    output = ""

    for i in range(0,len(l),8):
        ll = l[i:i+8]
        #print(ll)
        rep = list_to_int(l[i:i+8])
        #print(rep)
        output = output + chr(rep)

    return(output)