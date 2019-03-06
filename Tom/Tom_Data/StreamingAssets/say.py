#coding: utf-8
import wallpaper
import speech

if __name__ == '__main__':
	cl = wallpaper.Classifier()
	while True:
		response = speech.input('说下你的心情吧：')
		cl.classify(response)
		cl.wallpaper()
		file = open('emotion.txt', 'w')
		file.write(str(cl.idx + 1))
		file.close()