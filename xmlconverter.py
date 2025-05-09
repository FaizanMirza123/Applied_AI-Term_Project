import os
import xml.etree.ElementTree as ET

def parse_annotation(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Extract image information
    filename = root.find('filename').text
    path = root.find('path').text
    width = int(root.find('size/width').text)
    height = int(root.find('size/height').text)
    
    objects = []
    
    # Extract object information (class and bounding box)
    for obj in root.findall('object'):
        class_name = obj.find('name').text
        xmin = int(obj.find('bndbox/xmin').text)
        ymin = int(obj.find('bndbox/ymin').text)
        xmax = int(obj.find('bndbox/xmax').text)
        ymax = int(obj.find('bndbox/ymax').text)
        
        objects.append({
            'class_name': class_name,
            'xmin': xmin,
            'ymin': ymin,
            'xmax': xmax,
            'ymax': ymax
        })
    
    return filename, path, width, height, objects
