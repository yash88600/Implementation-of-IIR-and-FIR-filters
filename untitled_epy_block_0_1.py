"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, feedforward_taps=[1], feedbacktaps=[1]):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',  # will show up in GRC
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.feedforward_taps= feedforward_taps # These are your N+1 coefficients.
        self.feedbacktaps= feedbacktaps # These are your M+1 coefficients.


        self.inputbuffer = np.zeros(len(feedforward_taps)) # Initializing Input Buffer
        self.outputbuffer = np.zeros(len(feedbacktaps)) # Initializing Output Buffer

        self.index = 0



    def work(self, input_items, output_items):

        self.input= input_items[0][0] # First sample of input vector
        self.output=0

        k= len(self.feedforward_taps)-1
        self.output=self.input * self.feedforward_taps[0]  # Equation 4 for b0*x[n]
        #################################################################
        # This operation will take care of IIR filter of variable length.
        for i in range(1, k):
            self.output = self.output + (self.inputbuffer[k-i] * self.feedforward_taps[i]) + (self.outputbuffer[k-i]*self.feedbacktaps[i])
            # Fill in with suitable code to implement equation 4 of the manual for i = 1 to M and j= 1 to N. See line 40 & 49 for i=0 & j=0.
            # This will give you IIR filter of variable filter length/order.

        ###############################################################3
        self.output /= self.feedbacktaps[0]  # Divide by a0 in case a0!=1 to realize eq.4.

        output_items[0][0] = self.output  # Store output
        # print(self.output)
        self.inputbuffer[self.index] = input_items[0][0] # Append inputbuffer
        self.outputbuffer[self.index] = output_items[0][0] # Append outputbuffer
        self.index = self.index + 1
        if(self.index > k):
            self.inputbuffer = np.zeros(len(self.feedforward_taps))
            self.outputbuffer = np.zeros(len(self.feedbacktaps))
            self.index = 0

        return 1
