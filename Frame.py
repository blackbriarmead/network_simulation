
#a frame object 
class Frame:

    flag = [0,1,1,1,1,1,1,0] #flag is used to determine start and end of frames

    def __init__(this,data):
        contents = []
        contents = contents + this.flag
        contents = contents + this.filter_data(data)
        contents = contents + this.flag
        this.data = contents

    def filter_data(this,data):
        output = []
        consecutive = 0
        for d in data:
            if d == 1:
                consecutive += 1
            else:
                consecutive = 0
            
            if(consecutive > 5):
                output.append(0)
                consecutive = 1
            output.append(d)
        return(output)