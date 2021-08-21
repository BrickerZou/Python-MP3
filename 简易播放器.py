import pygame
import time
file='C:/Users/lenovo/Music'
pygame.mixer.init()
print('正在播放',file)
track=pygame.mixer.music.load(file)
pygame.mixer.music.play()
time.sleep(123)
pygame.mixer.music.stop()