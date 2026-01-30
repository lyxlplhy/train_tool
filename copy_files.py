import os
import shutil
import argparse
from collections import defaultdict

def is_photo_or_xml(file_path):
    """判断文件是否为照片或XML标签文件"""
    # 常见的照片文件扩展名
    photo_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
    ext = os.path.splitext(file_path)[1].lower()
    return ext in photo_extensions or ext == '.xml'

def get_unique_filename(dest_dir, original_name):
    """生成唯一的文件名，避免覆盖已有文件"""
    base_name, ext = os.path.splitext(original_name)
    counter = defaultdict(int)
    
    # 检查文件是否已存在，如果存在则添加后缀
    new_name = original_name
    while os.path.exists(os.path.join(dest_dir, new_name)):
        counter[base_name] += 1
        new_name = f"{base_name}_{counter[base_name]}{ext}"
    
    return new_name

def copy_files(src_dir, dest_dir):
    """递归复制源目录中的所有照片和XML文件到目标目录"""
    # 确保目标目录存在
    os.makedirs(dest_dir, exist_ok=True)
    
    # 遍历源目录中的所有内容
    for root, _, files in os.walk(src_dir):
        for file in files:
            src_path = os.path.join(root, file)
            if is_photo_or_xml(src_path):
                # 生成唯一的目标文件名
                unique_name = get_unique_filename(dest_dir, file)
                dest_path = os.path.join(dest_dir, unique_name)
                
                # 复制文件
                try:
                    shutil.copy2(src_path, dest_path)
                    print(f"复制: {src_path} -> {dest_path}")
                except Exception as e:
                    print(f"复制失败 {src_path}: {str(e)}")

def main():
    # 设置命令行参数
    parser = argparse.ArgumentParser(description='复制文件夹中的所有照片和XML标签文件到同一目录')
    parser.add_argument('--source',default="/data/origin_data/HKC_PROJECT/HKC_H5_20251231/20260127")
    parser.add_argument('--destination', default="/data/origin_data/HKC_PROJECT/HKC_H5_20251231/test_20260127")
    
    args = parser.parse_args()
    
    # 检查源文件夹是否存在
    if not os.path.isdir(args.source):
        print(f"错误: 源文件夹 '{args.source}' 不存在")
        return
    
    # 执行复制操作
    print(f"开始从 {args.source} 复制文件到 {args.destination}...")
    copy_files(args.source, args.destination)
    print("复制完成")

if __name__ == "__main__":
    main()
    