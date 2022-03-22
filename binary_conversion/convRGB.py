from PIL import Image
import math
import os
import time
import glob
import concurrent.futures

start_time = time.time()
fileDir = "./temp/"
outputDir = "./RGBs/"
resources = os.listdir(fileDir)

def generateImages(appname):
	if (str(appname) == ".DS_Store"):
		return
	temp = str(appname).index(".txt")
	app_name = str(appname)[:temp]
	print("Converting: " + str(app_name))
	f = open(fileDir + str(appname), "r")
	line = f.readlines()[0].split("\t")
	X = int(math.ceil(math.sqrt(len(line))))
	Y = X
	index = 0
	image = Image.new("RGB", (X, Y))
	for x in range(0, X):
		for y in range(0, Y):
			if (len(line[index]) == 0):
				continue
			if (index > len(line)):
				image.putpixel((x, y), (0, 0, 0))
				continue
			rgb = line[index].split(",")
			image.putpixel((x, y), (int(rgb[0]), int(rgb[1]), int(rgb[2])))
			index += 1
	image.save(outputDir + app_name + ".jpg")
with concurrent.futures.ProcessPoolExecutor() as executor:
	for app in zip(resources, executor.map(generateImages, resources)):
		print(str(app) + "Success")
end_time = time.time()
print("Converting malware time cost: " + str(end_time - start_time) + "s")