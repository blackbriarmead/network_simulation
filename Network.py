from Link import Link

#a network object contains all node and link objects contained within
class Network:

    def __init__(this):
        this.nodes = []
        this.links = []


    def add_node(this, node):
        this.nodes.append(node)

    def add_bidirectional_link(this, ip1, ip2):
        node1 = None
        node2 = None
        for node in this.nodes:
            if(node.get_ip_addr()==ip1):
                node1 = node
                #early termination
                if(not node1 == None and not node2 == None):
                    break
            elif(node.get_ip_addr()==ip2):
                node2 = node
                #early termination
                if(not node1 == None and not node2 == None):
                    break
        #establish link from node1 to node2
        link1 = Link(node1,node2,10)
        this.links.append(link1)
        node1.add_outbound_link(link1)
        node2.add_inbound_link(link1)
        #establish link from node2 to node1
        link2 = Link(node2,node1,10)
        this.links.append(link2)
        node1.add_inbound_link(link2)
        node2.add_outbound_link(link2)
    
    def display(this):
        print("Displaying information about structure of network\n\n")
        for node in this.nodes:
            node.display()
            print()