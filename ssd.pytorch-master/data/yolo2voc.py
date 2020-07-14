# Script to convert yolo annotations to voc format

# Sample format
# <annotation>
#     <folder>_image_fashion</folder>
#     <filename>brooke-cagle-39574.jpg</filename>
#     <size>
#         <width>1200</width>
#         <height>800</height>
#         <depth>3</depth>
#     </size>
#     <segmented>0</segmented>
#     <object>
#         <name>head</name>
#         <pose>Unspecified</pose>
#         <truncated>0</truncated>
#         <difficult>0</difficult>
#         <bndbox>
#             <xmin>549</xmin>
#             <ymin>251</ymin>
#             <xmax>625</xmax>
#             <ymax>335</ymax>
#         </bndbox>
#     </object>
# <annotation>
import os
import xml.etree.cElementTree as ET
from PIL import Image

ANNOTATIONS_DIR_PREFIX = "CUSTOMdevkit/JPEGImages"

DESTINATION_DIR = "CUSTOMdevkit/Annotations"

CLASS_MAPPING = {
    '0': 'button',
    '1': 'label',
    '2': 'radio-button',
    '3': 'textbox',
    '4': 'checkbox',
    '5': 'combobox',
    '6': 'spinbox',
    '7': 'menu',
    '8': 'submenu',
    '9': 'scrollbar',
    '10': 'progressbar',
    '11': 'dial',
    '12': 'tab',
    '13': 'tab-bar',
    '14': 'table',
    '15': 'slider',
    '16': 'calendar',
    '17': 'link',
    '18': 'switch',
    '19': 'icon-button',
    '20': 'dialogbox',
    '21': 'textarea',
    '22': 'close',
    '23': 'save',
    '24': 'load',
    '25': 'redo',
    '26': 'undo',
    '27': 'export',
    '28': 'new',
    '29': 'info',
    '30': 'search',
    '31': 'settings',
    '32': 'max-min',
    '33': 'dropdown',
    '34': 'text-combobox',
    '35': 'button-combobox'
}


def create_root(file_prefix, width, height):
    root = ET.Element("annotations")
    ET.SubElement(root, "folder").text = "JPEGImages"
    ET.SubElement(root, "filename").text = "{}.jpg".format(file_prefix)
    size = ET.SubElement(root, "size")
    ET.SubElement(size, "width").text = str(width)
    ET.SubElement(size, "height").text = str(height)
    ET.SubElement(size, "depth").text = "3"
    return root


def create_object_annotation(root, voc_labels):
    for voc_label in voc_labels:
        obj = ET.SubElement(root, "object")
        ET.SubElement(obj, "name").text = voc_label[0]
        ET.SubElement(obj, "pose").text = "Unspecified"
        ET.SubElement(obj, "truncated").text = str(0)
        ET.SubElement(obj, "difficult").text = str(0)
        bbox = ET.SubElement(obj, "bndbox")
        ET.SubElement(bbox, "xmin").text = str(voc_label[1])
        ET.SubElement(bbox, "ymin").text = str(voc_label[2])
        ET.SubElement(bbox, "xmax").text = str(voc_label[3])
        ET.SubElement(bbox, "ymax").text = str(voc_label[4])
    return root


def create_file(file_prefix, width, height, voc_labels):
    root = create_root(file_prefix, width, height)
    root = create_object_annotation(root, voc_labels)
    tree = ET.ElementTree(root)
    tree.write("{}/{}.xml".format(DESTINATION_DIR, file_prefix))


def read_file(file_path):
    file_prefix = file_path.split(".txt")[0]
    image_file_name = "{}.jpg".format(file_prefix)
    img = Image.open("{}/{}".format("CUSTOMdevkit/JPEGImages", image_file_name))
    w, h = img.size
    file_path = 'CUSTOMdevkit/JPEGImages/' + file_path
    with open(file_path, 'r') as file:
        lines = file.readlines()
        voc_labels = []
        for line in lines:
            voc = []
            line = line.strip()
            data = line.split()
            voc.append(CLASS_MAPPING.get(data[0]))
            bbox_width = float(data[3]) * w
            bbox_height = float(data[4]) * h
            center_x = float(data[1]) * w
            center_y = float(data[2]) * h
            voc.append(int(center_x - (bbox_width / 2)))
            voc.append(int(center_y - (bbox_height / 2)))
            voc.append(int(center_x + (bbox_width / 2)))
            voc.append(int(center_y + (bbox_height / 2)))
            voc_labels.append(voc)
        create_file(file_prefix, w, h, voc_labels)
    print("Processing complete for file: {}".format(file_path))


def start():
    if not os.path.exists(DESTINATION_DIR):
        os.makedirs(DESTINATION_DIR)
    for filename in os.listdir(ANNOTATIONS_DIR_PREFIX):
        if filename.endswith('txt'):
            read_file(filename)
        else:
            print("Skipping file: {}".format(filename))


if __name__ == "__main__":
    start()