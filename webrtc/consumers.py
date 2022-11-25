from channels.consumer import AsyncConsumer
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
import json
import base64
import numpy as np
from time import time
import os
from io import BytesIO
from subprocess import Popen, PIPE, STDOUT
import subprocess
import pyscreenshot
from mss import mss
from io import BytesIO
from PIL import Image
import json
from mss import mss

class AudioConsumer(AsyncWebsocketConsumer):
    
    async def websocket_connect(self,event):
        self.room_group_name="screenshare"
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        


    async def websocket_disconnect(self):
        await self.disconnect()

    async def websocket_receive(self, event):
        received_data = json.loads(event['text'])
        msg1 = received_data.get('message')
        
        #         loop = time()
        # with mss(display=":0.0") as sct:
        #     fp =BytesIO()
        #     monitor = sct.monitors[1]

        #     # left = monitor["left"]
        #     # top = monitor["top"]
        #     # right = left + 1
        #     # lower = top + 1
        #     # bbox = (TOP_GRAB, DOWN_GRAB)
        #     # Grab the picture
        #     im = sct.grab(monitor)
            
        #     # print(pyscreenshot.grab())
        #     # Get the entire PNG raw bytes
        #     # print(im)
        #     #raw_bytes = mss.tools.to_png(im.rgb, im.size)
            
        #     img = Image.frombytes('RGB',im.size,im.bgra,"raw",'BGRX')
        #     img.save(fp, 'JPEG')
        #     image = base64.b64encode(fp.getvalue())
        #     #print(img)
        #     print("fps {}".format(1/(time()-loop)))
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type":"chat_message",
                "text":msg1
            }
        )
        # name=bytes_datate
        #print(my_string)
        #os.system('ls')
        # cmd = ["ffmpeg -i - -vcodec libvpx -keyint_min 60 -g 60 -vb 4000k -f webm -cluster_size_limit 10M -cluster_time_limit 2100 out.webm"]
        # # p = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE,shell=False)
        # # out, err = p.communicate(input=my_string.read(), timeout=None)
        # ffmpeg_cmd = subprocess.Popen(
        #     cmd,
        #     stdin=subprocess.PIPE,
        #     stdout=subprocess.PIPE,
        #     shell=False
        # )
        # ffmpeg_cmd.stdin.write(my_string)
        # ffmpeg_cmd.stdin.close()
        # #hi = os.system('ffmpeg -i pipe: -vcodec libvpx -keyint_min 60 -g 60 -vb 4000k -f webm -cluster_size_limit 10M -cluster_time_limit 2100 out.webm')
        # print(ffmpeg_cmd)
        #print(my_string)
        #print(my_string)
        # print(str(my_string))
        # list1 = []
        # aud = np.frombuffer(my_string,dtype=np.float32)
        # for a in aud:
        #     string = str(a)
        #     list1.append(string)


        
        # for a in aud:
        #     string = str(a)
        #     list1.remove(string)

        




    async def chat_message(self,event):
        message = event['text']
        await self.send(text_data=message)