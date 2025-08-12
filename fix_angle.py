from PIL import Image
from defusedxml import ElementTree
from argparse import ArgumentParser
import os
from tqdm import tqdm
from glob import glob
import sys


def arg_parse():
    parser = ArgumentParser()
    parser.add_argument("path",
                        type=str)
    return parser.parse_args()

def get_roll(element):
    return element[0][0].attrib['{http://www.dji.com/drone-dji/1.0/}GimbalRollDegree']

def set_roll(element, val):
    element[0][0].attrib['{http://www.dji.com/drone-dji/1.0/}GimbalRollDegree']  = val

def get_yaw(element):
    return element[0][0].attrib['{http://www.dji.com/drone-dji/1.0/}GimbalYawDegree']

def set_yaw(element, val):
    element[0][0].attrib['{http://www.dji.com/drone-dji/1.0/}GimbalYawDegree']  = val

def fix_dji_gimbal_metadata(path):
    try:
        im = Image.open(path)
        xmp_data = im.info.get('xmp')
        root = ElementTree.fromstring(xmp_data)
    except Exception as e:
        print(f"read file {path} got error")
        raise e
    roll = float(get_roll(root))
    yaw = float(get_yaw(root))
    if roll > 180:
        raise ValueError(f"Unexpected roll > 180: {roll} in file {path}")
    if roll == 180:
        new_roll = "+0.00"
        correct_yaw = yaw + 180
        new_yaw = f"{correct_yaw:+.2f}"
        set_roll(root, new_roll)
        set_yaw(root, new_yaw)
        im.save(path, exif=im.info.get('exif'), xmp=ElementTree.tostring(root))
    im.close()

if __name__ == "__main__":
    root = arg_parse().path
    paths = glob(os.path.join(root, "**", "*.JPG"))
    paths += glob(os.path.join(root, "**", "*.jpg"))
    paths = list(set(paths))
    print(f"Total images: {len(paths)}, process? [Y]")
    k = input()
    if k != "Y":
        sys.exit()
    for p in tqdm(paths):
        fix_dji_gimbal_metadata(p)
