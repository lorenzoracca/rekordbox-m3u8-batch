# Introduction

This Python script converts your Rekordbox collection into a hierarchy of _m3u8_ playlists and folders (for playlists that are inside a group).

This is especially helpful for syncing playlists into iTunes or to simply export your music to other software.

The script creates a folder called **playlists** in which you will find all your playlists converted to _m3u8_ playlist files and subfolders based on the hierarchy of your rekordbox library.

# Prerequisites and Usage

In order for this script to work properly you will need a few things before hand.

- a working Python installation. 
- export your collection from Rekordbox to an xml file. As of Rekordbox 7.0.1, this is easily done by clicking on File -> Export collection in xml format. 

  The script, as-is, needs the library file saved as a 'rekordbox.xml' file in the same folder as the script itself.

For execution, simply type `python rekordbox-m3u8-batch.py` in your terminal window or using your preferred Python environment. 

Run the file and the folder 'playlists' should appear. 

For iTunes usage, simply select all the playlists you wish to import and click 'Enter'. 
Voilà!

# DISCLAIMER

* This script does not read, modify or delete any other files in your OS other than the once it needs to convert your Rekordbox XML collection file into a hierarchy or _m3u8_ files and folders.
* This script is provided AS IS. Meaning no support is given if you run into issues.
* You are welcome to fork and/or make pull request in order to learn how it was done and/or add improvements.
* Any misuse of this script is **NOT** the resposability of the original AUTHOR.
