import xml.etree.ElementTree as ET
import os

def parse_xml(path,names_dict):
    tree = ET.parse(path)
    img_name = path.split('/')[-1][:-4]
    
    height = tree.findtext("./size/height")
    width = tree.findtext("./size/width")

    objects = [img_name, width, height]

    for obj in tree.findall('object'):
        difficult = obj.find('difficult').text
        if difficult == '1':
            continue
        name = obj.find('name').text
        bbox = obj.find('bndbox')
        xmin = bbox.find('xmin').text
        ymin = bbox.find('ymin').text
        xmax = bbox.find('xmax').text
        ymax = bbox.find('ymax').text

        name = str(names_dict[name])
        objects.extend([name, xmin, ymin, xmax, ymax])
    if len(objects) > 1:
        return objects
    else:
        return None

def convert_voc_yolo(txt_path, annot_path,img_path, class_names_path ):
    img_path =  os.path.abspath(img_path)
#   Create dictionary mapping for class labels
    names_dict = {}
    cnt = 0
    f = open(class_names_path, 'r').readlines()
    for line in f:
        line = line.strip()
        names_dict[line] = cnt
        cnt += 1
     
#   Create a list of image file names without extension

    img_files = os.listdir(img_path)
    img_names = []
    for file in img_files:
        f, e = os.path.splitext(file)
        img_names.append(f)

#   From annotation file get the bounding boxes and save to file txt_path
    train_cnt = 0
    f = open(txt_path, 'w')

    for img_name in img_names:
        img_name = img_name.strip()
        xml_path = os.path.join(annot_path, img_name + '.xml', )
        objects = parse_xml(xml_path,names_dict)

        if objects:

            objects[0] = os.path.join(img_path,img_name + '.jpg')
            if os.path.exists(objects[0]):
                objects.insert(0, str(train_cnt))
                train_cnt += 1
                objects = ' '.join(objects) + '\n'
                f.write(objects)
    f.close()