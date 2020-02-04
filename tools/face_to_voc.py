"""
Created on 20/1/30

@author: 章彦博
"""
from skimage import io
import shutil
import random
import os
import string

headstr = """\
<annotation>
    <folder>VOC2007</folder>
    <filename>%06d.jpg</filename>
    <source>
        <database>My Database</database>
        <annotation>PASCAL VOC2007</annotation>
        <image>flickr</image>
        <flickrid>NULL</flickrid>
    </source>
    <owner>
        <flickrid>NULL</flickrid>
        <name>company</name>
    </owner>
    <size>
        <width>%d</width>
        <height>%d</height>
        <depth>%d</depth>
    </size>
    <segmented>0</segmented>
"""
objstr = """\
    <object>
        <name>%s</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>%d</xmin>
            <ymin>%d</ymin>
            <xmax>%d</xmax>
            <ymax>%d</ymax>
        </bndbox>
    </object>
"""

tailstr = '''\
</annotation>
'''

def fddb_path(filename):
    return os.path.join('../data/VOCdevkit2007/FDDB-folds', filename)

def all_path(filename):
    return os.path.join('../data/VOCdevkit2007/Wider_face', filename)

def write_all_path(filename):
    return os.path.join('../data/VOCdevkit2007/VOC2007', filename)

def writexml(idx, head, bbxes, tail):
    filename = write_all_path("Annotations/%06d.xml" % (idx))
    f = open(filename, "w")
    f.write(head)
    for bbx in bbxes:
        f.write(objstr % ('face', bbx[0], bbx[1], bbx[0] + bbx[2], bbx[1] + bbx[3]))
    f.write(tail)
    f.close()


def clear_dir():
    if shutil.os.path.exists(write_all_path('Annotations')):
        shutil.rmtree(write_all_path('Annotations'))
    if shutil.os.path.exists(write_all_path('ImageSets')):
        shutil.rmtree(write_all_path('ImageSets'))
    if shutil.os.path.exists(write_all_path('JPEGImages')):
        shutil.rmtree(write_all_path('JPEGImages'))

    shutil.os.mkdir(write_all_path('Annotations'))
    shutil.os.makedirs(write_all_path('ImageSets/Main'))
    shutil.os.mkdir(write_all_path('JPEGImages'))


def excute_datasets(idx, datatype):
    f = open(write_all_path('ImageSets/Main/' + datatype + '.txt'), 'a')
    f_bbx = open(all_path('wider_face_split/wider_face_' + datatype + '_bbx_gt.txt'), 'r')

    while True:
        filename = f_bbx.readline().strip('\n')
        if not filename:
            break
        try:
            im = io.imread(all_path('WIDER_' + datatype + '/images/'+filename))
        except IOError:
            print('没有检测到人脸', filename)  # 遇到这种情况并不以为着它没有被保存，而只是程序跳过处理
            print("其对应的文件编号是：%06d" % (idx-1))
            continue
        head = headstr % (idx, im.shape[1], im.shape[0], im.shape[2])
        nums = f_bbx.readline().strip('\n')
        bbxes = []
        for ind in range(int(nums)):
            bbx_info = f_bbx.readline().strip(' \n').split(' ')
            bbx = [int(bbx_info[i]) for i in range(len(bbx_info))]
            #x1, y1, w, h, blur, expression, illumination, invalid, occlusion, pose
            if bbx[7]==0:
                bbxes.append(bbx)
        writexml(idx, head, bbxes, tailstr)
        shutil.copyfile(all_path('WIDER_' + datatype + '/images/'+filename), write_all_path('JPEGImages/%06d.jpg' % (idx)))
        f.write('%06d\n' % (idx))
        idx +=1
    f.close()
    f_bbx.close()
    return idx


# 打乱样本
def shuffle_file(filename):
    f = open(filename, 'r+')
    lines = f.readlines()
    random.shuffle(lines)
    f.seek(0)
    f.truncate()
    f.writelines(lines)
    f.close()


if __name__ == '__main__':
    # clear_dir()
    #
    # idx = 1
    # idx = excute_datasets(idx, 'train')
    # idx = excute_datasets(idx, 'val')
    #
    # # 写训练集+验证集
    # f_train = open(write_all_path('ImageSets/Main/' + 'train' + '.txt'), 'r')
    # f_val = open(write_all_path('ImageSets/Main/' + 'val' + '.txt'), 'r')
    # f_trainval = open(write_all_path('ImageSets/Main/' + 'trainval' + '.txt'), 'w')
    #
    # f_trainval.writelines(f_train.readlines())
    # f_trainval.writelines(f_val.readlines())
    # f_train.close()
    # f_val.close()
    # f_trainval.close()

    # 以下是写测试集
    # 1 COPY JPEGImages文件
    for file in os.listdir(fddb_path('images')):
        shutil.copy(fddb_path('images/' + file),
                    write_all_path('JPEGImages/' + file))
    # 2 COPY Annotations
    for file in os.listdir(fddb_path('Annotations')):
        shutil.copy(fddb_path('Annotations/' + file),
                    write_all_path('Annotations/' + file))
    # 3 COPY test.txt
    shutil.copy(fddb_path('ImageSets/Main/' + 'test' + '.txt'),
                write_all_path('ImageSets/Main/' + 'test' + '.txt'))


