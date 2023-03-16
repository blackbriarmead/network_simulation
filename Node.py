from Frame import *
import util

class Node:
    flag = [0,1,1,1,1,1,1,0]
    def __init__(this, ip_addr):
        this.routing_table = []
        this.outboundlinks = []
        this.inboundlinks = []
        this.ip_addr = ip_addr
        this.outbound_data_buffers = {}
        this.inbound_data_buffers = {}
        this.outbound_target = None

    def display(this):
        print("Node:")
        print("  ip_addr: ",this.ip_addr)
        print("  inbound links:")
        for inboundlink in this.inboundlinks:
            inboundlink.display()
            print()
        print("  outbound links: ")
        for outboundlink in this.outboundlinks:
            outboundlink.display()
            print()

        print("outbound_data_buffers: ")
        for ip_addr in this.outbound_data_buffers.keys():
            print(this.ip_addr," -> ",ip_addr,":",[str(x) for x in this.outbound_data_buffers[ip_addr]])

        print("inbound_data_buffers: ")
        for ip_addr in this.inbound_data_buffers.keys():
            print(ip_addr," -> ",this.ip_addr,":")
            this.inbound_data_buffers[ip_addr].display()

    def get_ip_addr(this):
        return(this.ip_addr)
    
    #send data to neighboring node. This is not concerned with routing
    def send_data(this, data, outbound_link):
        target_ip = outbound_link.dest.ip_addr
        frame = Frame(data,target_ip,this.ip_addr)#construct a frame with the desired data        
        this.outbound_data_buffers[target_ip] = frame.data
        this.outbound_target = outbound_link

    #receiving data means monitoring inbound_links and pushing to respective buffer
    def receive_data(this, inbound_link):
        source_ip = inbound_link.source.ip_addr
        received = inbound_link.output #output is latest data produced by link
        this.inbound_data_buffers[source_ip].add_bit(received)
    
    #adds outbound link to array of outbound links
    def add_outbound_link(this, link):
        this.outboundlinks.append(link)
        this.outbound_data_buffers[link.dest.ip_addr] = []

    #adds inbound link to array of inbound links
    def add_inbound_link(this, link):
        this.inboundlinks.append(link)
        this.inbound_data_buffers[link.source.ip_addr] = InboundFrameHandler()

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
        this.process_data()

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
                print("final data:",this.data)
                print("dest_adr: ",util.list_to_int(this.data[0:8]))
                print("source_adr: ",util.list_to_int(this.data[8:16]))
                print("eth_protocol: ",util.list_to_int(this.data[16:20]))
                print("payload length (bytes): ",util.list_to_int(this.data[20:32]))
                print("payload: ",this.data[32:32+8*util.list_to_int(this.data[20:32])])
            else:
                #if not deflagged, just keep adding to data buffer
                if(not this.contains_deflagged(this.frame)):
                    this.data.append(this.frame[-1])
                #if deflagged, don't add latest bit
                else:
                    pass