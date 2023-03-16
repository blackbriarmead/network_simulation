from Link import Link

#a network object contains all node and link objects contained within
class Network:

    def __init__(this):
        this.nodes = []
        this.links = []


    def add_node(this, node):
        this.nodes.append(node)

    def add_link(this, ip1, ip2):
        node1 = None
        node2 = None
        for node in this.nodes:
            if(node.mac_addr==ip1):
                node1 = node
                #early termination
                if(not node1 == None and not node2 == None):
                    break
            elif(node.mac_addr==ip2):
                node2 = node
                #early termination
                if(not node1 == None and not node2 == None):
                    break
        #establish link from node1 to node2 and vice versa
        link = Link(10)
        this.links.append(link)
        node1.add_link(link,0)
        node2.add_link(link,1)
    
    def display(this):
        print("Displaying information about structure of network\n\n")
        for node in this.nodes:
            node.display()
            print()