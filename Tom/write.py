#coding: utf-8
from Tom_Data.StreamingAssets import wallpaper

if __name__ == '__main__':
	cl = wallpaper.Classifier()
	while True:
		response = raw_input('写下你的心情吧：'.decode('utf-8').encode('gbk'))
		cl.classify(response)
		cl.wallpaper()
		file = open('Tom_Data/StreamingAssets/emotion.txt', 'w')
		file.write(str(cl.idx + 1))
		file.close()