import os
import xml.etree.ElementTree as ET
app_path = '/Users/shaoyang/Desktop/newapk/apktool_output/'
apps = os.listdir(app_path)
targets = ['action', 'service', 'meta-data', 'uses-library', 'activity', 'receiver', 'provider', 'uses-permission']
def parsexml(root, temp):
	children = root.getchildren()
	if len(children) == 0:
		return
	else:
		for child in children:
			attribs = child.attrib
			if child.tag not in targets:
				parsexml(child, temp)
			else:
				for key in attribs.keys():
					if '}name' in key:
						if attribs[key] not in temp:
							temp.append(attribs[key])
				parsexml(child, temp)
for app in apps:
	if app == '.DS_Store':
		continue
	# if app != 'amuseworks.thermometer.apk':
	# 	continue
	else:
		try:
			tree = ET.parse(app_path + app + '/AndroidManifest.xml')
			temp = []
			parsexml(tree.getroot(), temp)
			fout = open('/Users/shaoyang/Desktop/newapk/appmanis/' + app[:app.index('.apk')] + '.txt', 'w')
			for t in temp:
				fout.write(t + '\n')
			fout.close()
		except Exception as e:
			fout = open('/Users/shaoyang/Desktop/newapk/appmanis/' + app[:app.index('.apk')] + '.txt', 'w')
			fout.close()
