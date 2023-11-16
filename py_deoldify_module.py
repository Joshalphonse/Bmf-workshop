import bmf
import numpy as np
from bmf import ProcessResult, Packet, Timestamp, VideoFrame
import PIL
import bmf.hml.hmp as mp

from deoldify import device
from deoldify.device_id import DeviceId
import torch
from deoldify.visualize import *
import warnings

debug = False

class py_deoldify_module(bmf.Module):
    def __init__(self, node, option=None):
        print(f'py_deoldify_module init ...')
        self.node_ = node
        self.option_ = option
        print(option)
        warnings.filterwarnings("ignore", category=UserWarning, message=".*?Your .*? set is empty.*?")

        #NOTE:  This must be the first call in order to work properly!
        #choices:  CPU, GPU0...GPU7
        device.set(device=DeviceId.GPU0)

        if not torch.cuda.is_available():
            print('warning: GPU is not available, the computation is going to be very slow...')

        weight_path=Path('/content/DeOldify')


#Task1
# Our module needs to use a specific set of weights for the DeOldify model, and these weights can 
# be located in different places. We have an option dictionary that might contain a custom path for these weights under the key 'model_path'. 
# How can we write a conditional statement that first checks if this custom path is provided 
# and then sets model_path to this value if it exists? 
#Task1
        
        self.colorizer = get_stable_video_colorizer(weight_path)
        self.idx = 0

        print(f'py_deoldify_module init successfully...')


    def process(self, task):
        # iterate through all input queues to the module
        idx = self.idx
#Task2
        
    #"In our module, we're dealing with multiple input queues, each potentially containing different video streams. 
    # How can we write a loop that goes through each of these input queues, processes the packets within them, and then 
    #places the results into the correct corresponding output queue? Also, consider how we should efficiently handle 
    #the situation where an input queue is empty. What would be a smart way to proceed when an input queue runs out of packets?"
        
#Task2

                # process packet if not empty
                if packet.timestamp != Timestamp.UNSET and packet.is_(VideoFrame):

                    vf = packet.get(VideoFrame)
                    rgb = mp.PixelInfo(mp.kPF_RGB24)
                    np_vf = vf.reformat(rgb).frame().plane(0).numpy()

                    # numpy to PIL
                    image = Image.fromarray(np_vf.astype('uint8'), 'RGB')

                    colored_image = self.colorizer.colorize_single_frame_from_image(image)

                    if not colored_image:
                        print(f'Fail to process the input image with idx = {idx}')
                        continue

                    if debug:
                        input_name = f'video/bmf_raw/frame_{idx}.png'
                        print(f'input_name = {input_name}')
                        image.save(input_name)

                        output_name = f'video/bmf_out/frame_{idx}.png'
                        print(f'output_name = {output_name}')
                        colored_image.save(output_name)

                    self.idx = idx + 1
                    #Task3
                    #In our colorization module, after we've successfully colorized an image, we need to convert it back into a format that
                    #  our video processing framework understands. We start by incrementing an index counter idx. 
                    # Can you think of why maintaining such a counter might be important in processing video frames? 
                    # Next, we need to convert our colorized image back into a frame. 
                    # How can we transform a colorized image (which is now a NumPy array) into a frame that's compatible with our BMF framework? 
                    # Also, consider the significance of setting properties like pts and time_base for the new frame. 
                    # What do these properties represent? 
                    # Why must they be accurately transferred from the original frame to the colorized frame?"
                    #Task3

                    output_queue.put(pkt)


        return ProcessResult.OK