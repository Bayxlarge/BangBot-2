#bangbot by bang
import requests
import os
import json
import keyboard 
import socketio 
import threading
import math
import random
import time
import urllib.request
import pyautogui
import math
import PIL
import numpy as np
import itertools
from itertools import cycle
from numpy import sqrt
from PIL import Image, ImageGrab, ImageDraw, ImageFont
from ast import literal_eval as make_tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sio = socketio.Client()
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--disable-webgl")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)

#######################################################################Higher PPS means speed bot.50 is limit.
PPS=50
speed = 1/PPS
#######################################################################
class Bang_Bot():   
    def __init__(self):
        self.chart = 7 #the map
        self.get_chart()

        self.authkey = None
        self.authtoken = None
        self.authid = None
        self.initial_login()

        self.key = 'f9'
        self.hotkeys()

        self.socket_connection()

    def get_color_index(self):
        try:
            cid = str(driver.find_element(By.XPATH,'/html/body/div[3]/div[2]').get_attribute("style"))
            a = cid.find('(')
            b = cid.find(')');b+=1
            cid = cid[a:b]
        finally:
            return self.get_color(make_tuple(cid))

    def get_color(self, input):
        if type(input) == int:
            return colors_reverse[(input)]
        elif type(input) == tuple:
            return colors[(input)]
        else:
            return None                              

    
    def get_coord(self):
        try:
            self.x, self.y = make_tuple(driver.find_element(By.XPATH,'/html/body/div[3]/div[4]').text)
            return self.x, self.y
            self.x, self.y = self.xy
        except:
             pass
            
    def hotkeys(self): #add more hotkeys in this section
        keyboard.add_hotkey('w', lambda: self.sus())
        keyboard.add_hotkey('z', lambda: self.tv()) 
        keyboard.add_hotkey('x', lambda: self.bomb())
        keyboard.add_hotkey('a', lambda: self.fill())
        keyboard.add_hotkey('p', lambda: self.protect())#Protecting selected pixels
        keyboard.add_hotkey('d', lambda: self.dotting())
        keyboard.add_hotkey('ç', lambda: self.circular())
        keyboard.add_hotkey('y', lambda: self.circularbang())
        keyboard.add_hotkey('m', lambda: self.multi_circle_zone())
        keyboard.add_hotkey('shift+r', lambda: self.new_fill())
        keyboard.add_hotkey('r', lambda: self.rndmnss_fill())
        keyboard.add_hotkey('shift+c', lambda: self.forever_circle())

    
    def forever_circle(self):
        x2,y2=self.get_coord()
        c=self.get_color_index()
        r=1
        plist = []
        while True:
            for i in range(x2-r, x2+r+1):
                for j in range(y2-r, y2+r+1):
                    distance = math.sqrt((i-x2)**2 + (j-y2)**2)
                    if distance <= r and distance >= r-1:
                        plist.append((i,j))
            plist= sorted(plist, key=lambda x: ((x[0]-x2)**2 + (x[1]-y2)**2)**0.5)
            for x,y in plist:
                if keyboard.is_pressed('q'):
                    return
                if self.cache[x,y] not in [colors_reverse[c]] + [(204,204,204)]:
                    sio.emit("p", [x, y, c, 1])
                    time.sleep(speed)
            plist=[]
            r+=1
        
    def circularbang(self):#Circular pattern
        x1, y1 = self.get_coord()
        while keyboard.is_pressed('y'):
             pass
        x2, y2 = self.get_coord()
        c=self.get_color_index()
        center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2 # center of the selected area
        pixels = []
        for x in range(x1, x2+1):
            for y in range(y1, y2+1):
                pixels.append((x, y))
                
        pixels= sorted(pixels, key=lambda x: ((x[0]-center_x)**2 + (x[1]-center_y)**2)**0.5)
        while True:
            if keyboard.is_pressed('q'):
                return
            for x,y in pixels:
                if self.cache[x,y] not in [colors_reverse[c]] + [(204,204,204)]:
                     if keyboard.is_pressed('q'):
                         print("Cancelled.")
                         return
                     sio.emit("p", [x, y, c, 1])
                     time.sleep(speed)

    def multi_circle_zone(self):    
        x1, y1 = self.get_coord()
        while keyboard.is_pressed('m'):
             pass
        x2, y2 = self.get_coord()
        c=self.get_color_index()
        pixels = []
        for x in range(x1, x2+1):
            for y in range(y1, y2+1):
                pixels.append((x, y))
    
        random_points = random.sample(pixels, 3)
        pixels.sort(key=lambda p: min([((p[0]-rp[0])**2 + (p[1]-rp[1])**2)**0.5 for rp in random_points]))
        while True:
            for p in pixels:
                if self.cache[p[0],p[1]] not in [colors_reverse[c]] + [(204,204,204)]:
                    if keyboard.is_pressed('q'):
                        print("Cancelled.")
                        return
                    sio.emit("p", [p[0], p[1], c, 1])
                    time.sleep(0.02)
               
        '''                
        #İt'll make baklava shape
        x1,y1=self.get_coord()
        x2,y2=int(input("X2: ")),int(input("Y2: "))
        c=self.get_color_index()
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        pixels = []
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                pixels.append([x, y])

        pixels.sort(key=lambda x: abs(x[0] - mid_x) + abs(x[1] - mid_y))
        
        for pixel in pixels:
            if self.cache[pixel[0],pixel[1]] not in [colors_reverse[c]] + [(204,204,204)]:
                sio.emit("p", [pixel[0], pixel[1], c, 1])
                time.sleep(0.02)
        '''
    
    def circular(self):#Xiaolin Wu
        c=self.get_color_index()
        x1, y1 = self.get_coord()
        while keyboard.is_pressed('ç'):
             pass
        x0, y0 = self.get_coord()
        radius=int(math.sqrt((x0-x1)**2 + (y0-y1)**2))
        color=self.get_color_index()
        x = radius
        y = 0
        decision = 5/4 - radius
        while x >= y:
            sio.emit("p", [x + x0, y + y0, color, 1])
            time.sleep(speed)
            sio.emit("p", [y + x0, x + y0, color, 1])
            time.sleep(speed)
            sio.emit("p", [-x + x0, y + y0, color, 1])
            time.sleep(speed)
            sio.emit("p", [-y + x0, x + y0, color, 1])
            time.sleep(speed)
            sio.emit("p", [-x + x0, -y + y0, color, 1])
            time.sleep(speed)
            sio.emit("p", [-y + x0, -x + y0, color, 1])
            time.sleep(speed)
            sio.emit("p", [x + x0, -y + y0, color, 1])
            time.sleep(speed)
            sio.emit("p", [y + x0, -x + y0, color, 1])
            time.sleep(speed)
            if decision < 0:
                decision = decision + 2 * y + 1
            else:
                decision = decision + 2 * (y - x) + 1
                x = x - 1
            y = y + 1
    
    def rndmnss_fill(self):#İt's not available for now.
        color = self.get_color_index()
        x1, y1 = self.get_coord()
        while keyboard.is_pressed('r'):
             pass
        x2, y2 = self.get_coord()
        

    def new_fill(self):
        color = self.get_color_index()
        x1, y1 = self.get_coord()
        while keyboard.is_pressed('shift+r'):
             pass
        x2, y2 = self.get_coord()
        height, width = abs(y2 - y1), abs(x2 - x1)
        
        for loop in range (width):
            x1,y1,x2,y2 = x1+1,y1+1,x2-1,y2-1
            for x in range (x1 ,x2 + 1):
                sio.emit("p",[x,y1, color, 1])
                sio.emit("p",[x,y2, color, 1])
                time.sleep(0.04)
            for y in range (y2 + 1,y1,-1):
                sio.emit("p",[x1,y, color, 1])
                sio.emit("p",[x2,y, color, 1])
                time.sleep(0.04)       
            

     
    def dotting (self):
        color = self.get_color_index()
        x1, y1 = self.get_coord()
        while keyboard.is_pressed('d'):
             pass
        x2, y2 = self.get_coord()
        while True:
            x = random.randint(x1 , x2)
            y = random.randint(y1 , y2)
            if self.cache[x,y] not in [colors_reverse[color]] + [(204,204,204)]:
                sio.emit("p",[x,y,color,1])
                time.sleep(speed)
                
            if keyboard.is_pressed('q'):
             print("Cancelled.")
             return
            
            
        
    def protect(self):
     color = self.get_color_index()
     x, y = self.get_coord()    
     pixel_list = []
     pixel_list += [[x, y, color],]    
     while True:              
         for pixel in pixel_list:
             if keyboard.is_pressed('q'):
                 print("Cancelled.")
                 return
             if keyboard.is_pressed('p'):
                 color = self.get_color_index()
                 x, y = self.get_coord()
                 pixel_list += [[x, y, color],]
                 time.sleep(speed) 
             if self.cache[pixel[0],pixel[1]] not in [colors_reverse[color]] + [(204,204,204)]:
                 sio.emit("p",[pixel[0] , pixel[1] , pixel[2] , 1])
                 time.sleep(speed)
            
    def fill(self):
        color = self.get_color_index()
        x1, y1 = self.get_coord()
        while keyboard.is_pressed('a'):
             pass
        x2, y2 = self.get_coord()
        while True:
            if keyboard.is_pressed('q'):
                return
            for x in range (x1, x2 + 1):
                for y in range (y1, y2 + 1):
                    if self.cache[x,y] not in [colors_reverse[color]] + [(204,204,204)]:
                        if keyboard.is_pressed('q'):
                            print("Cancelled.")
                            return
                        sio.emit("p",[x,y,color, 1])
                        time.sleep(speed)
    
    def bomb(self):
        self.get_coord()
        color = self.get_color_index()
        for x in range(7):
            for y in range(7):
                sio.emit("p",[self.x + x, self.y +y, color, 1])
        time.sleep (1)
                

    def tv(self):
        self.get_coord()
        size = int(input("Enter Tv size:  ")) 
        print ("Start TV  press q to stop.")
        while True:
             if keyboard.is_pressed('q'):
                print("Cancelled.")
                time.sleep(1)
                return
             sio.emit("p",[self.x + random.randint(0 , size), self.y + random.randint(0 , size), random.randint(0 , 38), 1])
             time.sleep(speed)
           
    def sus(self):
        self.get_coord()
        suscolor = random.randint(0, 38)
        sio.emit("p",[self.x, self.y, suscolor, 1])
        sio.emit("p",[self.x - 1, self.y, suscolor, 1])
        sio.emit("p",[self.x - 2, self.y, suscolor, 1])
        sio.emit("p",[self.x - 2, self.y + 1, suscolor, 1])
        sio.emit("p",[self.x - 2, self.y + 2, suscolor, 1])
        sio.emit("p",[self.x - 1, self.y + 2, suscolor, 1])
        sio.emit("p",[self.x, self.y + 2, suscolor, 1])
        sio.emit("p",[self.x - 3, self.y + 1, suscolor, 1])
        sio.emit("p",[self.x - 3, self.y + 2, suscolor, 1])
        sio.emit("p",[self.x , self.y + 3, suscolor, 1])
        sio.emit("p",[self.x - 1, self.y + 3, suscolor, 1])
        sio.emit("p",[self.x - 2, self.y + 3, suscolor, 1])
        sio.emit("p",[self.x , self.y + 4, suscolor, 1])
        sio.emit("p",[self.x - 2, self.y + 4, suscolor, 1])
        sio.emit("p",[self.x, self.y + 1, 0, 1])
        sio.emit("p",[self.x - 1, self.y + 1, 0, 1])
        time.sleep(0.32)
    

    def initial_login(self):
        print (' Welcome to bangbot')
        time.sleep(2)
        print (' Pixelplace is opening...')
        driver.get("https://pixelplace.io")
        while self.authkey == None or self.authtoken == None or self.authid == None:
            try:
                self.authkey = driver.get_cookie("authKey").get('value')
                self.authtoken = driver.get_cookie("authToken").get('value')
                self.authid = driver.get_cookie("authId").get('value')    
                print('Logged in.')
            except:
                print('Please log in.')
                time.sleep(5)
                pass
          
    def socket_connection(self):
        sio.connect('https://pixelplace.io', transports=['websocket'])

        @sio.event
        def connect():
            sio.emit("init",{"authKey":f"{self.authkey}","authToken":f"{self.authtoken}","authId":f"{self.authid}","boardId":self.chart})
            threading.Timer(15, connect).start()      
        
        @sio.on("p")        
        def update_pixels(p: tuple): 
            for i in p:
                self.cache[i[0], i[1]] = colors_reverse[i[2]]    
        
    def get_chart(self):
        with open(f'{self.chart}.png', 'wb') as f:
            f.write(requests.get(f'https://pixelplace.io/canvas/{self.chart}.png?t={random.randint(999,9999)}').content)
        image = PIL.Image.open(f'{self.chart}.png').convert('RGB')
        self.cache = image.load()
        
colors = {(255, 255, 255): 0,  (196, 196, 196): 1,
          (136, 136, 136): 2,  (85, 85, 85): 3,
          (34, 34, 34): 4,     (0, 0, 0): 5,
          (0, 54, 56): 39,     (0, 102, 0): 6,
          (27, 116, 0): 49,    (71, 112, 80): 40,
          (34, 177, 76): 7,    (2, 190, 1): 8,
          (81, 225, 25): 9,    (148, 224, 68): 10,
          (152, 251, 152): 41, (251, 255, 91): 11,
          (229, 217, 0): 12,   (230, 190, 12): 13,
          (229, 149, 0): 14,   (255, 112, 0): 42,
          (255, 57, 4): 21,    (229, 0, 0): 20,
          (206, 41, 57): 43,   (255, 65, 106): 44,
          (159, 0, 0): 19,     (107, 0, 0): 18,
          (255, 117, 95): 23,  (160, 106, 66): 15,
          (99, 60, 31): 17,    (153, 83, 13): 16,
          (187, 79, 0): 22,    (255, 196, 159): 24,
          (255, 223, 204): 25, (255, 167, 209): 26,
          (207, 110, 228): 27, (125, 38, 205): 45,
          (236, 8, 236): 28,   (130, 0, 128): 29,
          (51, 0, 119): 46,    (2, 7, 99): 31,
          (81, 0, 255): 30,    (0, 0, 234): 32,
          (4, 75, 255): 33,    (0, 91, 161): 47,
          (101, 131, 207): 34, (54, 186, 255): 35,
          (0, 131, 199): 36,   (0, 211, 221): 37,
          (69, 255, 200): 38,  (181, 232, 238): 48}
ocean_list = [33,47,34,35,36,38]
colors_reverse = {value: key for key, value in zip(colors.keys(), colors.values())}
bangbot = Bang_Bot()
