import scipy.io
import sys
import os
import cv2

# 实现读入脚本参数作为pathimage
if (len(sys.argv) > 1):
    path2database = sys.argv[1]
# 在ouput文件夹下创建database对应的文件夹保存结果
# 检测是相对路径还是绝对路径，如果是绝对路径只保留bev_parking_slot后的部分
if os.path.isabs(path2database):
    # path2databse从某一位置后进行切片
    path2output = os.path.join('output', path2database.split('bev_parking_slot/')[-1])
    print(path2output)

if not os.path.exists(path2output):
    os.makedirs(path2output)

# 遍历database文件夹
for root, dirs, files in os.walk(path2database):
    for file in files:
        if file.endswith('.jpg'):
            path2image = os.path.join(root, file)
            print(path2image)
            # 读入图片
            image = cv2.imread(path2image)
            # 读入image对应的label，label的文件名和image的文件名一样，只是后缀为.mat
            path2label = path2image.replace('.jpg', '.mat').replace('images', 'annotations')
            path2labelpng = path2image.replace('.jpg', '.png').replace('images', 'labels')
            print(path2label)
            print(path2labelpng)
            # 读入label，判断路径是否存在
            if os.path.exists(path2label):
                label = scipy.io.loadmat(path2label)
                # 读入label中的marks字段
                marks = label['marks']
                # 遍历marks对image进行标记
                for mark in marks:
                    # 读入mark中的x和y
                    x = int(mark[0])
                    y = int(mark[1])
                    # 在image上画圆
                    cv2.circle(image, (x, y), 5, (0, 0, 255), -1)
            else:
                # 将png格式的label进行读入
                labelpng = cv2.imread(path2labelpng, cv2.IMREAD_GRAYSCALE)
                # 使用labelpng进行标注
                for i in range(labelpng.shape[0]):
                    for j in range(labelpng.shape[1]):
                        if labelpng[i, j] == 1:
                            cv2.circle(image, (j, i), 5, (0, 0, 255), -1)

            # 保存标记后的image
            path2outputimage = os.path.join(path2output, file)
            cv2.imwrite(path2outputimage, image)
            print(path2outputimage)
                


            
                


