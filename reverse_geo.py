#!/usr/bin/env python3

from os import fsencode
import argparse
import exiftool
from geopy.geocoders import Nominatim

parser = argparse.ArgumentParser(description='Simple reverse geocoding with geopy and exiftool')
parser.add_argument('files', nargs='+', help='files to reverse geocode')
files = parser.parse_args().files

geolocator = Nominatim()

with exiftool.ExifTool() as et:
    for f in files:
        gps = et.get_tag('GPSLatitude', f), et.get_tag('GPSLongitude', f)
        location = geolocator.reverse(gps).raw['address']
        creator = et.get_tag('Creator', f)
        copyright = et.get_tag('Copyright', f)
        keywords = ', '.join(et.get_tag('XMP-dc:Subject', f))
        title = et.get_tag('XMP-dc:Title')
        description = et.get_tag('XMP-dc:Description', f)

        # Make sure something is written in IPTC
        # so that the MWG tags write to IPTC as well
        params = map(fsencode, ["-IPTC:By-line=nobody should see this", f])
        et.execute(*params)
        
        params = map(fsencode, ["-MWG:Creator=" + creator,
                                "-MWG:Copyright=" + copyright,
                                "-MWG:Keywords=" + keywords,
                                "-MWG:Country=" + location['country'],
                                "-MWG:State=" + location['state'],
                                "-MWG:City=" + location['city'],
                                "-MWG:Location=" + location['city_district'],
                                f])
        et.execute(*params)
