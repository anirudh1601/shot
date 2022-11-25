from django.shortcuts import render
import pyscreenshot
from io import BytesIO
from django.http import HttpResponse,StreamingHttpResponse
import pyautogui
import numpy as np
import cv2
from mss import mss
from PIL import Image
from .cam import Camera
from time import time
from multiprocessing import Process
from vidgear.gears import ScreenGear
import threading
from rest_framework.response import Response
mon = {'left': 160, 'top': 160, 'width': 200, 'height': 200}
import pyautogui
import numpy as np
import cv2
from PIL import ImageGrab





MAX_FPS=60
MIN_FRAME_TIME=1/MAX_FPS

SCR_SIZE = (640, 480)
HALFED_HEIGHT_SCR = SCR_SIZE[1] // 2
HALFED_SCR = (SCR_SIZE[0], HALFED_HEIGHT_SCR)
MON_SIZE= (1366, 768)
HALFED_SIZE_MON = (1366, 384)
TOP_GRAB = {'left':0, 'top': 0, 'width': HALFED_SIZE_MON[0], 'height':HALFED_SIZE_MON[1]}
DOWN_GRAB = {'left':0, 'top': HALFED_SIZE_MON[1], 'width': HALFED_SIZE_MON[0], 'height':HALFED_SIZE_MON[1]}

def reducer(frame=None, percentage=0, interpolation=cv2.INTER_LANCZOS4):
    """
    ## reducer
    Reduces frame size by given percentage
    Parameters:
        frame (numpy.ndarray): inputs numpy array(frame).
        percentage (int/float): inputs size-reduction percentage.
        interpolation (int): Change resize interpolation.
    **Returns:**  A reduced numpy ndarray array.
    """
    # check if frame is valid
    if frame is None:
        raise ValueError("[Helper:ERROR] :: Input frame cannot be NoneType!")

    # check if valid reduction percentage is given
    if not (percentage > 0 and percentage < 90):
        raise ValueError(
            "[Helper:ERROR] :: Given frame-size reduction percentage is invalid, Kindly refer docs."
        )

    if not (isinstance(interpolation, int)):
        raise ValueError(
            "[Helper:ERROR] :: Given interpolation is invalid, Kindly refer docs."
        )

    # grab the frame size
    (height, width) = frame.shape[:2]

    # calculate the ratio of the width from percentage
    reduction = ((100 - percentage) / 100) * width
    ratio = reduction / float(width)
    # construct the dimensions
    dimensions = (int(reduction), int(height * ratio))

    # return the resized frame
    return cv2.resize(frame, dimensions, interpolation=interpolation)


def capture():

    w = 1920 # set this
    h = 1080 # set this
    bmpfilenamename = "out.bmp" #set this

    # hwnd = win32gui.FindWindow(None, windowname)
    hwnd = None

    wDC = win32gui.GetWindowDC(hwnd)
    dcObj=win32ui.CreateDCFromHandle(wDC)
    cDC=dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0,0),(w, h) , dcObj, (0,0), win32con.SRCCOPY)
    # dataBitMap.SaveBitmapFile(cDC, bmpfilenamename)
    bmpinfo = dataBitMap.GetInfo()
    bmpstr = dataBitMap.GetBitmapBits(True)
    img = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX')
        # Free Resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

    return img


left = 0
right=2
top=0
btm=2
def serve_pil_image(request):
    loop = time()
    # printscreen_pil =  ImageGrab.grab()
    # printscreen_numpy =   np.array(printscreen_pil.getdata(),dtype='uint8').reshape((printscreen_pil.size[1],printscreen_pil.size[0],3)) 
    # # img = ImageGrab.grab(bbox=(0, 1000, 100, 1100)) #x, y, w, h
    # # img_np = np.array(img)
    # # frame =  reducer(img_np, percentage=30) 
    # encodedImage = cv2.imencode(".jpg", printscreen_numpy)[1].tobytes()
    # yield (b"--frame\r\nContent-Type:video/jpeg2000\r\n\r\n" + encodedImage + b"\r\n")
    #img = ImageGrab.grab()
    #print(screenshot)
    with mss(display=":0.0") as sct:
       
        monitor = sct.monitors[1]
        bbox = (left,top,right,btm)
        # left = monitor["left"]
        # top = monitor["top"]
        # right = left + 1
        # lower = top + 1
        # bbox = (TOP_GRAB, DOWN_GRAB)
        # Grab the picture
        im = sct.grab(monitor)
        
        # print(pyscreenshot.grab())
        # Get the entire PNG raw bytes
        # print(im)
        #raw_bytes = mss.tools.to_png(im.rgb, im.size)
        
        img = Image.frombytes('RGB',im.size,im.bgra,"raw",'BGRX')
        #print(img)
        print("fps {}".format(1/(time()-loop)))
        response = HttpResponse(content_type='multipart/x-mixed-replace; boundary=frame')
        img.save(response, "jpeg")
        return response 
        
    #     yield (b'--frame\r\n'
    #    b'Content-Type:image/jpeg\r\n'
    #    b'Content-Length: ' + f"{len(img.tobytes())}".encode() + b'\r\n'
    #    b'\r\n' + img.tobytes() + b'\r\n')
    #     #yield (b'Content-Type: image/jpeg\r\n\r\n' + img.tobytes() + b'\r\n')
    #     #img = img.resize((900,600),Image.NEAREST)
    #     #print(type(img))
    #     # img_buffer = BytesIO()
    #     # pyscreenshot.grab().save(img_buffer, 'jpeg', quality=50)
    #     # img_buffer.seek(0)
    #     # print(img_buffer)
        
            
    
def serve(request):
    mjpeg = serve()
    return StreamingHttpResponse(mjpeg, content_type='multipart/x-mixed-replace;boundary=frame')
    # response = HttpResponse(content_type='multipart/x-mixed-replace; boundary=frame')
    # img.save(response, "jpeg")
    # return response
    





def send_js(request,path):
    return flask.send_from_directory('js', path)

# Create your views here.
def audio(request):
    return render(request,'webrtc/a.html')