import cv2
import os


# 指定图片所在的文件夹路径
folder_path = '../runs/detect/exp7/crops/dev_label'

# 初始化微信二维码检测器
detect_obj = cv2.wechat_qrcode_WeChatQRCode('detect.prototxt', 'detect.caffemodel', 'sr.prototxt', 'sr.caffemodel')

# 获取文件夹中所有的图片文件
image_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.jpg')]


# 遍历所有图片文件
with open('qr_results.txt', 'w') as file:
    for image_file in image_files:
        # 构建完整的图片路径
        img_path = os.path.join(folder_path, image_file)
        
        # 读取图片
        img = cv2.imread(img_path)
        
        if img is not None:
            # 检测和解码二维码
            res, points = detect_obj.detectAndDecode(img)
            
            # 输出结果
            if res:
                file.write(f'{image_file}: {res}\n')
                print(f'File: {image_file}')
                print('Result:', res)
                print('Points:', points)
                
                # 可选：在图片上绘制二维码边界
                for pos in points:
                    color = (0, 0, 255)
                    thick = 3
                    for p in [(0, 1), (1, 2), (2, 3), (3, 0)]:
                        start = int(pos[p[0]][0]), int(pos[p[0]][1])
                        end = int(pos[p[1]][0]), int(pos[p[1]][1])
                        cv2.line(img, start, end, color, thick)
                
                # 可选：显示和保存标注后的图片
                cv2.imshow('img', img)
                cv2.imwrite(os.path.join('output', image_file), img)
                cv2.waitKey(1000)  # 等待1秒后自动关闭窗口
                cv2.destroyAllWindows()
            else:
                file.write(f'{image_file}: {res}\n')
                print(f'No QR code found in {image_file}')
        else:
            print(f'Failed to load image: {image_file}')
