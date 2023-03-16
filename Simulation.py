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
        old = this.network
        netcopy = copy.deepcopy(this.network)

        #steps:

        #for each node
        #send data down link
        #get receiver node to 

        #insert data into links
        for node in netcopy.nodes:
            outboundlinks = node.outboundlinks
            for outlink in outboundlinks:
                #get next bit from outbound_buffer
                dest_ip = outlink.dest.ip_addr
                outbound_buffer = node.outbound_data_buffers[dest_ip]
                input = 0
                if(not len(outbound_buffer) == 0):
                    input = outbound_buffer.pop(0) #pop from beginning becase we are sending back to front
                outlink.simulate(input)

        for node in netcopy.nodes:
            inboundlinks = node.inboundlinks
            for inlink in inboundlinks:
                received = inlink.output #output is latest data produced by link
                source_ip = inlink.source.ip_addr
                inbound_buffer = node.inbound_data_buffers[source_ip]
                inbound_buffer.append(received)

        this.network = netcopy #update current representation of network
        this.time += 1

    def simulate(this, iterations = 1, display = False):
        for i in range(iterations):
            this.simulateStep()
            if(display):
                this.display()