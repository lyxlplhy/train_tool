import os
import logging
import argparse

def remove_unmatched_files(xml_folder, images_folder, recursive=False):
    # 配置日志记录
    logging.basicConfig(filename='remove_unmatched_files.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # 检查文件夹是否存在
    if not os.path.exists(xml_folder):
        logging.error(f"XML folder does not exist: {xml_folder}")
        raise FileNotFoundError(f"XML folder does not exist: {xml_folder}")
    if not os.path.exists(images_folder):
        logging.error(f"Images folder does not exist: {images_folder}")
        raise FileNotFoundError(f"Images folder does not exist: {images_folder}")

    # 获取文件夹中的文件名（包括子文件夹）
    def get_files(folder, extensions, recursive):
        files = set()
        if recursive:
            for root, _, filenames in os.walk(folder):
                for filename in filenames:
                    if filename.lower().endswith(extensions):
                        files.add(os.path.splitext(filename)[0])
        else:
            for filename in os.listdir(folder):
                if filename.lower().endswith(extensions):
                    files.add(os.path.splitext(filename)[0])
        return files

    # 获取xml文件夹中的所有XML文件名（不带扩展名）
    xml_files = get_files(xml_folder, ('.txt',), recursive)

    # 获取images文件夹中的所有图片文件名（不带扩展名）
    image_files = get_files(images_folder, ('.png', '.jpg', '.jpeg', '.bmp', '.gif'), recursive)

    # 找出xml文件夹中没有对应图片的XML文件
    unmatched_xml_files = [file for file in xml_files if file not in image_files]

    # 找出images文件夹中没有对应XML文件的图片
    unmatched_image_files = [file for file in image_files if file not in xml_files]

    # 删除xml文件夹中没有对应图片的XML文件
    for file in unmatched_xml_files:
        xml_path = os.path.join(xml_folder, file + '.txt')
        if os.path.exists(xml_path):
            os.remove(xml_path)
            logging.info(f"Deleted unmatched XML file: {xml_path}")
            print(f"Deleted unmatched XML file: {xml_path}")

    # 删除images文件夹中没有对应XML文件的图片
    for file in unmatched_image_files:
        for ext in ('.png', '.jpg', '.jpeg', '.bmp', '.gif'):
            image_path = os.path.join(images_folder, file + ext)
            if os.path.exists(image_path):
                os.remove(image_path)
                logging.info(f"Deleted unmatched image file: {image_path}")
                print(f"Deleted unmatched image file: {image_path}")

def main():
    parser = argparse.ArgumentParser(description='voc转yolo')
    parser.add_argument('--xml_folder', default="/data/train/HKC/images/xml",help='源文件夹路径（将在该文件夹内创建分类子文件夹）')
    parser.add_argument('--images_folder', default="/data/train/HKC/images/images",help='源文件夹路径（将在该文件夹内创建分类子文件夹）')
    args = parser.parse_args()

    recursive = True  # 设置为True以递归处理子文件夹s

    remove_unmatched_files(args.xml_folder, args.images_folder, recursive)

if __name__ == "__main__":
    main()


