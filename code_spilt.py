import os
import shutil
import xml.etree.ElementTree as ET

def process_xml_and_images(xml_folder, images_folder, output_folder):
    # 创建输出目录
    os.makedirs(output_folder, exist_ok=True)
    
    # 获取所有XML文件和图片文件
    xml_files = {os.path.splitext(f)[0]: f for f in os.listdir(xml_folder) if f.endswith('.xml')}
    image_files = {os.path.splitext(f)[0]: f for f in os.listdir(images_folder) if 
                   f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))}
    
    # 遍历每个XML文件
    for base_name, xml_file in xml_files.items():
        # 检查是否有对应的图片
        if base_name not in image_files:
            continue
        
        xml_path = os.path.join(xml_folder, xml_file)
        image_path = os.path.join(images_folder, image_files[base_name])
        
        try:
            # 解析XML文件获取标签
            tree = ET.parse(xml_path)
            root = tree.getroot()
            
            # 假设XML中有一个名为'tag'的标签
            tag_element = root.find('object')
            tag_element=tag_element.find("name")
            if tag_element is None:
                print(f"警告: XML文件 {xml_file} 中未找到'tag'元素")
                continue
            
            tag = tag_element.text.strip()
            
            # 创建标签对应的输出子目录
            tag_folder = os.path.join(output_folder, tag)
            os.makedirs(tag_folder, exist_ok=True)
            
            # 复制文件到标签目录
            shutil.copy2(xml_path, os.path.join(tag_folder, xml_file))
            shutil.copy2(image_path, os.path.join(tag_folder, image_files[base_name]))
            
            print(f"已处理: {base_name} -> 标签 '{tag}'")
        except Exception as e:
            print(f"处理文件 {base_name} 时出错: {str(e)}")

import argparse

if __name__ == "__main__":
    # 设置目录路径

    parser = argparse.ArgumentParser(description='voc转yolo')
    parser.add_argument('--xml_folder', default="/data/train/tm16/G5/xml",help='源文件夹路径（将在该文件夹内创建分类子文件夹）')
    parser.add_argument('--images_folder', default="/data/train/tm16/G5/images",help='源文件夹路径（将在该文件夹内创建分类子文件夹）')
    parser.add_argument('--output_folder', default="/data/origin_data/TM16_PROJECT/G5/train",help='源文件夹路径（将在该文件夹内创建分类子文件夹）')
    args = parser.parse_args()

    xml_folder = args.xml_folder
    images_folder = args.images_folder
    output_folder = args.output_folder
    
    process_xml_and_images(xml_folder, images_folder, output_folder)
    print("处理完成!")    