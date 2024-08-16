# """
# Embedded Python Blocks:

# Each time this file is saved, GRC will instantiate the first class it finds
# to get ports and parameters of your block. The arguments to __init__  will
# be the parameters. All of them are required to have default values!
# """

# import numpy as np
# from gnuradio import gr

# class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
#     """Embedded Python Block example - a simple multiply const"""

#     def __init__(self, feedforward_taps=[1], feedbacktaps=[1]):  # only default arguments here
#         """arguments to this function show up as parameters in GRC"""
#         gr.sync_block.__init__(
#             self,
#             name='Embedded Python Block',  # will show up in GRC
#             in_sig=[np.float32],
#             out_sig=[np.float32]
#         )
#         # if an attribute with the same name as a parameter is found,
#         # a callback is registered (properties work, too).
#         self.feedforward_taps= feedforward_taps # These are your N+1 coefficients.
#         self.feedbacktaps= feedbacktaps # These are your M+1 coefficients.


#         self.inputbuffer = np.zeros(len(feedforward_taps)) # Initializing Input Buffer
#         self.outputbuffer = np.zeros(len(feedbacktaps)) # Initializing Output Buffer

#         self.index = 0



#     def work(self, input_items, output_items):

#         self.input= input_items[0][0] # First sample of input vector
#         self.output=0

#         k= len(self.feedforward_taps)-1
#         self.output=self.input * self.feedforward_taps[0]  # Equation 4 for b0*x[n]
#         #################################################################
#         # This operation will take care of IIR filter of variable length.
#         for i in range(1, k):
#             self.output = self.output + (self.inputbuffer[k-i] * self.feedforward_taps[i]) - (self.outputbuffer[k-i]*self.feedbacktaps[i])
#             # Fill in with suitable code to implement equation 4 of the manual for i = 1 to M and j= 1 to N. See line 40 & 49 for i=0 & j=0.
#             # This will give you IIR filter of variable filter length/order.

#         ###############################################################3
#         self.output /= self.feedbacktaps[0]  # Divide by a0 in case a0!=1 to realize eq.4.

#         output_items[0][0] = self.output  # Store output
#         # print(self.output)
#         self.inputbuffer[self.index] = input_items[0][0] # Append inputbuffer
#         self.outputbuffer[self.index] = output_items[0][0] # Append outputbuffer
#         self.index = self.index + 1
#         if(self.index > k):
#             self.inputbuffer = np.zeros(len(self.feedforward_taps))
#             self.outputbuffer = np.zeros(len(self.feedbacktaps))
#             self.index = 0

#         return 1

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
        self.feedforward_taps= feedforward_taps
        self.feedbacktaps= feedbacktaps

          # This is a local array that I define to store old output values. I need to set this up since there is not a set_history function to access old outputs (at least I cannot find such a function in GNU radio).
        # self.feedforward_taps = 0.0736, 0.2208, 0.2208, 0.0736  # feedforward taps of IIR filter
        # self.feedbacktaps = 1.0000, -0.9761, 0.8568, -0.2919  # feedback taps of IIR filter

        #H2(z) = (10000-12728z^-1+8100z^-2) / (100-160z^-1+64z^-2)
        # self.feedforward_taps = 10000, 12728, 8100  # feedforward taps of IIR filter
        # self.feedbacktaps = 100, 160, 64  # feedback taps of IIR filter

        self.inputbuffer = [0] * (len(self.feedforward_taps)-1) # Initializing Input Buffer
        self.outputbuffer = [0] * (len(self.feedbacktaps)-1) # Initializing Output Buffer



    def work(self, input_items, output_items):

        self.input= input_items[0][0] # First sample of input vector
        self.output=0

        k= len(self.feedforward_taps)-1
        self.output=self.input * self.feedforward_taps[0]

        #################################################################
        # This operation will take care of IIR filter of variable length.
        for i in range(0, k):
            self.output+= self.feedforward_taps[i+1]* self.inputbuffer[len(self.inputbuffer)-1-i] - self.feedbacktaps[i+1]* self.outputbuffer[len(self.inputbuffer)-1-i]
        self.output/= self.feedbacktaps[0]
        ###############################################################3

        output_items[0][0] = self.output  # Populate our output_items array
        self.inputbuffer.append(input_items[0][0]) # Append inputbuffer
        self.outputbuffer.append(output_items[0][0]) # Append outputbuffer

        return 1
