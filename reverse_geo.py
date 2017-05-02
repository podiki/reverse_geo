#!/usr/bin/env python3

from os import fsencode
import argparse
import exiftool
from geopy.geocoders import Nominatim

# Dictionary of tags for ExifTool locations to data from geopy
tags = {'-MWG:Country=': 'country', '-MWG:State=': 'state', '-MWG:City=': 'city',
        '-MWG:Location=': 'city_district'}

parser = argparse.ArgumentParser(description='Simple reverse geocoding with geopy and exiftool')
parser.add_argument('files', nargs='+', help='files to reverse geocode')
files = parser.parse_args().files

# Use Nominatim, from OpenStreetMap, for reverse lookup
geolocator = Nominatim()

with exiftool.ExifTool() as et:
    for f in files:
        # Find place names from GPS already in file
        # Note: use the XMP tags so that lat/long has a - sign for W or S
        gps = et.get_tag('XMP:GPSLatitude', f), et.get_tag('XMP:GPSLongitude', f)
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
        # This works best for cities, for rural areas (e.g. when hiking) let's
        # use the county if available. Would be great to get more info, but for
        # now that works okay. There may be a lot of variation in what makes
        # sense, especially the Location tag, so may need to make this more
        # sophisticated in the future.
        params = []

        for k in tags:
            if tags[k] in location:
                params.append(k + location[tags[k]])
            elif k == '-MWG:Location=' and 'county' in location:
                params.append(k + location['county'])

        # Then add the filename and encode everything
        params.append(f)
        params = map(fsencode, params)

        # Do the tagging!
        print(et.execute(*params).decode('utf-8'))
