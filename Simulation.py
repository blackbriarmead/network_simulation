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
            node.send_data()

        #let nodes receive data and process frames
        for node in this.network.nodes:
            node.receive_data()

        

        this.time += 1

    def simulate(this, iterations = 1, display = False):
        for i in range(iterations):
            this.simulateStep()
            if(display):
                this.display()