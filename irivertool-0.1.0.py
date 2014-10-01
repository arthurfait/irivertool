#!/usr/bin/env python

import os
import sys
import struct
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument('-i', '--input', nargs='+', dest='inDir', help='Music directory')
parser.add_argument('-o', '--output', dest='outFile', help='Playlist name')
parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1')

if len(sys.argv) == 1:
	parser.print_help()
	sys.exit(1)

args = parser.parse_args()


fileList = []
offsetList = []

def getFileList(rootdir, filelist, offsetlist):
	for root, subFolders, files in os.walk(rootdir):
		for file in files:
			if file.find('.mp3') != -1:
				filepath = '\\'+os.path.join(root, file).decode('utf-8').replace('/', '\\')
				filelist.append(filepath)
				offsetlist.append(len(filepath) - len(file.decode('utf-8')) + 1)
	return (filelist, offsetlist)


def printFileList(filelist, offsetlist):
	for i in range(len(filelist)):
		print offsetlist[i], filelist[i]
	print 'Total:', len(filelist), 'files.'


for dir in args.inDir:
	(fileList, offsetList) = getFileList(dir, fileList, offsetList)

printFileList(fileList, offsetList)



tracksTotal = len(fileList)
iriverSignature = 'iriver UMS PLA'
playlistHeader = (tracksTotal, iriverSignature)

outFile = args.outFile
filePath = 'Playlists/' + outFile + '.pla'
f = open(filePath, 'wb')
f.write(struct.pack('>I508s', *playlistHeader))

for i in range(len(fileList)):
	data = (offsetList[i], fileList[i].encode('utf-16-be'))
	s = struct.Struct('>h510s')
	chunk = s.pack(*data)
	f.write(chunk)

f.close()

print 'Done:', filePath
