import util
import enum

class Eth_Protocol(enum.IntEnum):
    ETHERNET = 0,
    NEIGHBOR_DISCOVERY_REQUEST = 1
    NEIGHBOR_DISCOVERY_REPLY = 2

#constructs the binary representation of a frame
class FrameConstructor:

    flag = [0,1,1,1,1,1,1,0] #flag is used to determine start and end of frames

    def __init__(this, data, dest_adr, source_adr, protocol = Eth_Protocol.ETHERNET):
        calculated_payload_length = ((len(data)-1) // 8)+1
        if(calculated_payload_length < 1):
            calculated_payload_length = 1


        contents = []
        contents = contents + this.flag
        encapsulated = util.to_bin_list(dest_adr, pad = 8)
        encapsulated = encapsulated + util.to_bin_list(source_adr, pad = 8)
        encapsulated = encapsulated + util.to_bin_list(bin(protocol), pad = 4)#this indicates the protocol this frame is using
        encapsulated = encapsulated + util.to_bin_list(bin(calculated_payload_length), pad = 12)#minimum transmission size of 1 byte
        encapsulated = encapsulated + util.pad(data,8*calculated_payload_length)
        encapsulated = this.filter_data(encapsulated)
        contents = contents + encapsulated
        contents = contents + this.flag
        this.data = contents

    def filter_data(this,data):
        output = []
        consecutive = 0
        
        for d in data:
            if d == 1:
                consecutive += 1
            else:
                if(consecutive == 5):
                    output.append(0)#edge case - does not need to deduplicated, but decode assumes it is
                consecutive = 0
            
            if(consecutive > 5):
                output.append(0)
                consecutive = 1
            output.append(d)
        
        return(output)
    
#encodes the useful information from a decoded frame    
class Frame:
    def __init__(this, data):
        this.data = data
        this.dest_adr = util.list_to_int(this.data[0:8])
        this.source_adr = util.list_to_int(this.data[8:16])
        this.eth_protocol = util.list_to_int(this.data[16:20])
        this.payload_length = util.list_to_int(this.data[20:32])
        this.payload = this.data[32:32+8*this.payload_length]