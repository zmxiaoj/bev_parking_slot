import scipy.io
import sys
import os
import json
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
            path2label = path2image.replace('.jpg', '.json').replace('images', 'labels')
            print(path2label)
        
            with open(path2label, 'r') as f:
                labels = json.load(f)
            imagename = labels['metadata']['file_name']
            imagewidth = labels['metadata']['image_width']
            imageheight = labels['metadata']['image_height']
            imagesize = (imagewidth, imageheight)
            # print(imagesize)
            # print(imagename)

            # 遍历ojects
            for object in labels['objects']:
                slot_id = object['id']
                # print(slot_id)
                point_list = object['point_list']
                # 遍历point_list
                for point in point_list:
                    x = int(point[0])
                    y = int(point[1])
                    # print(x, y)
                    # 画点
                    cv2.circle(image, (x, y), 5, (0, 0, 255), -1)   
                        
            # 保存标记后的image
            path2outputimage = os.path.join(path2output, file)
            cv2.imwrite(path2outputimage, image)
            print(path2outputimage)
                


            
                


