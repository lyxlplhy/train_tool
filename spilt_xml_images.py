import os
import shutil
import argparse

def is_photo(file_path):
    """判断文件是否为照片"""
    photo_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
    ext = os.path.splitext(file_path)[1].lower()
    return ext in photo_extensions

def is_xml(file_path):
    """判断文件是否为XML文件"""
    return os.path.splitext(file_path)[1].lower() == '.xml'

def get_unique_filename(dest_dir, original_name):
    """生成唯一的文件名，避免覆盖已有文件"""
    base_name, ext = os.path.splitext(original_name)
    counter = 1
    new_name = original_name
    
    while os.path.exists(os.path.join(dest_dir, new_name)):
        new_name = f"{base_name}_{counter}{ext}"
        counter += 1
    
    return new_name

def separate_files_in_place(src_dir):
    """在源文件夹内创建分类目录并分离文件"""
    # 在源文件夹内创建目标子文件夹
    images_dir = os.path.join(src_dir, 'images')
    xml_dir = os.path.join(src_dir, 'xml')
    
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(xml_dir, exist_ok=True)
    
    # 遍历源目录中的所有文件（不包括新创建的子文件夹）
    for root, _, files in os.walk(src_dir):
        # 跳过我们创建的目标文件夹，避免重复处理
        if root == images_dir or root == xml_dir:
            continue
            
        for file in files:
            src_path = os.path.join(root, file)
            
            # 检查文件类型并确定目标文件夹
            if is_photo(src_path):
                dest_dir = images_dir
            elif is_xml(src_path):
                dest_dir = xml_dir
            else:
                # 不是目标文件类型，跳过
                continue
            
            # 确保文件名唯一
            unique_name = get_unique_filename(dest_dir, file)
            dest_path = os.path.join(dest_dir, unique_name)
            
            try:
                # 移动文件（使用move而不是copy，因为是在同一目录下整理）
                shutil.move(src_path, dest_path)
                print(f"已移动: {src_path} -> {dest_path}")
            except Exception as e:
                print(f"处理文件失败 {src_path}: {str(e)}")

def main():
    # 设置命令行参数
    parser = argparse.ArgumentParser(description='在同一文件夹内将照片和XML文件分别整理到images和xml子文件夹')
    parser.add_argument('--source', default="/data/origin_data/HKC_H5/images",help='源文件夹路径（将在该文件夹内创建分类子文件夹）')
    
    args = parser.parse_args()
    
    # 检查源文件夹是否存在
    if not os.path.isdir(args.source):
        print(f"错误: 文件夹 '{args.source}' 不存在")
        return
    
    # 执行分离操作
    print(f"开始在 {args.source} 内整理文件...")
    separate_files_in_place(args.source)
    print("整理完成")

if __name__ == "__main__":
    main()
