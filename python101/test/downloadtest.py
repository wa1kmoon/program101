#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 21:29:49 2020

@author: xlew
"""

import os
import shutil
import warnings
import re
import random
import csv
import math
import sewpy
import astropy.coordinates as coord
import matplotlib
matplotlib.use('Agg')
import matplotlib.patheffects as PathEffects
import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
from astropy.visualization import AsinhStretch, PercentileInterval
from astropy.wcs import WCS
import astropy.units as u
from matplotlib.patches import Circle, FancyArrowPatch
from six.moves import urllib
import matplotlib.image as mpimg
import time as t

name='test'
time='191106.584'
ra='198.5560'
dec='11.2698'
radius='0.0003'
fol='./'

size=20
ra1,dec1=(float(ra),float(dec))
raS=ra.replace(':','%3A')
decS=dec.replace(':','%3A')
ra_dec=coord.SkyCoord(ra+' '+dec, unit=(u.deg, u.deg))
ra_hms='%02.f:%02.f:%05.2f' % (ra_dec.ra.hms)
dec_dms='%02.f:%02.f:%05.2f' % (ra_dec.dec.dms[0],abs(ra_dec.dec.dms[1]),abs(ra_dec.dec.dms[2]))

#### size /arcminutes
link='http://archive.eso.org/dss/dss/image?ra='+raS+'&dec='+decS+'&equinox=J2000&name=&x='+str(size)+'&y='+str(size)+'&Sky-Survey=DSS2-red&mime-type=download-fits&statsmode=WEBFORM'
#eg: 'http://archive.eso.org/dss/dss/image?ra=1%3A32%3A32&dec=32%3A12%3A32&equinox=J2000&name=&x=10&y=10&Sky-Survey=DSS2-red&mime-type=download-fits&statsmode=WEBFORM'
outf_path=fol+'/'+name+'/'+name+'_dss_red.fits'
csv_outf=fol+'/'+name+'/'+name+'.csv'
#with urllib.request.urlopen(link) as response, open(outf, 'wb') as outf:
startime = t.perf_counter()
print(startime)
response = urllib.request.urlopen(link)  #返回一个reponse对象，保存网页信息
end1time = t.perf_counter()
print(end1time)
outf = open(outf_path, 'wb')
# filelength = len(urllib.request.urlopen(link).read())
#shutil.copyfileobj(response, outf) #将网页内容复制到上一步新建的fits文件
#end2time = t.perf_counter()
#print(end2time)
# with open(outf_path,'rb') as fileobj:
#     if len(fileobj.read()) == filelength:
#         print('\t... image saved to:', outf_path)
#     fileobj.close()
