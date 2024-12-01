#这段代码用于ocr识别一个文件夹中的图片里的文字并且生成一个Txt文件保存对应的每张图片的文字。
#图片内容是中文，所以下载了中文识别包保存在tessdata里，这样才能识别出中文，不然识别出的是乱码。
#识别效果一般，有的序号被跳过去了，大概是图片质量不高的原因。

import os #用于操作文件和目录
from PIL import Image #用于图像处理。虽然写的是PIL其实是从系统中的Pillow库调的。pil已经停止更新了，Pillow是功能最新最全的图像处理库
import pytesseract #这是一个独立的模块，可以直接调用。Python 和tesseract的接口作用

def ocr_image_and_append_to_file(image_path, output_file):
    """
    进行OCR识别并将结果追加到指定的TXT文件中。
    
    参数:
    - image_path: 图片的路径
    - output_file: 输出TXT文件的对象
    """
    # 设置Tesseract的路径
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract_OCR\tesseract.exe'
    
    # 打开图片
    with Image.open(image_path) as img: #用Image库里的open方法打开图片路径并用pytesseract库里的image_to_string函数解读图片，存在text变量里
        # 进行OCR识别
        text = pytesseract.image_to_string(img, lang='chi_sim') #语言参数要设成chi_sim

    # 获取图片文件名（不含扩展名）
    image_name = os.path.splitext(os.path.basename(image_path))[0]
    #basename返回的是文件名加上扩展名。splittext将文件名和扩展名分开写在一个元组里（a,b）【0】取第一个返回文件名
    
    # 将结果追加到TXT文件中，格式为：图片名: 识别文本。n是用来换行的，使得每一个结果都占一行。f是占位符，{}里面的内容替换成实际的变量值。
    output_file.write(f"{image_name}: {text}\n")

def process_images_in_folder(input_folder, output_folder):
    """
    处理文件夹中的所有图片，进行OCR识别并将结果合并到一个TXT文件中。
    
    参数:
    - input_folder: 包含图片的输入文件夹
    - output_folder: OCR结果的输出文件夹
    """
    # 确保输出目录存在
    os.makedirs(output_folder, exist_ok=True)
    
    # 构建输出文件的完整路径
    output_file_path = os.path.join(output_folder, 'combined_output.txt')
    
    # 打开输出文件，如果文件不存在则创建，如果存在则清空内容
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        
        # 遍历文件夹中的所有文件
        for filename in os.listdir(input_folder):
            if filename.lower().endswith(('.jpg')):
                # 构建图片的完整路径
                image_path = os.path.join(input_folder, filename)
                # 调用OCR识别函数，将结果追加到输出文件
                ocr_image_and_append_to_file(image_path, output_file)

# 示例用法
input_folder = '../runs/detect/exp7/crops/dev_label'  # 替换为你的图片文件夹路径
output_folder = 'ocr_detection'  # 替换为你的输出文件夹路径

# 开始处理文件夹中的所有图片
process_images_in_folder(input_folder, output_folder)