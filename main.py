from Network import Network
from Node import Node
from Simulation import Simulation

#a node can be connected to other nodes with a link, outbound and inbound

net = Network()

node1 = Node(bin(1))
net.add_node(node1)
node2 = Node(bin(2))
net.add_node(node2)
node3 = Node(bin(3))
net.add_node(node3)

net.add_bidirectional_link(bin(1),bin(2))
net.add_bidirectional_link(bin(2),bin(3))
sim = Simulation(net)
payload = [1,1,1,1,1,1,1,1] + [1,1,1,1,1,1,1,0]
node1.send_data(payload,node1.outboundlinks[0])
sim.simulate(iterations = 100)
