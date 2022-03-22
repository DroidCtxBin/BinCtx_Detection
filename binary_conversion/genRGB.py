import sys
import os
import time
import glob
import concurrent.futures
import codecs
# from dexparser import DexParser
import binascii

start_time = time.time()
resourcesDir = "./apps/"
resources = os.listdir(resourcesDir)
RGB_m = os.listdir("./temp/")
def processFiles(appname):
	dex = "./apps/" 	+ str(appname) + "/classes.dex"
	if (str(appname) == ".DS_Store"):
		return
	if (not os.path.isfile(dex)):
		return
	print("Converting: " + str(appname))
	data = list()
	RGBfile = "./temp/" + str(appname) + ".txt"
	if (str(appname) + ".txt") in RGB_m:
		print("Skip: " + RGBfile)
		return
	with open(dex, "rb") as f:
		source = f.read()
	source = codecs.encode(source, "hex")
	# parser = DexParser(dex)
	# temp = parser.parse_dex_header(dex)
	# part1 = int.from_bytes(binascii.a2b_hex(temp), byteorder = 'big', signed = False) * 2
	# print(len(source))
	# print(part1)
	# start, end = parser.parse_strings()
	# temp1 = source[part1:start * 2]
	# temp2 = source[end * 2:]
	# source = source[part1:]
	# source = source[part1:]
	# print(len(source))
	while (len(source) > 0):
		temp = source[:6]
		data.append(temp)
		source = source[6:]
	print("*****--" + str(appname) + " is " + str(len(data)) + "--*****")
	f = open(RGBfile, "w")
	for i in data:
		if (len(i) == 6):
			r_bin = i[:2]
			g_bin = i[2:4]
			b_bin = i[4:]
			R = int(r_bin, 16)
			G = int(g_bin, 16)
			B = int(b_bin, 16)
			RGB = str(R) + "," + str(G) + "," + str(B)
			f.write(str(RGB) + "\t")
			continue
		if (len(i) == 4):
			r_bin = i[:2]
			g_bin = i[2:4]
			b_bin = "0"
			R = int(r_bin, 16)
			G = int(g_bin, 16)
			B = int(b_bin, 16)
			RGB = str(R) + "," + str(G) + "," + str(B)
			f.write(str(RGB) + "\t")
			continue
		if (len(i) == 2):
			r_bin = i[:2]
			g_bin = "0"
			b_bin = "0"
			R = int(r_bin, 16)
			G = int(g_bin, 16)
			B = int(b_bin, 16)
			RGB = str(R) + "," + str(G) + "," + str(B)
			f.write(str(RGB) + "\t")
			continue
	f.close()
	print(str(appname) + " finished analyzing! ")
		
with concurrent.futures.ProcessPoolExecutor() as executor:
	for app in zip(resources, executor.map(processFiles, resources)):
		print(str(app) + "Success")

end_time = time.time()
total_time = end_time - start_time
print("Total time spent: " + str(total_time))
