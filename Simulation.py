import copy

class Simulation:

    def __init__(this, network):
        this.network = network
        this.time = 0
        #perform any other required initilization operations
    
    def display(this):
        print("timestep: ",this.time)
        this.network.display()


    #each network step creates a copy of the network, because in minecraft, everything happens one tick at a time
    def simulateStep(this):

        #insert data into links
        for node in this.network.nodes:
            outboundlinks = node.outboundlinks
            for outlink in outboundlinks:
                #get next bit from outbound_buffer
                dest_ip = outlink.dest.ip_addr
                outbound_buffer = node.outbound_data_buffers[dest_ip]
                input = 0
                if(not len(outbound_buffer) == 0):
                    input = outbound_buffer.pop(0) #pop from beginning becase we are sending back to front
                outlink.simulate(input)

        #let nodes receive data and process frames
        for node in this.network.nodes:
            for inlink in node.inboundlinks:
                node.receive_data(inlink)

        

        this.time += 1

    def simulate(this, iterations = 1, display = False):
        for i in range(iterations):
            this.simulateStep()
            if(display):
                this.display()