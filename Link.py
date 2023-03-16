#link contains a one-way connection between two nodes
class Link:
    def __init__(this, source, dest, length):
        this.source = source
        this.dest = dest
        this.length = length
        this.data = [0 for x in range(length)]
        this.output = 0 #output is used for the receiving node, it is updated for every simulation step

    def display(this):
        print("    link:")
        print("      source_addr:",this.source.get_ip_addr())
        print("      dest_addr:",this.dest.get_ip_addr())
        print("      length: ",this.length)
        print("      Data in transit: ", [str(x) for x in this.data])

    #simulates the link. returns the output of the link and updates link with input value
    #propagates each bit in transit to the next position as well
    def simulate(this, input):
        this.data.insert(0,input) #insert new data into link
        this.output = this.data.pop() #pop last item from data