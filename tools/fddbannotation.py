import os,cv2
from math import *
import numpy as np
from xml.dom.minidom import Document
rootdir="../data/VOCdevkit2007/FDDB-folds"
origimagedir=rootdir+"/originalPics"
annotationdir=rootdir+"/FDDB-folds"
imagesdir=rootdir+"/images"
labelsdir=rootdir+"/labels"
Annotationsdir=rootdir+"/Annotations"
convert2rects=True
bsavexmlanno=True
bsavetxtanno=True
# datasetprefix="/home/yanhe/data/fddb/images/"
datasetprefix=""

def show_annotations():
    if not os.path.exists(Annotationsdir):
        os.mkdir(Annotationsdir)
    if not os.path.exists(labelsdir):
        os.mkdir(labelsdir)
    for i in range(10):
        annotationfilepath=annotationdir+"/FDDB-fold-%0*d-ellipseList.txt"%(2,i+1)
        annotationfile=open(annotationfilepath)
        while(True):
            filename=annotationfile.readline()[:-1]+".jpg"
            if not filename:
                break
            line=annotationfile.readline()
            if not line:
                break
            print(filename)
            facenum=(int)(line)
            img=cv2.imread(origimagedir+"/"+filename)  # 读原始文件
            filename=filename.replace('/','_')
            cv2.imwrite(imagesdir+"/"+filename,img)  # 写入到images文件夹
            w = img.shape[1]
            h = img.shape[0]
            if bsavetxtanno:  # 保存txt
                labelpath=labelsdir+"/"+filename.replace('/','_')[:-3]+"txt"
                labelfile=open(labelpath,'w')  # 写标签
            if bsavexmlanno:  # 保存xml
                xmlpath=Annotationsdir+"/"+filename.replace('/','_')[:-3]+"txt"
                xmlpath=xmlpath[:-3]+"xml"
                doc = Document()
                annotation = doc.createElement('annotation')
                doc.appendChild(annotation)
                folder = doc.createElement('folder')
                folder_name = doc.createTextNode('fddb')
                folder.appendChild(folder_name)
                annotation.appendChild(folder)
                filenamenode = doc.createElement('filename')
                filename_name = doc.createTextNode(filename)
                filenamenode.appendChild(filename_name)
                annotation.appendChild(filenamenode)
                source = doc.createElement('source')
                annotation.appendChild(source)
                database = doc.createElement('database')
                database.appendChild(doc.createTextNode('fddb Database'))
                source.appendChild(database)
                annotation_s = doc.createElement('annotation')
                annotation_s.appendChild(doc.createTextNode('PASCAL VOC2007'))
                source.appendChild(annotation_s)
                image = doc.createElement('image')
                image.appendChild(doc.createTextNode('flickr'))
                source.appendChild(image)
                flickrid = doc.createElement('flickrid')
                flickrid.appendChild(doc.createTextNode('-1'))
                source.appendChild(flickrid)
                owner = doc.createElement('owner')
                annotation.appendChild(owner)
                flickrid_o = doc.createElement('flickrid')
                flickrid_o.appendChild(doc.createTextNode('yanyu'))
                owner.appendChild(flickrid_o)
                name_o = doc.createElement('name')
                name_o.appendChild(doc.createTextNode('yanyu'))
                owner.appendChild(name_o)
                size = doc.createElement('size')
                annotation.appendChild(size)
                width = doc.createElement('width')
                width.appendChild(doc.createTextNode(str(img.shape[1])))
                height = doc.createElement('height')
                height.appendChild(doc.createTextNode(str(img.shape[0])))
                depth = doc.createElement('depth')
                depth.appendChild(doc.createTextNode(str(img.shape[2])))
                size.appendChild(width)
                size.appendChild(height)
                size.appendChild(depth)
                segmented = doc.createElement('segmented')
                segmented.appendChild(doc.createTextNode('0'))
                annotation.appendChild(segmented)
            for j in range(facenum):
                line=annotationfile.readline().strip().split()
                major_axis_radius=(float)(line[0])
                minor_axis_radius=(float)(line[1])
                angle=(float)(line[2])
                center_x=(float)(line[3])
                center_y=(float)(line[4])
                score=(float)(line[5])
                angle = angle / 3.1415926*180
                cv2.ellipse(img, ((int)(center_x), (int)(center_y)), ((int)(major_axis_radius), (int)(minor_axis_radius)), angle, 0., 360.,(255, 0, 0)) 
                if convert2rects:
                    mask=np.zeros((img.shape[0],img.shape[1]),dtype=np.uint8)
                    cv2.ellipse(mask, ((int)(center_x), (int)(center_y)), ((int)(major_axis_radius), (int)(minor_axis_radius)), angle, 0., 360.,(255, 255, 255))
                    #cv2.imshow("mask",mask) 
                    image, contours, hierarchy=cv2.findContours(mask,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)

                    # img = cv2.drawContours(img, [contours[0]], -1, (0, 255, 0), 10)  # 标记处编号为0的轮廓，此处img为三通道才能显示轮廓
                    # # cv2.imshow('drawimg',img)
                    # cv2.imwrite("contors_0.jpg", img)
                    #
                    # img = cv2.drawContours(img, [contours[1]], -1, (0, 255, 0), 10)  # 标记处编号为0的轮廓，此处img为三通道才能显示轮廓
                    # # cv2.imshow('drawimg',img)
                    # cv2.imwrite("contors_1.jpg", img)
                    # 不知道这里为什么会重复

                    last_x_min = 0
                    last_y_min = 0
                    last_x_max = 0
                    last_y_max = 0
                    last_xcenter = 0
                    last_ycenter = 0
                    for k in range(len(contours)):
                        r=cv2.boundingRect(contours[k])  # 椭圆转矩形
                        x_min=r[0]
                        y_min=r[1]
                        x_max=r[0]+r[2]
                        y_max=r[1]+r[3]
                        xcenter=r[0]+r[2]/2
                        ycenter=r[1]+r[3]/2

                        # 过滤掉重复的部分
                        if x_min == last_x_min and y_min == last_y_min and \
                                last_x_max == x_max and last_y_max == y_max and \
                                last_xcenter == xcenter and last_ycenter == ycenter:
                            continue

                        last_x_min = x_min
                        last_y_min = y_min
                        last_x_max = x_max
                        last_y_max = y_max
                        last_xcenter = xcenter
                        last_ycenter = ycenter

                        if bsavetxtanno:
                            labelline="0"+"\t"+str(xcenter*1.0/w) + '\t' + str(ycenter*1.0/h) + '\t' + str(r[2]*1.0/w) + '\t' + str(r[3]*1.0/h)	+ '\n'
                            labelfile.write(labelline)
                        if bsavexmlanno:
                            object = doc.createElement('object')
                            annotation.appendChild(object)
                            object_name = doc.createElement('name')
                            object_name.appendChild(doc.createTextNode('face'))
                            object.appendChild(object_name)
                            pose = doc.createElement('pose')
                            pose.appendChild(doc.createTextNode('Unspecified'))
                            object.appendChild(pose)
                            truncated = doc.createElement('truncated')
                            truncated.appendChild(doc.createTextNode('1'))
                            object.appendChild(truncated)
                            difficult = doc.createElement('difficult')
                            difficult.appendChild(doc.createTextNode('0'))
                            object.appendChild(difficult)
                            bndbox = doc.createElement('bndbox')
                            object.appendChild(bndbox)
                            xmin = doc.createElement('xmin')
                            xmin.appendChild(doc.createTextNode(str(x_min)))
                            bndbox.appendChild(xmin)
                            ymin = doc.createElement('ymin')
                            ymin.appendChild(doc.createTextNode(str(y_min)))
                            bndbox.appendChild(ymin)
                            xmax = doc.createElement('xmax')
                            xmax.appendChild(doc.createTextNode(str(x_max)))
                            bndbox.appendChild(xmax)
                            ymax = doc.createElement('ymax')
                            ymax.appendChild(doc.createTextNode(str(y_max)))
                            bndbox.appendChild(ymax)
                        if x_min < 0 or y_min < 0:
                            print("sss")
                        cv2.rectangle(img,(int(x_min),int(y_min)),(int(x_max),int(y_max)),(0,0,255))
            if bsavetxtanno:
                labelfile.close()
            if bsavexmlanno:
                f=open(xmlpath,"w")
                f.write(doc.toprettyxml(indent = ''))
                f.close() 
            # cv2.imshow("img",img)
            cv2.waitKey(1)

def generatetxt(trainratio=0,valratio=0,testratio=1):
    files=os.listdir(labelsdir)
    ftrain=open(rootdir+"/"+"train.txt","w")
    fval=open(rootdir+"/"+"val.txt","w")
    ftrainval=open(rootdir+"/"+"trainval.txt","w")
    ftest=open(rootdir+"/"+"test.txt","w")
    index=0 
    for i in range(len(files)):
        filename=files[i]
        filename=datasetprefix+filename[:-3]+"jpg"+"\n"
        if i<trainratio*len(files):
            ftrain.write(filename)
            ftrainval.write(filename)
        elif i<(trainratio+valratio)*len(files):
            fval.write(filename)
            ftrainval.write(filename)
        elif i<(trainratio+valratio+testratio)*len(files):
            ftest.write(filename)
    ftrain.close()
    fval.close()
    ftrainval.close()
    ftest.close()

def generatevocsets(trainratio=0,valratio=0,testratio=1):
    if not os.path.exists(rootdir+"/ImageSets"):
        os.mkdir(rootdir+"/ImageSets")
    if not os.path.exists(rootdir+"/ImageSets/Main"):
        os.mkdir(rootdir+"/ImageSets/Main")
    ftrain=open(rootdir+"/ImageSets/Main/train.txt",'w')
    fval=open(rootdir+"/ImageSets/Main/val.txt",'w')
    ftrainval=open(rootdir+"/ImageSets/Main/trainval.txt",'w')
    ftest=open(rootdir+"/ImageSets/Main/test.txt",'w')
    files=os.listdir(labelsdir)
    for i in range(len(files)):
        imgfilename=files[i][:-4]
        ftrainval.write(imgfilename+"\n")
        if i<int(len(files)*trainratio):
            ftrain.write(imgfilename+"\n")
        elif i<int(len(files)*(trainratio+valratio)):
            fval.write(imgfilename+"\n")
        else:
            ftest.write(imgfilename+"\n")
    ftrain.close()
    fval.close()
    ftrainval.close()
    ftest.close()


if __name__=="__main__":
    show_annotations()
    generatevocsets()
    generatetxt()
