import os
import shutil
import random
from pathlib import Path

def remove_unmatched_images(img_dir, label_dir, img_extensions=('jpg', 'jpeg', 'png', 'bmp')):
    """删除没有对应标签的图片"""
    # 获取所有标签文件名（不含扩展名）
    label_files = {os.path.splitext(f)[0] for f in os.listdir(label_dir) if os.path.isfile(os.path.join(label_dir, f))}
    
    # 遍历图片文件夹，删除没有对应标签的图片
    removed_count = 0
    for img_file in os.listdir(img_dir):
        if img_file.lower().endswith(img_extensions):
            img_base = os.path.splitext(img_file)[0]
            if img_base not in label_files:
                img_path = os.path.join(img_dir, img_file)
                os.remove(img_path)
                removed_count += 1
                print(f"已删除: {img_path}")
    
    print(f"总共删除了 {removed_count} 张没有对应标签的图片")

def split_dataset_in_place(img_dir, label_dir, val_ratio=0.2, seed=42):
    """在原文件夹中划分训练集和验证集"""
    # 设置随机种子，确保结果可复现
    random.seed(seed)
    
    # 创建train和val子目录
    for sub_dir in ['train', 'val']:
        os.makedirs(os.path.join(img_dir, sub_dir), exist_ok=True)
        os.makedirs(os.path.join(label_dir, sub_dir), exist_ok=True)
    
    # 获取所有图片文件名（不含扩展名）
    img_files = [f for f in os.listdir(img_dir) if os.path.isfile(os.path.join(img_dir, f)) and 
                not f.startswith('.') and not f.lower().endswith(('.txt', '.xml', '.json'))]
    
    # 划分训练集和验证集
    random.shuffle(img_files)
    val_size = int(len(img_files) * val_ratio)
    val_files = img_files[:val_size]
    train_files = img_files[val_size:]
    
    # 移动文件到对应的目录
    def move_files(file_list, split):
        for img_file in file_list:
            img_base, img_ext = os.path.splitext(img_file)
            # 移动图片
            src_img = os.path.join(img_dir, img_file)
            dst_img = os.path.join(img_dir, split, img_file)
            shutil.move(src_img, dst_img)
            
            # 查找对应的标签文件
            label_extensions = ('.txt', '.xml', '.json')  # 根据实际情况调整
            label_file = None
            for ext in label_extensions:
                potential_label = os.path.join(label_dir, f"{img_base}{ext}")
                if os.path.exists(potential_label):
                    label_file = potential_label
                    break
            
            if label_file:
                dst_label = os.path.join(label_dir, split, os.path.basename(label_file))
                shutil.move(label_file, dst_label)
            else:
                print(f"警告: 图片 {img_file} 没有找到对应的标签文件")
    
    # 移动训练集文件
    move_files(train_files, 'train')
    print(f"已移动 {len(train_files)} 个训练样本")
    
    # 移动验证集文件
    move_files(val_files, 'val')
    print(f"已移动 {len(val_files)} 个验证样本")

import argparse

def main():
    # 设置目录路径

    parser = argparse.ArgumentParser(description='将JSON标注文件转换为YOLO格式')
    parser.add_argument('--img_dir',default="/root/data/all_new/train/images", help='输入JSON文件所在目录')
    parser.add_argument('--label_dir',default='/root/data/all_new/train/labels', help='输出YOLO格式文件的目录')
    parser.add_argument('--val_ratio',default="",type=float, help='划分比列')
    
    # 解析命令行参数
    args = parser.parse_args()

    img_dir = args.img_dir  # 原始图片文件夹
    label_dir = args.label_dir  # 原始标签文件夹
    
    # 验证集比例
    val_ratio = args.val_ratio
    
    # 1. 删除没有对应标签的图片
    remove_unmatched_images(img_dir, label_dir)
    
    # 2. 在原文件夹中划分数据集
    split_dataset_in_place(img_dir, label_dir, val_ratio)
    
    print("数据处理完成！")

if __name__ == "__main__":
    main()    