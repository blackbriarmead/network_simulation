#link contains a two-way connection between two nodes
#the nodes are not specified because in the real world, a cable does not know what it is connected to
class Link:
    def __init__(this, length):
        this.length = length
        this.data = [[0 for x in range(length)],[0 for x in range(length)]]
        this.output = [0,0] #output is used for the receiving node, it is updated for every simulation step

    def display(this):
        print("    link:")
        print("      length: ",this.length)
        print("      Data in transit1: ", [str(x) for x in this.data])
        print("      Data in transit2: ", [str(x) for x in this.data])

    #simulates the link. returns the output of the link and updates link with input value
    #propagates each bit in transit to the next position as well
    def simulate(this, input, which = 0):
        this.data[which].insert(0,input)
        this.output[which] = this.data[which].pop()