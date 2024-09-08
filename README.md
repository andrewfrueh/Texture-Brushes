# Texture painting in Blender

This repo has a starter-kit collection of texture brushes and a Blender add-on for importing images as textures.

## The brushes
The brushes in this collection were all painstakingly... um, lovinging, made by me. I created them by painting with ink on paper, then scanning, levingling, cropping, exporting, etc.

The brushes are available at multiple resolutions (0.1k, 1k, 4k). Beware that this kind of work is very GPU intensive, so make sure you import brushes that are appropriate for your hardware.

Here are some samples of the brushes you'll find...

![brush image](/Brush-Images/0.1k/1_a.png) ![brush image](/Brush-Images/0.1k/14_c.png) ![brush image](/Brush-Images/0.1k/9_c.png)



## The Blender add-on
I've also created an add-on for Blender that lets you import a bunch of images (like the texture brushes) as textures. I used the imfamous "import images as planes" add-on (which is now the internal feature "Add -> Image -> Mesh Plane") for reference.

https://docs.blender.org/manual/en/latest/addons/import_export/images_as_planes.html

### Images as Textures
The plugin included in this repo is "import images as textures" and has some properties that are appropriate for using textures. You can use it to import the brushes from this collection and then use those brushes to do some awesome texture painting. 

The add-on is here:
[Import Images as Textures add-on](Blender-Add-On/io_import_images_as_textures.py)

