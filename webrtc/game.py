SCR_SIZE = (640, 480)
HALFED_HEIGHT_SCR = SCR_SIZE[1] // 2
HALFED_SCR = (SCR_SIZE[0], HALFED_HEIGHT_SCR)
MON_SIZE= (1366, 768)
HALFED_SIZE_MON = (1366, 384)
TOP_GRAB = {'left':0, 'top': 0, 'width': HALFED_SIZE_MON[0], 'height':HALFED_SIZE_MON[1]}
DOWN_GRAB = {'left':0, 'top': HALFED_SIZE_MON[1], 'width': HALFED_SIZE_MON[0], 'height':HALFED_SIZE_MON[1]}

def grabber_top(queueTop, isRunning):
  from mss import mss
  from cv2 import resize, cvtColor, COLOR_BGRA2BGR
  from numpy import asarray
  global TOP_GRAB, SCR_SIZE
  with mss() as sct:
    while isRunning.value:
      queueTop.put(cvtColor(resize(asarray(sct.grab(TOP_GRAB)),(SCR_SIZE[0], SCR_SIZE[1]//2)), COLOR_BGRA2BGR))
  print('Top Grabber Finished!')

def grabber_down(queueDown, isRunning):
  from mss import mss
  from cv2 import resize, cvtColor, COLOR_BGRA2BGR
  from numpy import asarray
  global DOWN_GRAB, SCR_SIZE
  with mss() as sct:
    while isRunning.value:
      queueDown.put(cvtColor(resize(asarray(sct.grab(DOWN_GRAB)),(SCR_SIZE[0], SCR_SIZE[1]//2)), COLOR_BGRA2BGR))
  print('Down Grabber Finished!')

def displayer(queueTop, queueDown, isRunning):
  import pygame
  import pygame.display
  import pygame.image
  import pygame.time
  import pygame.font
  import pygame.event
  from pygame.locals import DOUBLEBUF
  global SCR_SIZE, HALFED_SIZE_MON, HALFED_SCR
  pygame.init()
  SCR = pygame.display.set_mode(SCR_SIZE, DOUBLEBUF)
  SCR.set_alpha(None)
  clock = pygame.time.Clock()
  FONT_COMIC = pygame.font.SysFont('Cambria Math', 20)
  topFrame = None
  downFrame = None
  while isRunning.value:
    clock.tick(60)
    for EVENT in pygame.event.get():
      if EVENT.type == pygame.QUIT:
        print('Quit Game')
        isRunning.value = 0

    if not queueTop.empty():
      topFrame = queueTop.get_nowait()
      SCR.blit(pygame.image.frombuffer(topFrame, HALFED_SCR, 'BGR'), (0,0))
      SCR.blit(FONT_COMIC.render(f'FPS: {str(clock.get_fps())[:5]}', False, (0,255,0)),(10,10))
      SCR.blit(FONT_COMIC.render(f'QUEUE: {str(queueTop.qsize())[:5]}, {str(queueDown.qsize())[:5]}', False, (0,255,0)),(10,30))
      pygame.display.update(0, 0,SCR_SIZE[0], HALFED_HEIGHT_SCR)
    if not queueDown.empty():
      downFrame = queueDown.get_nowait()
      SCR.blit(pygame.image.frombuffer(downFrame, HALFED_SCR, 'BGR'), (0,HALFED_HEIGHT_SCR))
      pygame.display.update(0, HALFED_HEIGHT_SCR, SCR_SIZE[0], HALFED_HEIGHT_SCR)
  print('Displayer Finished!')

if __name__ == "__main__":
  from multiprocessing import Process, Queue, Value
  from time import sleep
  queueTop = Queue(maxsize=5)
  queueDown = Queue(maxsize=5)
  isGameRunning = Value('i', 1)
  p1 = Process(target=grabber_top, args=(queueTop,isGameRunning, ))
  p2 = Process(target=grabber_down, args=(queueDown,isGameRunning, ))
  p3 = Process(target=displayer, args=(queueTop, queueDown,isGameRunning, ))
  p1.start()
  p2.start()
  p3.start()
  while isGameRunning.value:
    sleep(5)
  p1.terminate()
  p2.terminate()
  p3.terminate()
  print('All process terminated!')