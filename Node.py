class Node:
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
            print(ip_addr," -> ",this.ip_addr,":",[str(x) for x in this.inbound_data_buffers[ip_addr]])

    def get_ip_addr(this):
        return(this.ip_addr)
    
    #send data to neighboring node. This is not concerned with routing
    def send_data(this, data, outbound_link):
        target_ip = outbound_link.dest.ip_addr
        this.outbound_data_buffers[target_ip] = data
        this.outbound_target = outbound_link

    #receiving data means monitoring inbound_links and pushing to respective buffer
    def receive_data(this, bit, inbound_link):
        source_ip = inbound_link.source.ip_addr
        this.inbound_data_buffers[source_ip].append(bit)

    
    #adds outbound link to array of outbound links
    def add_outbound_link(this, link):
        this.outboundlinks.append(link)
        this.outbound_data_buffers[link.dest.ip_addr] = []

    #adds inbound link to array of inbound links
    def add_inbound_link(this, link):
        this.inboundlinks.append(link)
        this.inbound_data_buffers[link.source.ip_addr] = []