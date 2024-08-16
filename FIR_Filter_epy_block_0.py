"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr

buff=[0,0,0,0,0,0,0,0,0,0,0,0] #global decleration

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, example_param=1.0):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=[np.float32], # changing input type to float
            out_sig=[np.float32] # changing output type to float
        )

        self.example_param = example_param
        self.IR_length = 12 # Length of FIR filter


        # YOUR FILTER COEFFICIENTS
        self.coefs=[1,-1,1,-1,1,-1,1,-1,1,-1,1,-1]

        self.output=0
        self.temp=0
        self.input=0
        
        
        
 
    def work(self, input_items, output_items):
        """example: multiply with constant"""

        # WRITE YOUR CODE HERE
    
        self.input=input_items[0][0]
                    
        for j in range(self.IR_length-1,-1,-1):
            # Code to shift buffer
            buff[j] = buff[j-1]
        
        buff[0]=self.input
        self.output=0
        
        for j in range(0,self.IR_length):
            # Multiply buffer with coefficients and accumulate in output.
            self.output = self.output + buff[j]*self.coefs[j]

        output_items[0][0] = self.output
        return 1
