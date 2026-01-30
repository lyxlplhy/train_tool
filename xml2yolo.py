import os
import xml.etree.ElementTree as ET
import argparse

def convert_voc_to_yolo(voc_xml_dir, yolo_txt_dir, classes_file,good_code):
    """
    将VOC格式的XML标注文件转换为YOLO训练所需的TXT格式
    
    参数:
        voc_xml_dir: VOC格式XML文件所在目录
        yolo_txt_dir: 生成的YOLO格式TXT文件保存目录
        classes_file: 包含所有有效类别的classes.txt文件路径
    """
    # 创建输出目录（如果不存在）
    os.makedirs(yolo_txt_dir, exist_ok=True)
    
    # 读取classes.txt获取有效类别列表
    with open(classes_file, 'r', encoding='utf-8') as f:
        classes = [line.strip() for line in f if line.strip()]
    class_names = {cls: idx for idx, cls in enumerate(classes)}
    print(f"已加载 {len(classes)} 个有效类别")
    
    # 遍历所有XML文件
    for xml_filename in os.listdir(voc_xml_dir):
        if not xml_filename.endswith('.xml'):
            continue
            
        xml_path = os.path.join(voc_xml_dir, xml_filename)
        txt_filename = os.path.splitext(xml_filename)[0] + '.txt'
        txt_path = os.path.join(yolo_txt_dir, txt_filename)
        
        try:
            # 解析XML文件
            tree = ET.parse(xml_path)
            root = tree.getroot()
            
            # 获取图片宽高
            size = root.find('size')
            img_width = int(size.find('width').text)
            img_height = int(size.find('height').text)
            
            # 收集所有目标标注
            yolo_annotations = []
            has_valid_class = False
            
            for obj in root.iter('object'):
                # 获取类别名称
                cls_name = obj.find('name').text.strip()
                
                #背景生成
                if cls_name==good_code:
                    with open(txt_path, 'w', encoding='utf-8') as f:
                        f.write('')
                    continue
                
                # 检查是否为有效类别
                if cls_name not in class_names:
                    continue  # 跳过无效类别
                has_valid_class = True
                
                # 获取边界框坐标
                bbox = obj.find('bndbox')
                xmin = int(bbox.find('xmin').text)
                ymin = int(bbox.find('ymin').text)
                xmax = int(bbox.find('xmax').text)
                ymax = int(bbox.find('ymax').text)
                
                # 转换为YOLO格式（归一化中心坐标和宽高）
                x_center = (xmin + xmax) / 2.0 / img_width
                y_center = (ymin + ymax) / 2.0 / img_height
                width = (xmax - xmin) / img_width
                height = (ymax - ymin) / img_height
                
                # 确保坐标在0-1范围内
                x_center = max(0, min(1, x_center))
                y_center = max(0, min(1, y_center))
                width = max(0, min(1, width))
                height = max(0, min(1, height))
                
                # 添加到标注列表（类别ID + 坐标）
                cls_id = class_names[cls_name]
                yolo_annotations.append(f"{cls_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")
            
            # 只有当存在有效类别时才生成TXT文件
            if has_valid_class:
                with open(txt_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(yolo_annotations))
                print(f"已转换: {xml_filename} -> {txt_filename}")
            else:
                print(f"跳过: {xml_filename} (无有效类别)")
                
        except Exception as e:
            print(f"处理 {xml_filename} 时出错: {str(e)}")
    
    print("转换完成!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='voc转yolo')
    parser.add_argument('--VOC_XML_DIR', default="",help='源文件夹路径（将在该文件夹内创建分类子文件夹）')
    parser.add_argument('--YOLO_TXT_DIR', default="",help='源文件夹路径（将在该文件夹内创建分类子文件夹）')
    parser.add_argument('--CLASSES_FILE', default="",help='源文件夹路径（将在该文件夹内创建分类子文件夹）')
    parser.add_argument('--GOOD_CODE', default="",help='源文件夹路径（将在该文件夹内创建分类子文件夹）')
    args = parser.parse_args()

    # VOC_XML_DIR = "/root/code/ultralytics/ultralytics/data/m19/a/xml"    # VOC格式XML文件所在目录
    # YOLO_TXT_DIR = "/root/code/ultralytics/ultralytics/data/m19/a/labels"  # 输出的YOLO格式TXT文件目录
    # CLASSES_FILE = "/root/code/ultralytics/ultralytics/tools/classes.txt"             # 类别文件路径
    
    # 执行转换
    convert_voc_to_yolo(args.VOC_XML_DIR, args.YOLO_TXT_DIR, args.CLASSES_FILE,args.GOOD_CODE)