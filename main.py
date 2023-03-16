from Network import Network
from Node import Node
from Simulation import Simulation
import util

#a node can be connected to other nodes with a link, outbound and inbound

net = Network()

node1 = Node(bin(1))
net.add_node(node1)
node2 = Node(bin(2))
net.add_node(node2)
node3 = Node(bin(3))
net.add_node(node3)

net.add_link(bin(1),bin(2))
net.add_link(bin(2),bin(3))
sim = Simulation(net)
s = ascii('huy is a sussy baka')[1:-1]
print([ord(x) for x in s])
s = [util.to_bin_list(bin(ord(c)),pad=8) for c in s]
payload = []
for item in s:
    payload = payload + item
node1.initiate_send_data(payload,0)
sim.simulate(iterations = 1000)
