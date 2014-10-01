#!/usr/bin/env python

import os
import sys
import struct
from argparse import ArgumentParser

VERSION = '0.2.2b'

parser = ArgumentParser()
parser.add_argument('-i', '--input', nargs='+', dest='inDir', help='Music directory')
parser.add_argument('-o', '--output', dest='outFile', help='Playlist name')
parser.add_argument('-l', '--list', dest='fileListPath', help='List with tracks')
parser.add_argument('-v', '--version', action='version', version='irivertool v' + VERSION)

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
#	for i in range(len(filelist)):
#		print offsetlist[i], filelist[i]
	print 'Total:', len(filelist), 'files.'

def createPLA(filelist, offsetlist, outfile):
	tracksTotal = len(filelist)
	iriverSignature = 'iriver UMS PLA'
	playlistHeader = (tracksTotal, iriverSignature)

	filePath = outfile + '.pla'
	f = open(filePath, 'wb')
	f.write(struct.pack('>I508s', *playlistHeader))

	for i in range(len(filelist)):
		data = (int(offsetlist[i]), filelist[i].encode('utf-16-be'))
		chunk = struct.pack('>h510s', *data)
		f.write(chunk)
	f.close()

if not args.fileListPath:
	for dir in args.inDir:
		(fileList, offsetList) = getFileList(dir, fileList, offsetList)
		printFileList(fileList, offsetList)
		createPLA(fileList, offsetList, args.outFile)
else:
	f = open(args.fileListPath, 'r')
	dataList = f.read()
	f.close()
	dataList = dataList.decode('utf-8')
	dataList = dataList.split('\n')
	for line in dataList:
		(offset, file) = line.split(' | ')
		offsetList.append(offset)
		fileList.append(file)

	printFileList(fileList, offsetList)
	createPLA(fileList, offsetList, args.outFile)

print 'Done:', args.outFile+'.pla'
