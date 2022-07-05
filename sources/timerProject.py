###!/usr/bin/env

import os,sys
sys.path.append('/usr/local/lib/python3.9')
sys.path.append('/usr/local/lib/python3.9/lib-dynload')
sys.path.append('/usr/local/lib/python3.9/site-packages')

import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo

import threading
from pprint import pprint

import time
from datetime import datetime

## python script to display timer and ount down 
## Author :   D. VERBEKE
## Date : 03/07/2022 - Moirans
## Version : 0.01

class countDown :
    def __init__(self,nb_sec_down):
        threading.Thread.__init__(self)
        self.nb_sec_down=nb_sec_down
        self._stop = threading.Event()

    def run(self, nb_sec_down):
        self.nb_sec_down=nb_sec_down
        m, s = divmod(self.nb_sec_down, 60)
        self.min_sec_format = '{:02d}:{:02d}'.format(m, s)
        ## print(f'Start count down {self.min_sec_format}')

        while self.nb_sec_down:
            if self.stopped():
                ## print('thread is stopped')
                return
            time.sleep(1)
            self.nb_sec_down -= 1
            m, s = divmod(self.nb_sec_down, 60)
            self.min_sec_format = '{:02d}:{:02d}'.format(m, s)
            lblCountDown.config(text="Countdown : "+str(self.min_sec_format))
        print('Countdown finished.')
        return

    def stop(self,nb_sec_down):
        self.nb_sec_down=nb_sec_down
        m, s = divmod(self.nb_sec_down, 60)
        self.min_sec_format='{:02d}:{:02d}'.format(m, s)
        lblCountDown.config(text=f'CountDown : {self.min_sec_format}')
        self._stop.set()
        return
    
    def stopped(self):
        return self._stop.isSet()
    
    def restart(self):
        ## print(f'Restart countdown : {self.min_sec_format}')
        return self._stop.clear()
    
    def reset(self,nb_sec_down):
        self.nb_sec_down=nb_sec_down
        m, s = divmod(self.nb_sec_down, 60)
        self.min_sec_format='{:02d}:{:02d}'.format(m, s)
        lblCountDown.config(text=f'CountDown : {self.min_sec_format}')
        return self._stop.clear()
    
class countTime :
    def __init__(self):
        threading.Thread.__init__(self)
        self._running=True
        self.nb_sec_timer=0
        self.count=0
        self.previousTime=0
        self._stop = threading.Event()
        
    def run(self, n):
        self.count+=1
        self.nb_sec_timer=n
        m, s = divmod(self.nb_sec_timer, 60)
        self.min_sec_format = '{:02d}:{:02d}'.format(m, s)
        ## print(f'Start timer : {self.min_sec_format}')
        while self._running :
            if self.stopped():
                print('thread is stopped')
                return
            time.sleep(1)
            self.nb_sec_timer += 1
            m, s = divmod(self.nb_sec_timer, 60)
            self.min_sec_format = '{:02d}:{:02d}'.format(m, s)
            lblTimer.config(text=f'Timer : {self.min_sec_format}')

    def stop(self):
        self._running = False
        self.previousTime=self.nb_sec_timer
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()
    
    def restart(self):
        ## print(f'Restart timer : {self.min_sec_format}')
        self._running = True
        return self._stop.clear()
    
    def reset(self):
        ## print(f'Reset timer : {self.min_sec_format}')
        self.nb_sec_timer=0
        self.previousTime=0
        self.count=0
        m, s = divmod(self.nb_sec_timer, 60)
        self.min_sec_format='{:02d}:{:02d}'.format(0, 0)
        lblTimer.config(text=f'Timer : {self.min_sec_format}')
        self._running = True
        return self._stop.clear()
 
## define timer for material and geometric sequence
global tmax
minuteNumberDefault=int(180)
tmax=minuteNumberDefault
m, s = divmod(tmax, 60)
countDownInit= '{:02d}:{:02d}'.format(m, s)

### thread for timer
def thread_startTimer():
    n=0
    th_Timer = threading.Thread(target = countTimeObject.run, args =(n, ))
    if th_Timer.is_alive():
        th_Timer.join()
    th_Timer.start()
    return

def thread_stopTimer():
    ##print('stop thread timer')
    countTimeObject.stop()
    return

def thread_resetTimer():
    countTimeObject.stop() ## termine le thread courant
    countTimeObject.reset()
    return

## thread for countDown
def thread_startCountDown(initVal:int):
    th_countDown = threading.Thread(target = countDownObject.run, args =(initVal, ))
    if th_countDown.is_alive():
        th_countDown.join()
    th_countDown.start()
    return

def thread_stopCountDown(initVal:int):
    countDownObject.stop(initVal)
    return

def thread_resetCountDown(initVal:int):
    countDownObject.reset(initVal)
    return

################################  GUI FRAME ##############################################################"
if __name__ == '__main__':

    ## create timer object
    global countTimeObject
    countTimeObject=countTime()

    global countDownObject
    countDownObject=countDown(tmax)
    
    root = Tk()
    root.geometry('430x250')
    root.title(str(datetime.now().strftime("%d/%m/%Y -- %H:%M:%S ")) )

    frameMain=tk.LabelFrame(root, text ="")
    frameMain.grid(column=0, row=0,columnspan=2, sticky=W)

    lblTimer=Label(frameMain, text=f'Timer : 00:00' )
    lblTimer.grid(column=0, row=0, sticky=W)

    lblCountDown=Label(frameMain,  text=f'Countdown : {countDownInit}')
    lblCountDown.grid(column=1, row=0, sticky=W)

    ttk.Button(frameMain , text="Start timer",command=lambda:thread_startTimer(),width=20).grid(column=0, row=1)
    ttk.Button(frameMain , text="Reset timer",command=lambda: thread_resetTimer(), width=20).grid(column=0, row=2)
    ttk.Button(frameMain , text="Stop timer",command=lambda: thread_stopTimer(), width=20).grid(column=0, row=3)

    ttk.Button(frameMain , text="Start count down",command=lambda:thread_startCountDown(tmax),width=20).grid(column=1, row=1)
    ttk.Button(frameMain , text="Reset count down",command=lambda: thread_resetCountDown(tmax), width=20).grid(column=1, row=2)
    ttk.Button(frameMain , text="Stop count down",command=lambda: thread_stopCountDown(tmax), width=20).grid(column=1, row=3)


    for child in frameMain.winfo_children(): 
        child.grid_configure(padx=5, pady=5)

    root.mainloop()
