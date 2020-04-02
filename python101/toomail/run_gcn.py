#!/usr/bin/env python

import gcn
import os
import lxml.etree
import astropy.utils.data as astrodata
from astropy.io import fits as fits
import run_visibility
import run_identification
import run_mail


# Define your custom handler here.
#@gcn.handlers.include_notice_types(
#    gcn.notice_types.TEST_COORDS,
#    gcn.notice_types.SWIFT_TOO_FOM,
#    gcn.notice_types.SWIFT_BAT_GRB_ALERT,
#    gcn.notice_types.SWIFT_UVOT_DBURST,
#    gcn.notice_types.SWIFT_XRT_POSITION)
#gcn_keys_list=['gcn_name', 'ra', 'dec', 'fol', 'gcn_img', 'gcn_Packet_Type']

def write_log(TrigID_new,grb_time,TrigID_old):
    #### write logfile
    print(TrigID_new,grb_time,TrigID_old)
    with open('toomail.log','a+') as too_log:
        too_log.seek(0)
        histort=too_log.readlines()
        too_log.write(TrigID_new+' '+grb_time+'\n')
    for i in histort:
        if TrigID_old in i:
            grb_time = i.split()[-1]
    return grb_time



def process_gcn(payload, root):
    # Respond only to 'test' events.
    # VERY IMPORTANT! Replace with the following code
    # to respond to only real 'observation' events.
    # Read all of the VOEvent parameters from the "What" section.
    params = {elem.attrib['name']:
              elem.attrib['value']
              for elem in root.iterfind('.//Param')}
    #passnum = ['83', '140', '141']
    #SWIFT = [60,61,62,67,81]
    SWIFT = {'60':'SWIFT_BAT','61':'SWIFT_BAT','62':'SWIFT_BAT','67':'SWIFT_XRT','81':'SWIFT_UVOT'}
    #INTEGRAL = [53,55]
    #FERMI = [120,121,128]
    #SNEWS = [149,]
    #AMON = [157,158]
    passnum = SWIFT #+ INTEGRAL + FERMI + SNEWS + AMON
    Packet_Type = params['Packet_Type']
    print(Packet_Type)
    #print(gcn_name)
    ##### check gcn
    if Packet_Type not in passnum :
        return
    gcn_Packet_Type=SWIFT[Packet_Type]
    #if 'SWIFT' not in gcn_name:
    #    return
    #if root.attrib['role'] != 'test':
    #    return
    who = root.find('.//{*}Who')
    gcn_time = str(who.find('.//{*}Date').text)
    TimeInstant = root.find('.//{*}TimeInstant')
    grb_time_s = str(TimeInstant.find('.//{*}ISOTime').text)
    #grb_time=grb_time_s[2:4]+grb_time_s[5:7]+grb_time_s[8:10]+str((int(grb_time_s[11:13])*3600+int(grb_time_s[14:15])*60+float(grb_time_s[17:]))/86400+0.000001)[1:5]
    grb_day = params['Burst_TJD']
    grb_day_time = params['Burst_SOD']
    grb_day_time_s = str((float(grb_day_time)/86400+0.00000001))
    grb_day_jd = float(grb_day)+2440000.5+float(grb_day_time)/86400
    #t_now = Time(obj_date, format='isot', scale='utc')
    #now_jd = t_now.jd
    grb_time = grb_time_s[2:4]+grb_time_s[5:7]+grb_time_s[8:10]+"{:.3f}".format(float(grb_day_time_s))[1:5]
    #gcn_name = os.path.basename(root.attrib['ivorn']).split('.')[0]
    TrigID_new=root.attrib['ivorn'].split('_')[-1]
    try:
        Citations = root.find('.//{*}Citations')
        TrigID_old = str(Citations.find('.//{*}EventIVORN').text).split('_')[-1]
    except:
        TrigID_old='00000'
    grb_time = write_log(TrigID_new,grb_time,TrigID_old)
    print(grb_time)
    gcn_name = 'GCN'+gcn_time
    fol = globals()['fol']
    os.system('mkdir '+fol+'/'+gcn_name)
    #### save xml
    _voname = fol+'/'+gcn_name+'/'+gcn_name+'.xml'
    print(_voname)
    if os.path.exists(_voname):
        return
    else:
        with open(_voname,'wb+') as _vo:
            _vo.write(payload)
    #print(payload)
    # Look up right ascension, declination, and error radius fields.
    pos2d = root.find('.//{*}Position2D')
    ra = str(pos2d.find('.//{*}C1').text)
    dec = str(pos2d.find('.//{*}C2').text)
    radius = str(pos2d.find('.//{*}Error2Radius').text)

    #### other thing
    Sun_Distance = params['Sun_Distance']
    MOON_Distance = params['MOON_Distance']
    ## make ds9.reg
    try:
        ds9_reg=fol+'/'+gcn_name+'/GRB'+grb_time+'_'+gcn_Packet_Type+'.reg'
        a=open(ds9_reg,'w')
        ds9_list_1='global color=green dashlist=8 3 width=1 font="helvetica 10 normal roman" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1\nfk5\n\n'
        radius_s=str(float(radius)*3600)
        ds9_list_2='circle('+ra+','+dec+','+radius_s+'")\ncircle('+ra+','+dec+',15") # color=red width=2\n'
        ds9_list=ds9_list_1+ds9_list_2
        a.write(ds9_list)
        a.close()
    except:
        pass
    #####for UVOT_image
    try:
        Image_URL = params['Image_URL']
        os.system('wget '+Image_URL+' '+fol+'/'+gcn_name+'/')
        gcn_img = fol+'/'+gcn_name+'/'+os.path.basename(root.attrib['Image_URL'])
        fits1 = fits.open(gcn_img)
        from astropy import wcs
        from astropy.coordinates import SkyCoord
        w = wcs.WCS(fits1[0].header)
        X_GRB = float(params['X_GRB'])
        Y_GRB = float(params['Y_GRB'])
        pixcrd = np.array([[X_GRB,Y_GRB],])
        world = w.wcs_pix2world(pixcrd, 1)
        ra = str(world[0][0])[:10]
        dec = str(world[0][1])[:10]
    except:
        pass
    #### return
    gcn_keys_list=['gcn_name', '_voname', 'gcn_time', 'grb_time', 'ra', 'dec', 'radius', 'fol', 'gcn_img', 'gcn_Packet_Type', 'Packet_Type', 'Sun_Distance', 'MOON_Distance', 'ds9_reg']
    gcn_keys={}
    for i in gcn_keys_list:
        key=str(i)
        try:
            #print(globals()[key])
            gcn_keys[key] = str(locals()[key])
        except:
            pass
    #gcn_keys={'gcn_name':gcn_name, 'ra':str(ra), 'dec':str(dec), 'fol':fol, 'gcn_img':gcn_img}
    print(gcn_keys)
    print('gcn_name = {:s}, ra = {:s}, dec = {:s}, radius = {:s}, Sun_Distance = {:s}, MOON_Distance = {:s}'.format(gcn_name, ra, dec, radius, Sun_Distance, MOON_Distance))
    with open('gcn.log','a') as gg:
        gg.write('"gcn_name" = "{:s}", "_voname" = "{:s}","gcn_time" = "{:s}", "grb_time" = "{:s}", "ra" = "{:s}", "dec" = "{:s}", "radius" = "{:s}", "Sun_Distance" = "{:s}", "MOON_Distance" = "{:s}","fol" = "{:s}"\n'.format(gcn_name, _voname, gcn_time, grb_time, ra, dec, radius, Sun_Distance, MOON_Distance, fol))
    visibility_keys = run_visibility.run_visibility(gcn_name, str(ra), str(dec), fol)
    identification_keys = run_identification.dsscut(gcn_name, grb_time, str(ra), str(dec), str(radius), fol )
    print(gcn_keys)
    email_keys=run_mail.send_email(gcn_keys, visibility_keys, identification_keys)



# Listen for VOEvents until killed with Control-C.
if __name__ == "__main__":
    __version__ = 1.1
    fol='workdir'
    os.system('mkdir '+fol)
    #gcn.listen(host='127.0.0.1',port=8099,handler=process_gcn)
    gcn.listen(handler=process_gcn)
