# reSmush.it Image Optimizer Python package

[![Downloads](https://static.pepy.tech/badge/resmushit)](https://pepy.tech/project/resmushit)
![Tests](https://github.com/hemansah/resmushit/actions/workflows/tests.yaml/badge.svg?branch=master)  

## Project Description

Python3 wrapper for resmush.it API to optimize image file size.

    

[resmush.it](https://resmush.it/) Image Optimizer allows you to use free Image optimization based on reSmush.it API.

reSmush.it provides image size reduction based on several algorithms. The API accept JPG, PNG and GIF files up to 5MB.



## Installation

1. Install using pip3:

  

    `$ pip3 install resmushit`

  

## Usage

```
import resmushit

# Save image to current directory
resmushit.from_path(image_path='image.png', quality=95) 

# Save image to preferred directory
resmushit.from_path(image_path='image.png', quality=95, output_dir="output/") 

# return image bytes
_bytes = resmushit.from_url(image_url="https://ps.w.org/resmushit-image-optimizer/assets/icon-128x128.png", quality=95, save=False)

```

  

## Options

```
image_url (str): The url of image.

image_path (str): The path of image

quality (int): Quality at which image is going to be optimized.

output_dir (str): Location for output image.

preserve_exif (bool): Preserve EXIF data in the file after optimization.

preserve_filename (bool): Optimized image will prefix 'optimized-' before image name.

quiet_mode (bool): Run in quiet mode when True

save (bool): When True, saves image in directory.
             When False, returns bytes of image.             
```

