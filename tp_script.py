# -*- coding: utf-8 -*-
#/usr/bin/python

#python -m py_compile file.py

import ConfigParser
import string, os, sys
import argparse
import shutil

reload(sys)
sys.setdefaultencoding('utf-8')

cf = ConfigParser.ConfigParser()

cf.read("config.conf")
'''
#return all section
secs = cf.sections()
print 'sections:', secs

opts = cf.options("opt_format")
print 'options:', opts

kvs = cf.items("opt_format")
print 'path:', kvs

#read by type
db_host = cf.get("path", "packer_path")
db_port = cf.get("path", "orgImg_path")
db_user = cf.get("path", "output_path")
db_pass = cf.get("path", "project_path")

print "db_host:", db_host
print "db_port:", db_port
print "db_user:", db_user
print "db_pass:", db_pass

#modify one value and write to file
cf.set("db", "db_pass", "xgmtest")
cf.write(open("config.conf", "w"))
'''
###########################################################################

#packer_path = cf.get("path", "packer_path")
#orgImg_path = cf.get("path", "orgImg_path")
global packer_path

optList = cf.get("opt_format", "opt")
optList = optList.split(',')
t_format = cf.get("format", "texture_format")
t_sheet = cf.get("format", "texture_sheet")
t_f = cf.get("format", "format")
#optList = ["RGBA8888","RGBA4444","RGBA5551","RGB565"]

def is_ascii_char(in_str):
	return all(ord(c) < 128 for c in in_str)

def in_filter_files(item):
	if item.endswith('.gz') or item.startswith('.'):
		return True

	if not is_ascii_char(item):
		return True

	return False

def copy_files(src, dst):
	for item in os.listdir(src):
		path = os.path.join(src, item)
		# Android can not package the file that ends with ".gz";
		# the file that contain chinese characters or in the specific file lists.
		if not in_filter_files(item) and os.path.isfile(path):
			shutil.copy(path, dst)
		if os.path.isdir(path):
			new_dst = os.path.join(dst, item)
			os.mkdir(new_dst)
			copy_files(path, new_dst)

def pack_textrue(makeDir, outPath, pixel, fname, isAnySize, isMultipack):
	global packer_path
	filePath = os.path.join(outPath, fname)

	
	param = " %s" %(makeDir)
	#param += " --smart-update"
	param += " --format %s" %(t_f)#('cocos2d')
	
	param += " --maxrects-heuristics Best"
	param += " --pack-mode Best"
	param += " --enable-rotation"

	#param += " --basic-sort-by Name"
	#param += " --basic-order Ascending"

	#layout
	#param += " --max-size 1024"
	if isAnySize=="False":
		param += " --max-width 1024"
		param += " --max-height 1024"
		if isMultipack=="True":
			#更高的版本才可用
			param += " --multipack"

	param += " --allow-free-size"
	param += " --size-constraints AnySize" #POT AnySize
	
	#param += " --force-squared"

	param += " --opt %s" %(pixel)

	param += " --scale 1"
	param += " --scale-mode Smooth"

	param += " --trim-mode Trim" #剪裁图片,即移除图片周围的透明像素,保留原始尺寸,默认开启 示例:--trim no-trim
	
	
	param += " --texture-format %s" %(t_format)#('pvr2ccz')
	
	param += " --shape-padding 2"
	param += " --border-padding 2"
	#param += " --trim-margin 1"
	param += " --extrude 1"
	
	if pixel=="RGBA4444" or pixel=="RGBA5551":
		#param += " --dither-type FloydSteinbergAlpha"
		#param += " --alpha-handling KeepTransparentPixels"
		param += " --dither-fs-alpha"
	elif pixel=="RGBA8888":
		#param += " --alpha-handling KeepTransparentPixels"
		param += " --dither-fs-alpha"
	elif pixel=="RGB565":
		#param += " --dither-type FloydSteinberg"
		param += " --dither-fs"
	if isMultipack=="True":
		param += " --data %s_{n}.plist" %(filePath)
		param += " --sheet %s_{n}.%s" %(filePath, t_sheet)#'pvr.ccz')
	else:
		param += " --data %s.plist" %(filePath)
		param += " --sheet %s.%s" %(filePath, t_sheet)#'pvr.ccz')

	command = '"%s" %s' % (packer_path, param)

	if os.system(command) != 0:
		raise Exception("packer [ " + makeDir + " ] fails!")
'''
	try:
		os.system(command)
	except Exception, e:
		print 'str(Exception):\t', str(Exception)
		print 'str(e):\t\t', str(e)
		print 'repr(e):\t', repr(e)
		print 'e.message:\t', e.message
		print("packer [ " + makeDir + " ] fails!")

		#更高的版本才可用
		param += " --multipack"
		command = '"%s" %s' % (packer_path, param)
		if os.system(command) != 0:
			raise Exception("packer [ " + makeDir + " ] fails!")
'''

#################################
def main():
	
	'''
	helpConf = cf.get("help", "help")
	if helpConf=="true":
		command = '"%s"' % (packer_path)
		os.system(command)
		return
	'''
	'''
	global packer_path = sys.argv[1]
	running_path = sys.argv[2]
	isDirectoryStructure = sys.argv[2]
	'''
	global packer_path
	parser = argparse.ArgumentParser(description='manual to this script')
	parser.add_argument('-tp', type=str, default="")
	parser.add_argument('-op', type=str, default="")
	parser.add_argument('-replacePath', type=str, default="")
	parser.add_argument('-isDir', type=str, default="False")
	parser.add_argument('-isAnySize', type=str, default="False")
	parser.add_argument('-isClear', type=str, default="False")
	parser.add_argument('-isMultipack', type=str, default="False")
	args = parser.parse_args()
	
	packer_path = args.tp
	running_path = args.op
	replacePath = args.replacePath
	isDirectoryStructure = args.isDir
	isAnySize = args.isAnySize
	isClear = args.isClear
	isMultipack = args.isMultipack

	curPath = os.path.split(os.path.realpath(__file__))[0]
	output_path = os.path.join(curPath, "ExportDir")

	if os.path.exists(output_path)==False:
		os.mkdir(output_path)
	
	if isClear=="True":
		#删除目录内容
		shutil.rmtree(output_path, True)

	if running_path=="":
		command = '"%s"' % (packer_path)
		os.system(command)
		return

	output_path = os.path.join(output_path, running_path.replace(replacePath, ''))
	
	print "packer "+packer_path
	print "running_path = "+running_path
	print "output_path = "+output_path	

	pixel = "RGBA8888"
	
	#opt = RGBA8888,RGBA4444,RGBA5551,RGB565
	for parent,dirnames,filenames in os.walk(running_path):
		if filenames:
			p, fname = os.path.split(parent);
			#print "p = "+p
			print("fname = "+fname)
			if isDirectoryStructure=="True":
				#print("isDirectoryStructure==True:")

				outp = p.replace(running_path, output_path)
				print("outp = "+outp)
				if os.path.exists(outp)==False:
					os.makedirs(outp)
			else:
				#print("isDirectoryStructure==False:")
				outp = output_path
			#print "parent = "+parent
			#print("outp = "+outp)
			if parent.find("0565")!=-1:
				pixel = "RGB565"
			elif parent.find("4444")!=-1:
				pixel = "RGBA4444"
			elif parent.find("5551")!=-1:
				pixel = "RGBA5551"
			else:
				pixel = "RGBA8888"
			#print("pixel = "+pixel )
			pack_textrue(parent, outp, pixel, fname, isAnySize, isMultipack)

	'''
	if isTextrueFile == True:
		if os.path.exists(project_path)==False:
			os.mkdir(project_path)
		if os.path.exists(project_path)==True:
			copy_files(output_path, project_path)
	else:
		print "no file find to pack textrue"
	'''

if __name__=="__main__":
	main()


