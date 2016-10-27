#!/usr/bin/env python3

from os import fsencode
import argparse
import exiftool
from geopy.geocoders import Nominatim

parser = argparse.ArgumentParser(description='Simple reverse geocoding with geopy and exiftool')
parser.add_argument('files', nargs='+', help='files to reverse geocode')
files = parser.parse_args().files

# Use Nominatim, from OpenStreetMap, for reverse lookup
geolocator = Nominatim()

with exiftool.ExifTool() as et:
    for f in files:
        # Find place names from GPS already in file
        gps = et.get_tag('GPSLatitude', f), et.get_tag('GPSLongitude', f)
        location = geolocator.reverse(gps).raw['address']

        # Copy XMP info to IPTC (darktable does not write IPTC currently),
        # using xmp2iptc.args from exiftool's complete Perl distribution
        # This also ensures that the MWG tags write to IPTC as well
        with exiftool.ExifTool() as et_iptc:
            params = map(fsencode, ["-@", "xmp2iptc.args", f])
            print(et_iptc.execute(*params).decode('utf-8')) # output comes as byte

        # Apply reverse geocoding using MWG tag standards
        # (see, e.g., http://www.metadataworkinggroup.org/ and
        # http://www.sno.phy.queensu.ca/~phil/exiftool/TagNames/MWG.html)
        # This is a preliminary try, may vary based on country, region, etc.,
        # so will have to manually monitor and adjust in the future,
        # especially the Location tag
        params = map(fsencode, ["-MWG:Country=" + location['country'],
                                "-MWG:State=" + location['state'],
                                "-MWG:City=" + location['city'],
                                "-MWG:Location=" + location['city_district'],
                                f])
        print(et.execute(*params).decode('utf-8'))
