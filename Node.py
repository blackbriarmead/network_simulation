from Frame import *
import util

class Node:
    flag = [0,1,1,1,1,1,1,0]
    def __init__(this, mac_addr):
        this.mac_addr = mac_addr
        this.link_handlers = []
        this.dest_mac = []

    def display(this):
        print("Node:")
        print("  mac_addr: ",this.mac_addr)
        print(" table of connected mac addresses: ")
        for i in range(len(this.dest_mac)):
            print("Port",i," -> ", bin(this.dest_mac[i]))
            print("link side: ",this.link_handlers[i].side)
        
    
    #send data to neighboring node. This is not concerned with routing
    def send_data(this):
        for link_handler in this.link_handlers:
            link_handler.send_data()

    def initiate_send_data(this, data, port_no):
        this.link_handlers[port_no].initiate_send_data(data,this.dest_mac[port_no])

    #receiving data means monitoring inbound_links and pushing to respective buffer
    def receive_data(this):
        for link_handler in this.link_handlers:
            frame, port_no = link_handler.receive_data()
            if(not frame == None):
                frame.display()
                match frame.eth_protocol:
                    case Eth_Protocol.NEIGHBOR_DISCOVERY_REQUEST:
                        this.dest_mac[port_no] = int(frame.source_adr)
                        this.neighbor_discovery_reply(port_no)
                        print("neighbor discovered via request")
                        print("my mac address: ",this.mac_addr)
                        print("neighbor mac address: ",int(frame.source_adr))
                        break
                    case Eth_Protocol.NEIGHBOR_DISCOVERY_REPLY:
                        this.dest_mac[port_no] = frame.source_adr
                        print("neighbor discovered")
                        break

    
    #adds link to link handler
    def add_link(this, link, side):
        this.link_handlers.append(LinkHandler(this.mac_addr,link,side,len(this.link_handlers)))
        this.dest_mac.append(0)
        this.neighbor_discovery_request(len(this.link_handlers)-1)

    def neighbor_discovery_request(this, port_no):
        print("initiating neighbor discovery request")
        this.link_handlers[port_no].initiate_send_data( [0 for x in range(8)],dest_mac = 0, protocol = Eth_Protocol.NEIGHBOR_DISCOVERY_REQUEST)

    def neighbor_discovery_reply(this, port_no):
        print("initiating neighbor discovery reply")
        this.link_handlers[port_no].initiate_send_data( [0 for x in range(8)],dest_mac = this.dest_mac[port_no], protocol = Eth_Protocol.NEIGHBOR_DISCOVERY_REPLY)

class LinkHandler:
    def __init__(this, mac_addr, link, side, port_no):
        this.mac_addr = mac_addr
        this.inbound_handler = InboundFrameHandler()
        this.outbound_handler = OutboundFrameHandler()
        this.link = link
        this.side = side
        this.port_no = port_no

    def receive_data(this):
        received = this.link.output[1-this.side]
        processed = this.inbound_handler.add_bit(received)
        return((processed,this.port_no))
                    

    def send_data(this):
        this.link.simulate(this.outbound_handler.get_next_bit(), this.side)

    #dest_adr specifies the intended target, but is not required for a wired link
    def initiate_send_data(this, data, dest_mac = 0, protocol = Eth_Protocol.ETHERNET):
        this.outbound_handler.frame = FrameConstructor(data,bin(dest_mac),this.mac_addr, protocol = protocol).data

                


class InboundFrameHandler():
    def __init__(this):
        this.flag =       [0,1,1,1,1,1,1,0]
        this.de_flagged = [0,1,1,1,1,1,0]
        this.frame_start = False
        this.finished = False
        this.length = 0
        this.frame = []
        this.data = []

    def display(this):
        print("Frame: ", this.frame)
        print("Data: ", this.frame)
        print("frame_start: ", this.frame_start)
        print("finished: ", this.finished)

    def add_bit(this,bit):
        this.frame.append(bit)
        return(this.process_data())

    def contains_flag(this, data):
        return(data[-len(this.flag):] == this.flag)
    
    def contains_deflagged(this,data):
        return(data[-len(this.de_flagged):] == this.de_flagged)
    
    def process_data(this):
        if(not this.frame_start):
            #wait until length of frame is at least the length of the flag
            if(len(this.frame) >= len(this.flag)):
                #if flag found, change frame_start to true
                if(this.contains_flag(this.frame)):
                    this.frame_start = True
                    print("first flag detected, frame started")
                    #if flag not found, discard first bit received
                else:
                    this.frame.pop(0)#remove first bit received to ensure this buffer does not grow forever

        elif(not this.finished):
            #middle of frame
            if(this.contains_flag(this.frame)):
                #pop flag from data - data should now only be the bits that were intended to be received
                _ = [this.data.pop() for x in range(len(this.flag)-1)]
                this.finished = True
                print("second flag detected, frame ended")
                print("final frame:",this.frame)
                return(Frame(this.data))

            else:
                #if not deflagged, just keep adding to data buffer
                if(not this.contains_deflagged(this.frame)):
                    this.data.append(this.frame[-1])
                #if deflagged, don't add latest bit
                else:
                    pass

class OutboundFrameHandler():
    def __init__(this):
        this.frame = []

    def display(this):
        print("Frame: ", this.frame)
        print("Data: ", this.frame)
        print("frame_start: ", this.frame_start)
        print("finished: ", this.finished)

    def get_next_bit(this):
        bit = 0
        if(not len(this.frame) == 0):
            return(this.frame.pop(0))
        