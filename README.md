# Texturepacker unpacker (for vamp survivors)
unpacks + repacks pngs using json files made by Texturepacker (doesn't support rotating)

Place the exe/python files into the directory containing json files and images and then run it, for vampire survivors this is \Steam\steamapps\common\Vampire Survivors\resources\app\.webpack\renderer\assets\img
(technically you don't have to do this since it asks for paths)

Normally, all the individual frames from animations and such would be separated into individual files, which makes it hard to keep track of all the images relating to each other in one folder, but I've added an option to export images as a spritesheet instead.

For some reason some animated frames are different sizes to each other, so those (smaller) frames are anchored to the center or to the bottom of a bigger dimension, with a red box around it showing the cutoff

I've also added a repack functionality, so you can actually edit and then use the generated spritesheets back into the game.

I should also note that you shouldn't rename the files of the images if you want to repack them, or they will just be ommitted from the repacked texture

The whole point of this is to make cool new textures for games and perhaps share them, so have fun and make some pixelart

[download here](https://github.com/SigilQuiver/Texturepacker-unpacker-vamp-survivors-/releases/tag/v0.0.1)
