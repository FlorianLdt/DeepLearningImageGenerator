# DeepLearningImageGenerator

Image generator that can be used in Deep Learning **(Image classification or Object Detection)** to increase the number of data.

## Overview

Initialy created for the project [WallyML](https://github.com/FlorianLdt/WallyML) and the talk **Solving “Where’s Wally?” with Turi Create**, this script can help generating a lot of image data for your Deep Learning project **(Image classification or Object Detection)** if you don't have initially access to a large amoubnt of data.

The script take an original images folder ...

<img src="https://github.com/FlorianLdt/DeepLearningImageGenerator/blob/master/doc/originals.png?raw=true" title="original images folder"/>

... and an layers folder ...

<img src="https://github.com/FlorianLdt/DeepLearningImageGenerator/blob/master/doc/layers.png?raw=true" title="layers folder"/>

... to generate randomized images ...

<img src="https://github.com/FlorianLdt/DeepLearningImageGenerator/blob/master/doc/generated.jpg?raw=true" title="randomized image"/>

... with the annotations.csv file (Turi Create format)
```
path,annotations
images/0.jpg,[{"coordinates": {"height": 36, "width": 27, "x": 567, "y": 600}, "label": "wally"}]
images/1.jpg,[{"coordinates": {"height": 550, "width": 290, "x": 596, "y": 290}, "label": "wally"}]
images/2.jpg,[{"coordinates": {"height": 46, "width": 23, "x": 843, "y": 415}, "label": "wally"}]
images/3.jpg,[{"coordinates": {"height": 40, "width": 34, "x": 580, "y": 677}, "label": "wally"}]
images/4.jpg,[{"coordinates": {"height": 105, "width": 51, "x": 196, "y": 91}, "label": "wally"}]
images/5.jpg,[{"coordinates": {"height": 903, "width": 512, "x": 752, "y": 495}, "label": "wally"}]
images/6.jpg,[{"coordinates": {"height": 131, "width": 57, "x": 74, "y": 232}, "label": "wally"}]
......
```


## Usage

This script is using the [Pillow](https://github.com/python-pillow/Pillow) library for image manipulations.

Please refer to the [Installation Guide](https://pillow.readthedocs.io/en/latest/installation.html) first to install Pillow before executing the script.

In the console, you can run `python DeepLearningImageGenerator.py -h` to have access to the help page of the script.

```
usage: DeepLearningImageGenerator.py [-h]
                                     original_image_folder layer_folder
                                     number_of_iteration output_folder
                                     annotation_label

Create random images from a list of original images and layers.

ex: python DeepLearningImageGenerator.py original/ layer/ 100 images/ cat
will create 100 image from the original/ folder, will apply layers from the layer/ folder and generate those images in the images/ folder.

positional arguments:
  original_image_folder
                        path of the folder containing the original images. ex:
                        "original/"
  layer_folder          path of the folder containing the layer images. ex:
                        "layer/"
  number_of_iteration   number of image genarated. ex: 100
  output_folder         path of the folder where the images should be
                        generated. ex: "images/"
  annotation_label      label of the annotation node. ex: "cat"

optional arguments:
  -h, --help            show this help message and exit
```

Let's assume that the hierarchy of your Deep Learning project is:

```
\MyDeepLearningProject
|_ original
   |_ 0.jpg
   |_ 1.jpg
   |_ 2.jpg
   |_ ...
|_ layer
   |_ layer0.jpg
   |_ layer1.jpg
   |_ layer2.jpg
   |_ ...
|_ DeepLearningImageGenerator.py
```
You can now run `DeepLearningImageGenerator.py original layer 10000 images cat`

When the generation will be finish, your Deep Learning project will look like:

```
\MyDeepLearningProject
|_ original
   |_ 0.jpg
   |_ 1.jpg
   |_ 2.jpg
   |_ ...
|_ layer
   |_ layer0.jpg
   |_ layer1.jpg
   |_ layer2.jpg
   |_ ...
|_ resized
   |_ 0.jpg
   |_ 1.jpg
   |_ 2.jpg
   |_ ...
|_ 256
   |_ 0.jpg
   |_ 1.jpg
   |_ 2.jpg
   |_ ...
|_ images
   |_ 0.jpg
   |_ 1.jpg
   |_ 2.jpg
   |_ ...
|_ annotations.csv
|_ DeepLearningImageGenerator.py
```

The resized images can be found in the `resized` folder, the cropped images can be found in the `256` folder, the generated images can be found in the `images` folder.

It has not been decided yet to remove the `resized` and `256` folder after execution.

## Contact
If you have a question or any comment, feel free to open an issue or to DM me on [@florianldt](https://twitter.com/florianldt).
