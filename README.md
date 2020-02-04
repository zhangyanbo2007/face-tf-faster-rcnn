# 项目简介
本项目的原始工程来源于[here](https://github.com/endernewton/tf-faster-rcnn)，本人在此基础上做了人脸检测器项目. 
### 代码工程安装
1. 克隆本仓库
  ```Shell
  git clone https://github.com/zhangyanbo2007/face-tf-faster-rcnn.git
  ```
2. 查看GPU版本是否匹配(模型较大，训练模型推荐使用GPU)
  ```Shell
  cd tf-faster-rcnn/lib
  # Change the GPU architecture (-arch) if necessary
  vim setup.py
  ```
  | GPU model  | Architecture |
  | ------------- | ------------- |
  | TitanX (Maxwell/Pascal) | sm_52 |
  | GTX 960M | sm_50 |
  | GTX 1080 (Ti) | sm_61 |
  | Grid K520 (AWS g2.2xlarge) | sm_30 |
  | Tesla K80 (AWS p2.xlarge) | sm_37 |
3. 安装[Python COCO API](https://github.com/pdollar/coco). (本人已配好，可忽略此步骤)
  ```Shell
  cd data
  git clone https://github.com/pdollar/coco.git
  cd coco/PythonAPI
  make
  cd ../../..
  ```
4. pip安装库（根据自身情况选择CPU版本或者GPU版本）

  ```Shell
  cd docker
  # cpu版本
  pip install -r requirements-cpu.txt
  # gpu版本
  pip install -r requirements-gpu.txt
  ```

5. 加载人脸数据集
  - 点击百度网盘地址：[人脸数据集](https://github.com/pdollar/coco)，下载数据文件. 
  - 解压该数据集，并将其中的VOCdevkit2007文件夹覆盖到data/VOCdevkit2007的位置. 

6. 加载特征抽取模型
  - 点击百度网盘地址：[特征抽取模型](https://pan.baidu.com/s/1CF4MyINrS20J4OfeODhDQw)，下载特征抽取模型文件. 
  - 将下载后的imagenet_weights文件夹覆盖到data/imagenet_weights的位置. 

### 人脸检测器测试
1. 加载训练模型
  - 点击百度网盘地址：[人脸检测器训练模型](https://pan.baidu.com/s/13iEEb3qoO18fanLO7iK-jA)，下载模型文件. 
  - 将下载后的voc_2007_trainval文件夹覆盖到output/vgg16/voc_2007_trainval的位置. 

2. 人脸检测器模型测试
  ```Shell
  cd tools
  # cpu版本
  cp cpu-configfile/config.py ../lib/model/config.py
  cp cpu-configfile/nms_wrapper.py ../lib/model/nms_wrapper.py
  cp cpu-configfile/setup.py ../lib/setup.py
  python test_net.py --imdb voc_2007_test --model ../output/vgg16/voc_2007_trainval/default/vgg16_faster_rcnn_iter_165000.ckpt --cfg ../experiments/cfgs/vgg16.yml --net vgg16 --set ANCHOR_SCALES '[8,16,32]' ANCHOR_RATIOS '[0.5,1,2]'
  # gpu版本
  cp gpu-configfile/config.py ../lib/model/config.py
  cp gpu-configfile/nms_wrapper.py ../lib/model/nms_wrapper.py
  cp gpu-configfile/setup.py ../lib/setup.py
  ldconfig /usr/local/cuda/lib64
  python test_net.py --imdb voc_2007_test --model ../output/vgg16/voc_2007_trainval/default/vgg16_faster_rcnn_iter_165000.ckpt --cfg ../experiments/cfgs/vgg16.yml --net vgg16 --set ANCHOR_SCALES '[8,16,32]' ANCHOR_RATIOS '[0.5,1,2]'
  ```

### 训练你自己的人脸检测器模型
1. 人脸检测器模型训练
  ```Shell
  cd tools
  # cpu版本
  cp cpu-configfile/config.py ../lib/model/config.py
  cp cpu-configfile/nms_wrapper.py ../lib/model/nms_wrapper.py
  cp cpu-configfile/setup.py ../lib/setup.py
  ldconfig /usr/local/cuda/lib64
  python trainval_net.py --weight ../data/imagenet_weights/vgg16.ckpt --imdb voc_2007_trainval --imdbval voc_2007_test --iters 500000 --cfg ../experiments/cfgs/vgg16.yml --net vgg16 --set ANCHOR_SCALES '[8,16,32]' ANCHOR_RATIOS '[0.5,1,2]' TRAIN.STEPSIZE '[50000]'
  # gpu版本
  cp gpu-configfile/config.py ../lib/model/config.py
  cp gpu-configfile/nms_wrapper.py ../lib/model/nms_wrapper.py
  cp gpu-configfile/setup.py ../lib/setup.py
  python trainval_net.py --weight ../data/imagenet_weights/vgg16.ckpt --imdb voc_2007_trainval --imdbval voc_2007_test --iters 500000 --cfg ../experiments/cfgs/vgg16.yml --net vgg16 --set ANCHOR_SCALES '[8,16,32]' ANCHOR_RATIOS '[0.5,1,2]' TRAIN.STEPSIZE '[50000]'

  ```
2. Tensorboard可视化
  ```Shell
  tensorboard --logdir=tensorboard/vgg16/voc_2007_trainval/
  ```

### 制作docker镜像（注意数据集路径可能存在问题，仅供参考，可适当修改）
1. docker-cpu镜像制作
  ```Shell
  sudo docker build -t zhangyanbo2007/face-detector-cpu:dev1 -f configfile/Dockerfile-gpu .
  ```
2. docker-gpu镜像制作
  ```Shell
  sudo docker build -t zhangyanbo2007/face-detector-gpu:dev1 -f configfile/Dockerfile-gpu .
  ```

### 人脸检测器-CPU DOCKER镜像工程测试
1. 创建docker镜像
  - 方法一：拉取官方镜像
  ```Shell
    docker pull zhangyanbo2007/face-detector-cpu:dev1
  ```
  - 方法二：直接解压镜像
    - 点击百度网盘地址：[docker-cpu](https://pan.baidu.com/s/12WLncaLkLQOOKKRtNhDSpg)，下载该镜像文件. 
    - 执行合并分卷命令并解压镜像文件
  ```Shell
    cd /yourdir
    cat ./images/face-detector-cpu.tar0* > ./images/face-detector-cpu.tar
    sudo docker load –i ./images/face-detector-cpu.tar
  ```
2. 执行人脸检测器测试命令
  ```Shell
  # 步骤一：查看当前路径
  pwd #/home/zyb/myProject/face_recognition
  # 步骤二：执行测试命令
  /home/zyb/myProject/face_recognition/test_image:/home/zyb/myProject/face_recognition/tf-faster-rcnn/tools/test_image –it zhangyanbo2007/face-detector-cpu:dev1 sh -c "/bin/bash test.sh"
  ```

### 人脸检测器-GPU DOCKER镜像工程测试
1. 创建docker镜像
  - 方法一：拉取官方镜像
  ```Shell
    docker pull zhangyanbo2007/face-detector-gpu:dev1
  ```
  - 方法二：直接解压镜像
    - 点击百度网盘地址：[docker-gpu](https://pan.baidu.com/s/174dNxTjaAtGopp-rbP0cJQ)，下载该镜像文件. 
    - 执行合并分卷命令并解压镜像文件
  ```Shell
    cd /yourdir
    cat ./images/face-detector-gpu.tar0* > ./images/face-detector-gpu.tar
    sudo docker load –i ./images/face-detector-gpu.tar
  ```
2. 执行人脸检测器测试命令
  ```Shell
  # 步骤一：查看当前路径
  pwd #/home/zyb/myProject/face_recognition
  # 步骤二：执行测试命令
  /home/zyb/myProject/face_recognition/test_image:/home/zyb/myProject/face_recognition/tf-faster-rcnn/tools/test_image –it zhangyanbo2007/face-detector-gpu:dev1 sh -c "/bin/bash test.sh"
  ```