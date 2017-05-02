# reverse_geo
Simple reverse geocoding with Python and ExifTool

## Requirements
[ExifTool](http://www.sno.phy.queensu.ca/~phil/exiftool/) for reading/writing EXIF/IPTC/XMP tags in images, [pyexiftool](https://github.com/smarnach/pyexiftool) for using ExifTool from Python, and [geopy](https://github.com/geopy/geopy) for reverse geocoding. This script has only been used with Python 3.5.2.

## Usage
Run the following command
``` shell
python reverse_geo.py files
```
where files are the images to be updated. ExifTool will not override the files; the originals will be renamed with `_original` at the end.

## Notes
This is just a simple script which copies XMP tags to IPTC (since [darktable](https://www.darktable.org/) currently does not write IPTC tags) and then uses embedded GPS coordinates to do a reverse lookup and fill in location tags. This last part has only been tested in European cities, and some rural US areas where it uses county if no city information. This should cover a lot of use cases, but might need to be updated with more sophisticated handling for other locations. This is written with Metadata Working Group [MWG](http://www.metadataworkinggroup.org/) standards as [handled](http://www.sno.phy.queensu.ca/~phil/exiftool/TagNames/MWG.html) by ExifTool.
