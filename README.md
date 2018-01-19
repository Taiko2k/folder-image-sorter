# Folder Image Sorter
A basic GUI for sorting images into given folder names with an image preview.

![screenshot](https://raw.githubusercontent.com/Taiko2k/folder-image-sorter/master/Screenshot.png)
___

Imagine you have a folder of images, say animal pictures, and you want to sort each type into its own folder. For example; 'dogs' and 'cats', normally you might use your file manager, but if there's many types and many files, this may become a little tiresome.

This application allows you to queue up images and give each image a folder name to be moved to.

Tips:

 - Use short folder names for fast sorting, like 'c' for cat. You can always rename the folders later.
 - Press TAB to reuse the last label. TAB will also auto-complete to closest previous match.
 - Entering a blank label will skip that image
 - If you make a mistake, just press the 'Previous' button and re-enter a new label
 - Checking the checkbox will allow you to delete images just by hitting the Delete key, otherwise use Ctrl+Delete.

 ___
 ### Usage

 You will need pyqt5 installed.

 Run `python3 main.py`
