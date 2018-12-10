import os

files = os.listdir(".")

print(files)


'''
from os import rename, listdir

files = listdir('.')

for name in files:
	if name.startswith('jangchangwon'):
		newname = name.replace('jangchangwon','jcw')
		rename(name,newname)
		print name + ' -> ' + newname
'''