# -*- coding: utf-8 -*-
#/usr/bin/python
import ConfigParser
import string, os, sys
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

packer_path = cf.get("path", "packer_path")
orgImg_path = cf.get("path", "orgImg_path")
output_path = cf.get("path", "output_path")
project_path = cf.get("path", "project_path")

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

def pack_textrue(makeFileName):
    #先尝试创建输出目录
    if os.path.exists(output_path)==False:
        os.mkdir(output_path)
    source = os.path.join(orgImg_path, makeFileName)

    content = makeFileName.split('#')
    optIdx = 0
    opt = optList[optIdx]
    if len(content)>1:
        for i in range(0, len(optList)):
        #for v in optList:
            print optList[i]
            if optList[i]==content[1]:
                opt = optList[i]
                optIdx = i
                break

    filePath = os.path.join(output_path, content[0])
    print "packer "+packer_path
    print "source "+source
    print "filePath "+filePath
    param = "--smart-update"
    param += " %s" %(source)
    
    param += " --format %s" %(t_f)#('cocos2d')
    param += " --data %s#%d#{n}.plist" %(filePath, optIdx)
    param += " --sheet %s#%d#{n}.%s" %(filePath, optIdx, t_sheet)#'pvr.ccz')
    param += " --maxrects-heuristics best"
    param += " --enable-rotation"
    #param += " --scale 1"
    param += " --shape-padding 2"
    '''
     None              Keep transparent pixels
     Trim              Remove transparent pixels, use original size.
     Crop              Remove transparent pixels, use trimmed size, flush position.
     CropKeepPos       Remove transparent pixels, use trimmed size, keep position.
    '''
    #layout
    param += " --size-constraints AnySize" #POT AnySize
    #param += " --max-size 1024"
    param += " --max-width 1024"
    param += " --max-height 1024"
    
    param += " --opt %s" %(opt)
    #更高的版本才可用
    param += " --multipack"
    param += " --texture-format %s" %(t_format)#('pvr2ccz')
    param += " --trim-mode Trim"

    if opt != optList[0]:
        if opt == optList[3]:
            param += " --dither-fs"
        else:
            param += " --dither-fs-alpha"
    
    command = '"%s" %s' % (packer_path, param)
    
    if os.system(command) != 0:
        raise Exception("packer [ " + makeFileName + " ] fails!")

#################################
def main():
    helpConf = cf.get("help", "help")
    if helpConf=="true":
        command = '"%s"' % (packer_path)
        os.system(command)
        return
    
    #curPath = os.path.split(os.path.realpath(__file__))[0]
    shutil.rmtree(output_path, True)

    isTextrueFile = False
    parent_path = None
    for parent,dirnames,filenames in os.walk(orgImg_path):
        if parent_path==None:
            parent_path = parent

        if parent_path==parent:
            for dirname in dirnames:
                pack_textrue(dirname)
                isTextrueFile = True

    if isTextrueFile == True:
        if os.path.exists(project_path)==False:
            os.mkdir(project_path)
        if os.path.exists(project_path)==True:
            copy_files(output_path, project_path)
    else:
        print "no file find to pack textrue"

if __name__=="__main__":

    main()

