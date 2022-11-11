from channels.consumer import AsyncConsumer
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
import base64
import numpy as np

import os

from subprocess import Popen, PIPE, STDOUT
import subprocess
import pyscreenshot
from mss import mss
from io import BytesIO
from PIL import Image



class AudioConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name="screenshare"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
        img_buffer = BytesIO()
        pyscreenshot.grab().save(img_buffer, 'PNG', quality=50)
        img_buffer.seek(0)
        
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type":"chat_message",
                "text":img_buffer
            }
        )

    def disconnect(self):
        self.disconnect()

    def receive(self, text_data=None,bytes_data=None):
        #my_string = text_data
        print(my_string)
        
        
        # name=bytes_data
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

        




    def chat_message(self,event):
        message = event['text']
        self.send(bytes_data=(message))