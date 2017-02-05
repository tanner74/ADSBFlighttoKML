# capture_dump1090, Python script to capture aircraft.json data to a CSV file
# every one second.
#
# Copyright 2017 by Michael Tan <michael.tan@gmail.com>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE.

#import urllib.request      #for Python 3
import urllib2              #for Python 2.7

import json
import os
import time
from time import gmtime, strftime
from datetime import datetime

url = 'http://192.168.10.58/dump1090/data/aircraft.json'        # where to get the aircraft.json
ADSBDir = 'd:/adsb/'                                            # where to save the CSV files

headers = {'Cache-Control':'no-cache','Pragma':'no-cache','If-Modified-Since':'Sat, 1 Jan 2000 00:00:00 GMT',}

while 1:

    #use next two lines if you are using Python 3
    #request=urllib.request.Request(url, None, headers)
    #response = urllib.request.urlopen(request)

    #use next two lines if you are using Python 2.7
    request=urllib2.Request(url, None, headers)
    response = urllib2.urlopen(request)

    data = response.read().decode('utf8')
    jsonPlane = json.loads(data)

    # CSV file named as dump1090_YY-MM-DD.csv using UTC time
    fileName = ADSBDir+'dump1090_'+datetime.utcnow().strftime("%Y-%m-%d")+'.csv'

    if os.path.isfile(fileName):
        ADSBFile = open(fileName, 'a')
    else:
        ADSBFile = open(fileName, 'w')
        ADSBFile.write('UTC,icao,flight,spd,lat,lon,altitude,mlat\n')       #header

    for plane in jsonPlane['aircraft']:

        resultStr = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") + ','

        if int(plane['seen']) <= 1:                         # planes that have been seen within the last one second
            if 'seen_pos' in plane:                         # if it's been seen, let's save some data

                # if additional data is wanted, add it below and adjust the header

                if 'hex' in plane:
                    resultStr = resultStr +str(plane['hex']) + ','
                else:
                    resultStr = ','

                if 'flight' in plane:
                    resultStr = resultStr + str(plane['flight']).strip() + ','
                else:
                    resultStr = resultStr + ','

                if 'speed' in plane:
                    resultStr = resultStr + str(plane['speed']) + ','
                else:
                    resultStr = resultStr + ','

                if 'lat' in plane:
                    resultStr = resultStr + str(plane['lat']) + ','
                else:
                    resultStr = resultStr + ','

                if 'lon' in plane:
                    resultStr = resultStr + str(plane['lon']) + ','
                else:
                    resultStr = resultStr +','

                if 'altitude' in plane:
                    resultStr = resultStr + str(plane['altitude']) + ','
                else:
                    resultStr = resultStr +','

                if 'mlat' in plane:
                    resultStr = resultStr + 'True'
                else:
                    resultStr = resultStr + 'False'

                ADSBFile.write(resultStr+'\n')

                # comment the below if you do not want to see on the console what is being saved
                print (resultStr)
    ADSBFile.close()
    time.sleep(1)
