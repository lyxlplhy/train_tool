import os

def generate_yolo_data_yaml(classes_file, train_path, val_path, output_file,good_code):
    # 读取classes.txt文件
    try:
        with open(classes_file, 'r', encoding='utf-8') as f:
            classes = [line.strip() for line in f if line.strip()]
        
        if not classes:
            print("错误：classes.txt文件为空或只包含空白行")
            return False
        if good_code in classes:
            classes.remove(good_code)
    except FileNotFoundError:
        print(f"错误：找不到文件 {classes_file}")
        return False
    except Exception as e:
        print(f"读取classes.txt时出错：{str(e)}")
        return False
    
    # 获取分类数量
    nc = len(classes)
    
    # 生成YAML内容
    yaml_content = f"""train: {train_path}
val: {val_path}

# 分类数量
nc: {nc}

# 分类名称
names: {classes}
"""
    
    # 写入文件
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(yaml_content)
        print(f"\n成功生成data.yaml文件：{os.path.abspath(output_file)}")
        print("文件内容：")
        print("------------------------")
        print(yaml_content)
        print("------------------------")
        return True
    except Exception as e:
        print(f"写入文件时出错：{str(e)}")
        return False
    
import argparse

if __name__ == "__main__":
    # 获取所有用户输入
    parser = argparse.ArgumentParser(description='voc转yolo')
    parser.add_argument('--classes_file_path', default="/data/ultralytics/tools/class_file/classeshkc.txt",help='')
    parser.add_argument('--train_path', default="",help='')
    parser.add_argument('--val_path', default="",help='')
    parser.add_argument('--output_path', default="",help='')
    parser.add_argument('--good_code', default="",help='')
    args = parser.parse_args()
    # 调用函数生成文件
    generate_yolo_data_yaml(
        classes_file=args.classes_file_path,
        train_path=args.train_path,
        val_path=args.val_path,
        output_file=args.output_path,
        good_code=args.good_code
    )
    