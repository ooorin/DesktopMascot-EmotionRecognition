# coding: utf-8
from __future__ import print_function, division
import jieba
import win32api, win32con, win32gui
from PIL import Image, ImageFont, ImageDraw
import os
import random

root_path = os.path.split(os.path.realpath(__file__))[0] + '/'

class Classifier:

    def __init__(self):
        self.last_idx = 0
        self.idx = 0
        self.happy = open(root_path + 'data/happy.txt', 'r')
        self.angry = open(root_path + 'data/angry.txt', 'r')
        self.sad = open(root_path + 'data/sad.txt', 'r')
        self.fair = open(root_path + 'data/fair.txt', 'r')
        self.level = open(root_path + 'data/emotion_level.txt', 'r')
        self.neg = open(root_path + 'data/neg.txt', 'r')

        self.emotion = []

        self.happy_dic = {}
        self.angry_dic = {}
        self.sad_dic = {}
        self.fair_dic = {}
        self.level_dic = {}
        self.neg_dic = []
        self.read()

    def read(self):
        self.neg_dic = self.neg.read().split('\n')

        while True:
            line = self.happy.readline().split()
            if not line:
                break
            self.happy_dic[line[0]] = float(line[1])
        while True:
            line = self.angry.readline().split()
            if not line:
                break
            self.angry_dic[line[0]] = float(line[1])
        while True:
            line = self.sad.readline().split()
            if not line:
                break
            self.sad_dic[line[0]] = float(line[1])
        while True:
            line = self.fair.readline().split()
            if not line:
                break
            self.fair_dic[line[0]] = float(line[1])
        while True:
            line = self.level.readline().split()
            if not line:
                break
            self.level_dic[line[0]] = float(line[1])

    def classify(self, txt):
        self.emotion = []
        words = (' '.join(jieba.cut(txt)).split())
        words = [word.encode('utf-8') for word in words]
        score = [0, 0, 0, 0] # happy, angry, sad, fair
        head = 0

        for i in range(len(words)):
            neg_cnt = 0
            tmp_score = 0
            if words[i] in self.happy_dic and i >= head:
                self.emotion.append(words[i])
                tmp_score += self.happy_dic[words[i]]
                for j in range(head, i):
                    tmp_score *= (-1 if words[j] in self.neg_dic else 1)
                    tmp_score *= self.level_dic.get(words[j], 1)
                score[0] += tmp_score
                head += 1

            elif words[i] in self.angry_dic and i >= head:
                self.emotion.append(words[i])
                tmp_score += self.angry_dic[words[i]]
                for j in range(head, i):
                    tmp_score *= (-1 if words[j] in self.neg_dic else 1)
                    tmp_score *= self.level_dic.get(words[j], 1)
                score[1] += tmp_score
                head += 1
                
            elif words[i] in self.sad_dic and i >= head:
                self.emotion.append(words[i])
                tmp_score += self.sad_dic[words[i]]
                for j in range(head, i):
                    tmp_score *= (-1 if words[j] in self.neg_dic else 1)
                    tmp_score *= self.level_dic.get(words[j], 1)
                score[2] += tmp_score
                head += 1

            elif words[i] in self.fair_dic and i >= head:
                self.emotion.append(words[i])
                tmp_score += self.fair_dic[words[i]]
                for j in range(head, i):
                    tmp_score *= (-1 if words[j] in self.neg_dic else 1)
                    tmp_score *= self.level_dic.get(words[j], 1)
                score[3] += tmp_score
                head += 1

        tmp_score = [abs(tmp) for tmp in score]
        idx = tmp_score.index(max(tmp_score))
        if max(score) == 0 and min(score) == 0:
            self.idx = -1
        elif score[idx] < 0 and idx == 0:
            self.emotion = [(u'不'.encode('utf-8') + em) for em in self.emotion]
            self.idx = 2
        elif score[idx] < 0:
            self.emotion = [(u'不'.encode('utf-8') + em) for em in self.emotion]
            self.idx = 0
        else:
            self.idx = idx

    def wallpaper(self):
        k = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, 'Control Panel\Desktop', 0, win32con.KEY_ALL_ACCESS)
        current_path = win32api.RegQueryValueEx(k, 'Wallpaper')[0]
        if self.idx == -1:
            if os.path.exists(root_path + 'current_copy.bmp'):
                name = root_path + 'current_copy.bmp'
            else:
                name = current_path
        else:
            if self.idx == 0:
                path = 'Happy'
            elif self.idx == 1:
                path = 'Angry'
            elif self.idx == 2:
                path = 'Sad'
            else:
                path = 'Fair'
            ls = os.listdir(root_path + 'Wallpaper\\' + path)
            suffix = ['bmp', 'jpg', 'png', 'jpeg']
            ls = [l for l in ls if l.split('.')[-1].lower() in suffix]
            if len(ls) == 0:
                if os.path.exists('current_copy.bmp'):
                    name = root_path + 'current_copy.bmp'
                else:
                    name = current_path
            else:
                name = root_path + 'Wallpaper\\' + path + '\\' + ls[random.randint(0, len(ls) - 1)]

        img = Image.open(name)
        img_ = Image.open(name)
        font = ImageFont.truetype(root_path + "font.ttf", 180, encoding="utf-8")
        draw = ImageDraw.Draw(img)
        if len(self.emotion):
            draw.text((200, 500), unicode(' '.join(self.emotion), 'utf-8'), (255, 255, 255), font=font)
        else:
            draw.text((200, 500), unicode('一切正常', 'utf-8'), (255, 255, 255), font=font)
        img_.save(root_path + 'current_copy.bmp')
        img.save(root_path + 'current.bmp')
        win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, os.path.split(os.path.realpath(__file__))[0] + '\\' + 'current.bmp', 1+2)
        win32api.RegCloseKey(k)

if __name__ == '__main__':
    cl = Classifier()
    cl.classify(u'很开心')
    cl.wallpaper()