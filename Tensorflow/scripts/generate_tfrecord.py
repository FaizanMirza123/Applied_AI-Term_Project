import os
import xml.etree.ElementTree as ET
import tensorflow as tf
from object_detection.utils import dataset_util
import glob
# Function to parse the XML annotation
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


# Function to convert the annotation data into TFRecord format
def create_example(image_path, width, height, objects):
    # Read image
    with tf.io.gfile.GFile(image_path, 'rb') as fid:
        encoded_image = fid.read()
    
    # Define features
    feature = {
        'image/encoded': dataset_util.bytes_feature(encoded_image),
        'image/filename': dataset_util.bytes_feature(bytes(image_path, 'utf8')),
        'image/format': dataset_util.bytes_feature(b'jpg'),
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
    }
    
    # Add objects' bounding boxes and labels
    xmins = [obj['xmin'] / width for obj in objects]
    ymins = [obj['ymin'] / height for obj in objects]
    xmaxs = [obj['xmax'] / width for obj in objects]
    ymaxs = [obj['ymax'] / height for obj in objects]
    
    classes = [1 for obj in objects]  # Assuming 'hello' is the only class for now
    
    feature.update({
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/label': dataset_util.int64_list_feature(classes)
    })
    
    example = tf.train.Example(features=tf.train.Features(feature=feature))
    return example


# Function to write the TFRecord
def write_to_tfrecord(xml_files, tfrecord_file):
    with tf.io.TFRecordWriter(tfrecord_file) as writer:
        for xml_file in xml_files:
            filename, path, width, height, objects = parse_annotation(xml_file)
            example = create_example(path, width, height, objects)
            writer.write(example.SerializeToString())

def write_to_tfrecord(xml_files, tfrecord_file):
    with tf.io.TFRecordWriter(tfrecord_file) as writer:
        for xml_file in xml_files:
            filename, path, width, height, objects = parse_annotation(xml_file)
            example = create_example(path, width, height, objects)
            writer.write(example.SerializeToString())

if __name__ == "__main__":
    test_xml_files = glob.glob(r'Tensorflow/workspace/images/test/*.xml')
    train_xml_files = glob.glob(r'Tensorflow/workspace/images/train/*.xml')

    # Convert and save the TFRecords
    write_to_tfrecord(train_xml_files, 'Tensorflow/workspace/annotations/train.record')
    write_to_tfrecord(test_xml_files, 'Tensorflow/workspace/annotations/test.record')
    print("TFRecord files created successfully.")