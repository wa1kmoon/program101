#!/usr/bin/env python3

import numpy as np
import astropy.coordinates as coord
import astropy.units as u
from datetime import datetime,timezone,timedelta
#from six.moves import urllib
#import shutil

def ecliptic(ra,dec):
    D2R = np.pi/180.0
    twopi = 2.0*np.pi
    fourpi = 4.0*np.pi
    R2D = 1.0/D2R
    
    psi=0.0
    stheta=0.39777715593
    ctheta=0.91748206207
    phi=0.0
    
    a = ra*D2R - phi
    b = dec*D2R
    sb = np.sin(b)
    cb = np.cos(b)
    cbsa = cb*np.sin(a)
    b = -stheta*cbsa + ctheta*sb
    w, = np.where(b > 1.0)
    if w.size > 0:
        b[w] = 1.0
    bo = np.arcsin(b)*R2D
    a = np.arctan2( ctheta*cbsa + stheta*sb, cb*np.cos(a))
    ao = ( (a+psi+fourpi) % twopi) * R2D
    
    return str(round(ao,6)),str(round(bo,6))



def visibility(name,ra,dec,fol,vilink):
    
    #
    # sexagesimal/degrees transformation
    #
    ra1,dec1=(float(ra),float(dec))
    ra1s=str(round(ra1,6))
    dec1s=str(round(dec1,6))
    
    #
    # transformation to galactic coords
    #
    c_icrs = coord.SkyCoord(ra1*u.degree, dec1*u.degree, frame='icrs')
    gal=c_icrs.galactic.to_string('decimal',precision=6).split()
    
    #
    # transformation to ecliptic coordinates
    #
    ecl=ecliptic(ra1,dec1)
    
    #
    # current date/time
    #
    utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)
    utc_hours=vilink[list(vilink.keys())[0]][0]
    tel_now = utc_now.astimezone(timezone(timedelta(hours=int(utc_hours))))
    
    nday=str(tel_now.day)
    if len(nday) == 1:
        nday="0"+nday
    
    nmonth=str(tel_now.month)
    if len(nmonth) == 1:
        nmonth="0"+nmonth
    
    nyear=str(tel_now.year)[2:]
    
    coordlist=ra+'+'+dec
    
    #
    # retrieving and saving the visibility plot
    #
    #print(vilink)
    link="http://catserver.ing.iac.es/staralt/index.php?action=showImage&form%5Bmode%5D=1&form%5Bday%5D="+nday+"&form%5Bmonth%5D="+nmonth+"&form%5Byear%5D="+str(tel_now.year)+"&form%5B"+vilink[list(vilink.keys())[0]][1]+"&form%5Bcoordlist%5D="+coordlist+"&form%5Bcoordfile%5D=&form%5Bparamdist%5D=2&form%5Bformat%5D=gif&submit=+Retrieve+"
    
    '''
    outf=fol+'/'+name+'/'+name+list(vilink.keys())[0]+'.gif'
    try:
        response,outf = urllib.request.urlopen(link),open(outf, 'wb')
        shutil.copyfileobj(response, outf)
        print('\n... plot saved to:', fol+'/'+name+'/'+name+list(vilink.keys())[0]+'.gif')
        return {"out":fol+'/'+name+'/'+name+list(vilink.keys())[0]+'.gif',"coord":[ra,dec],"coordD":[ra1s,dec1s],"coordG":[gal[0],gal[1]],"coordEc":[ecl[0],ecl[1]]}
    except Exception as e:
        print(str(e))
        return {"out":"-99","coord":[ra,dec],"coordD":[ra1s,dec1s],"coordG":[gal[0],gal[1]],"coordEc":[ecl[0],ecl[1]]} 
    '''
    return {"out":link}






def run_visibility(name,ra,dec,fol):
    vis = {}
    vilinks = {'Xinglong':['+8','observatory%5D=Xinglong+Observatory+(China)'],'Mauna Kea':['-10','observatory%5D=Mauna+Kea+Observatory+(Hawaii,+USA)'],'Nanshan':['+8','sitecoord%5D=87.1777++43.4708+2080'],'NOT':['+0','observatory%5D=Roque+de+los+Muchachos+Observatory+(La+Palma,+Spain)'],'Cerro Paranal':['-5','observatory%5D=Cerro+Paranal+Observatory+(Chile)']}
    #{'Xinlong':['+8','sitecoord%5D=117.964++40.6508+950'],'NOT':'observatory%5D=Roque+de+los+Muchachos+Observatory+(La Palma,+Spain)','Lijiang':'observatory%5D=Lijiang+Observatory+(China)'，'Mauna':'observatory%5D=Mauna+Kea+Observatory+(Hawaii,+USA)','Mauna':'sitecoord%5D=204.5317++19.8250+4215'}
    for vilin in vilinks:
        vilink = {vilin:vilinks[vilin]}
        keylist = visibility(name,ra,dec,fol,vilink)
        print(keylist['out'])
        vis[vilin]=keylist['out']
    return vis



name = 'test'
ra = '15.2'
dec = '22'
fol = './'

if __name__ == "__main__":
    run_visibility(name,ra,dec,fol)
    pass
    pass



