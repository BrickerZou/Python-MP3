import os
import tkinter
from tkinter import Canvas,PhotoImage
from PIL import Image, ImageTk
# import tkinter.filedialog
import time
import random
import threading
import pygame
import ctypes



#高像素

#创建窗口，root可替换成自己定义的窗口
root =tkinter.Tk()
#调用api设置成由应用程序缩放
ctypes.windll.shcore.SetProcessDpiAwareness(1)
#调用api获得当前的缩放因子
ScaleFactor=ctypes.windll.shcore.GetScaleFactorForDevice(0)
#设置缩放因子
root.tk.call('tk', 'scaling', ScaleFactor/80)


# step 1: 搭建界面
# root =tkinter.Tk()

root.attributes('-alpha',1)

root.title('8.13音乐播放器')
# 图标
root.iconbitmap('star.ico')
# 窗口大小和位置
root.geometry('460x600+550+100')
# 禁止拉伸
root.resizable(False,False)

#设置背景图片
canvas = tkinter.Canvas(root, width=460, height=600, bd=0, highlightthickness=0)
# imgpath = str(random.randint(1,3))+'.jpg'
imgpath = '2.jpg'
img = Image.open(imgpath)
photo = ImageTk.PhotoImage(img)
canvas.create_image(300, 306, image=photo)
canvas.pack()




folder = 'C:/Users/lenovo/Music'
res = []
num = random.randint(0,13)     #随机播放
# now_music = ''

# 功能函数
def buttonaddClick():
    global folder
    global res
    if folder:
        # folder = tkinter.filedialog.askdirectory() # 选择目录
        musics = [folder +'/' + music
                 for music in os.listdir(folder)
                 if music.endswith('.mp3')]
        ret=[]
        for i in musics:
            ret.append(i.split('/')[-1][:-4])# 获取歌曲名
            res.append(i)
        var2 = tkinter.StringVar()
        var2.set(ret)
        lb = tkinter.Listbox(root,listvariable=var2,background='SkyBlue')
        lb.place(x=80,y=120,width=260,height=260)
        global playing
        playing = True
        # 歌单导出，按键解除禁用状态
        buttonPlay['state'] = 'normal'
        buttonStop['state'] = 'normal'

        pause_resume.set('播放')

def play():
    # if (len(res)):
    pygame.mixer.init()
    global num

    while playing:
        if not pygame.mixer.music.get_busy():    # 音乐播放完
            nextMusic = res[num]
            print(nextMusic.split('/')[-1][:-4])
            print(num)
            pygame.mixer.music.load(nextMusic.encode())
            pygame.mixer.music.play(1)  #播放
            if len(res)-1==num:
                num=0
            else:
                num=num+1
            nextMusic = nextMusic.split('/')[-1][:-4]
            musicName.set('~~~'+nextMusic+'~~~')
        else:
            time.sleep(0.1)

def buttonPlayClick():
    global  pause_resume,playing
    buttonPre['state'] = 'normal'
    buttonNext['state'] = 'normal'
    if pause_resume.get() == '播放':
        pause_resume.set('暂停')

        playing = True

        #增加一个线程播放音乐
        t = threading.Thread(target=play)  # play函数
        t.start()

    elif pause_resume.get() == '暂停':
        playing = False       #*****
        pygame.mixer.music.pause()
        pause_resume.set('继续')
    elif pause_resume.get() == '继续':
        playing = True
        pygame.mixer.music.unpause()
        pause_resume.set('暂停')




def buttonStopClick():
    global playing

    playing = False

    pygame.mixer.music.stop()



def buttonPreClick():
    global playing
    playing = False
    pygame.mixer.music.stop()
    global num
    if num == 0:
        num = len(res)-2
    else:
        num-= 2
    playing = True

    # 增加一个线程播放音乐
    t = threading.Thread(target=play)  # play函数    num+1
    t.start()


def buttonNextClick():
    global playing
    playing = False
    pygame.mixer.music.stop()

    global num
    if len(res)-1== num:
        num=-1
    playing = True

    # 增加一个线程播放音乐
    t = threading.Thread(target=play)  # play函数   num+1
    t.start()

def END():
    try:
        pygame.mixer.music.stop()
        pygame.mixer.quit()
    except:
        pass
    global root
    root2.destroy()
    root.destroy()     # 关闭窗口
def closeWindow():
    global root2    # 退出界面
    root2 = tkinter.Tk()
    root2.title('退出界面')
    root2.geometry('360x200+600+250')
    buttonStop = tkinter.Button(root2, text='确认关闭',fg = "red", bg = "blue",command=END)
    buttonStop.place(x=154, y=65, width=75, height=35)
def contorlVoice(value=30):
    pygame.mixer.music.set_volume(value/100)


# 关闭窗口
root.protocol('WM_DELETE_WINDOW',closeWindow)

# 添加歌单按钮
buttonadd = tkinter.Button(root,text='添加',command=buttonaddClick,bg='SkyBlue')
# 布局
buttonadd.place(x=80,y=10,width=50,height=20)


# 跟踪变量
pause_resume= tkinter.StringVar(root,value='随播')   # 可以更改
# 添加按钮
buttonPlay = tkinter.Button(root,textvariable=pause_resume,command=buttonPlayClick,bg='SkyBlue')
buttonPlay.place(x=140,y=10,width=50,height=20)
# 禁用状态
buttonPlay['state'] = 'disabled'

#
#停止
buttonStop = tkinter.Button(root,text='停止',command=buttonStopClick,bg='SkyBlue')
buttonStop.place(x=190,y=10,width=50,height=20)
buttonStop['state'] = 'disabled'

# 下一首
buttonNext = tkinter.Button(root,text='下一首',command=buttonNextClick,bg='SkyBlue')
buttonNext.place(x=260,y=10,width=50,height=20)
buttonNext['state'] = 'disabled'

# 上一首
buttonPre = tkinter.Button(root,text='上一首',command=buttonPreClick,bg='SkyBlue')
buttonPre.place(x=310,y=10,width=50,height=20)
buttonPre['state'] = 'disabled'

musicName = tkinter.StringVar(root,value="暂时没有播放音乐...")   #可以更改
labelName = tkinter.Label(root,textvariable=musicName,fg = "SeaGreen",bg='FloralWhite')
labelName.place(x=80,y=33,width=279,height=20)

#
s=tkinter.Scale(root,label='',bg='FloralWhite',fg = "DeepSkyBlue",from_=0,to_=100,orient=tkinter.HORIZONTAL,length=290,showvalue=0,tickinterval=25,resolution=0.1,command=contorlVoice)
s.place(x=80,y=52,width=279)

root.mainloop()

