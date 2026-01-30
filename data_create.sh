# #制作yolo训练格式数据集脚本

#包含images和xml的路径
source="/data/origin_data/HKC_PROJECT/HKC_H5_20251231/"

#生成训练集路径
respath="/data/train/hkc"

# 是否生成按label划分的数据集格式
Label_data_create=false

GOOD_CODE='good'

python copy_files.py \
    --source "${source}" \
    --destination "${respath}"

python spilt_xml_images.py \
    --source "${respath}"

#是否生成一个按照标签分类的文件夹，如下格式：
# -train_out 10711 1190
# --12PT0_G
# --12FB0_G
# --14DC0_G
if $Label_data_create; then
    python code_spilt.py \
        --xml_folder "${respath}/xml" \
        --images_folder "${respath}/images" \
        --output_folder "${respath}/out"
else
    echo "不生成按label划分文件夹"
fi

python xml2yolo.py \
    --VOC_XML_DIR "${respath}/xml" \
    --YOLO_TXT_DIR "${respath}/labels" \
    --CLASSES_FILE "../class_file/classeshkc.txt" \
    --GOOD_CODE  "${GOOD_CODE}"

python file_ismatch.py \
    --xml_folder "${respath}/labels"\
    --images_folder "${respath}/images"

python train_val_test.py \
    --img_dir "${respath}/images" \
    --label_dir "${respath}/labels" \
    --val_ratio 0.1

python create_datayaml.py \
    --classes_file_path "../class_file/classeshkc.txt" \
    --train_path "${respath}/images/train" \
    --val_path "${respath}/images/val" \
    --output_path "${respath}/data.yaml" \
    --good_code "${GOOD_CODE}"

# yolo start train
yolo task=detect mode=train model=../../model/yolov8l.pt data=${respath}/data.yaml epochs=180 batch=32 device=[1,2] imgsz=1024 patience=false