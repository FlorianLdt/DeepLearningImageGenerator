from PIL import Image
import os, sys
import argparse
import random

image_counter = 0

def draw_random_wally_annotation(image, output_folder,layer_folder, layer_array, annotation_label):
    global image_counter
    if not os.path.exists(output_folder):
            os.mkdir(output_folder)

    random_layer = random.choice(layer_array)
    layer = Image.open(layer_folder+"/"+random_layer)
    random_x = random.randint(10, image.width - 10 - layer.width)
    random_y = random.randint(10, image.height - 10 - layer.height)
    x_max = random_x + layer.width
    y_max = random_y + layer.height
    box = (random_x, random_y, x_max, y_max)
    
    image.paste(layer, box)
    output_file = output_folder+str(image_counter)+'.jpg'
    image.save(output_file)
    f.write(str(output_file)+',[{"coordinates": {"height": '+str(layer.height)+', "width": '+str(layer.width)+', "x": '+str(random_x + int(layer.width / 2))+', "y": '+str(random_y + int(layer.height / 2))+'}, "label": "'+annotation_label+'"}]')
    f.write("\n")
    image_counter += 1 
    print('Printed: '+output_file)

def resize(input_path, dimensions):
    if not os.path.exists(input_path):
        raise ValueError("original path doesn't exist")

    if not os.path.exists("resized"):
            os.mkdir("resized")
    file_name = 0
    for file in os.listdir(input_path):
        if not file.endswith(".jpg") or file.endswith(".png"):
            print("file is not an image")
            continue
        origine_file_name = input_path+'/'+file
        im = Image.open(origine_file_name)
        resized_image = im.resize((dimensions, dimensions))
        resized_image_name = str(file_name)+os.path.splitext(file)[1]
        resized_image.save("resized/"+resized_image_name)
        print('Resized: '+resized_image_name)
        file_name += 1

def crop(input_path, initial_size, cropped_size):
    if not os.path.exists(input_path):
        raise ValueError("resized path doesn't exist")
    folder_name = str(int(cropped_size))
    if not os.path.exists(folder_name):
            os.mkdir(folder_name)
    
    saved_file_name = 0
    for file in os.listdir(input_path):
        if not file.endswith(".jpg") or file.endswith(".png"):
            print("file is not an image")
            continue
        file_name = os.path.splitext(file)[0]
        file_extension = os.path.splitext(file)[1]
        current_file_path = input_path+'/'+file_name+file_extension
        im = Image.open(current_file_path)
        ratio = initial_size / cropped_size
        sub_ratio = initial_size / ratio
        
        x = 1
        
        while x < ratio + 1:
            y = 1
            while y < ratio + 1:
                box = (sub_ratio * (x-1), sub_ratio * (y-1), sub_ratio*x, sub_ratio*y)
                region = im.crop(box)
                region.save(folder_name+'/'+str(saved_file_name)+file_extension)
                y += 1
                saved_file_name += 1
            x +=1
            print('Cropped: '+ file_name+file_extension)

def layer_array(folder_path):
    if not os.path.exists(folder_path):
        raise ValueError("layer path doesn't exist")
    layers_array = []
    for file in os.listdir(folder_path):
        if not file.endswith(".jpg") or file.endswith(".png"):
            print("file is not an image")
            continue
        layers_array.append(file)
    return layers_array

def createNewImages(input_path, output_path, size, iteration_number, layer_folder, layer_array, annotation_label):
    if not os.path.exists(input_path):
        raise ValueError("input_path doesn't exist")
    i = 0
    while i < iteration_number:
        new_image = Image.new("RGB", (size, size))
        ratio = int(1024 / 256)
        sub_ratio = int(1024 / 4)
        x = 1
        while x < ratio + 1:
            y = 1
            while y < ratio + 1:
                random_image = Image.open(input_path+random.choice(os.listdir(input_path)))
                # 0 -> No 
                # 1 -> FLIP_LEFT_RIGHT
                # 2 -> FLIP_TOP_BOTTOM
                # 3 -> FLIP_LEFT_RIGHT + FLIP_TOP_BOTTOM 
                transformMode = random.randint(0, 3)
                if transformMode == 1:
                    random_image = random_image.transpose(Image.FLIP_LEFT_RIGHT)
                elif transformMode == 2:
                    random_image = random_image.transpose(Image.FLIP_TOP_BOTTOM)
                elif transformMode == 2:
                    random_image = random_image.transpose(Image.FLIP_LEFT_RIGHT)
                    random_image = random_image.transpose(Image.FLIP_TOP_BOTTOM)
                box = (sub_ratio * (x-1), sub_ratio * (y-1), sub_ratio*x, sub_ratio*y)
                new_image.paste(random_image, box)              
                y += 1
            x +=1
        draw_random_wally_annotation(new_image, output_path,layer_folder, layer_array, annotation_label) 
        i += 1

def start(original_image_folder, resize_dimension, cropped_by, layer_folder, number_of_iteration, output_folder, annotation_label):
    resize(original_image_folder, resize_dimension)
    sub_square_dimension = resize_dimension / cropped_by
    crop("resized", resize_dimension, sub_square_dimension)
    l_array = layer_array(layer_folder)
    print(str(int(sub_square_dimension))+"/")
    createNewImages(str(int(sub_square_dimension))+"/", output_folder, resize_dimension, number_of_iteration, layer_folder, l_array, annotation_label)


parser = argparse.ArgumentParser(description=
'''Create random images from a list of original images and layers.

ex: python imageGenerator.py "original/" "layer/" 100 "images/"
will create 100 image from the original/ folder, will apply layers from the layer/ folder and generate those images in the images/ folder.''', formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('original_image_folder', metavar='original_image_folder', type=str, help='path of the folder containing the original images. ex: "original/"')
parser.add_argument('layer_folder', metavar='layer_folder', type=str, help='path of the folder containing the layer images. ex: "layer/"')
parser.add_argument('number_of_iteration', metavar='number_of_iteration', type=int, help='number of image genarated. ex: 100')
parser.add_argument('output_folder', metavar='output_folder', type=str, help='path of the folder where the images should be generated. ex: "images/"')
parser.add_argument('annotation_label', metavar='annotation_label', type=str, help='label of the annotation node. ex: "cat"')
args = parser.parse_args()

print('-- START')
f = open("annotations.csv", "w")
f.write("path,annotations")
f.write("\n")

original_image_folder = sys.argv[1]
resize_dimension = 1024
cropped_by = 4
layer_folder = sys.argv[2]
number_of_iteration = int(sys.argv[3])
output_folder = sys.argv[4]
annotation_label = sys.argv[5]
start(original_image_folder, resize_dimension, cropped_by, layer_folder, number_of_iteration, output_folder, annotation_label)


print('-- DONE WITH '+str(image_counter)+' IMAGES')






