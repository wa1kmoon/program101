#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 21:53:31 2020

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

####### setting
ram='raMean' #23
decm='decMean' #24
ra_err='raMeanErr' # 25
dec_err='decMeanErr' # 26
gm='gMeanPSFMag' # 45
gm_err='gMeanPSFMagErr' #46
rm='rMeanPSFMag' #61
rm_err='rMeanPSFMagErr'#62
im='iMeanPSFMag' #77
im_err='iMeanPSFMagErr' #78
zm='zMeanPSFMag' #93
zm_err='zMeanPSFMagErr' #94
ym='yMeanPSFMag' #99
ym_err='yMeanPSFMagErr' #100
Rm='Rm'
Rm_err='Rm_err'
Im='Im'
Im_err='Im_err'
mykey=['ALPHA_J2000','DELTA_J2000','MAG_AUTO','MAGERR_AUTO','MAG_BEST','MAGERR_BEST','ELLIPTICITY']
#mykey=['ALPHA_J2000','DELTA_J2000','MAG_A','MAGERR_']
#mytuo=0.3
#ymag_err=0.1
mm=rm
mm_err=rm_err
rmag=[14.5,18]
rmag_err=0.1
#s_head='0'
#####
# R=r-0.2936*(r-i)-0.1439 sigma=0.0072
#######################################3333

def rdb(dbname):
    global db_head
    globals()
    #print(my_head)
    db=open(dbname)
    db_p=db.tell()
    #db.seek(0,0)
    db_data= csv.reader(db) #得到可迭代的星表数据，每一项都是星表中的一行数据的列表形式
    result=[]
    db_head=re.split('[,|\n]',db.readline()) #得到星表表头列表
    #print(db.readline())
    headlist=[]
    dblen=0
    try :
        global my_head
    except SyntaxWarning:
        pass
    print(mm)
    if mm == 'Rm': #若标注R波段星等：
        my_head=[ram,decm,rm,rm_err,im,im_err]
        for i in my_head :
            headlist.append(db_head.index(i))
        print(db_head)
        print(my_head,'\n',headlist)
        headlog=0
        for once in db_data:
            dblen=dblen+1
            headlog=headlog+1
            #print(once)
            try:
                if rmag[0] < float(once[headlist[2]]) < rmag[1] : #若星表r星等在规定范围内：
                    if 0 < float(once[headlist[3]]) < rmag_err : #若星表r误差在规定范围内：
                        if float(once[headlist[4]]) > 0: #若星表i星等存在（大于0）：由r星等和i星等计算R星等
                            r_once=float(once[headlist[2]])
                            i_once=float(once[headlist[4]])
                            R_once=r_once-0.2936*(r_once-i_once)-0.1439 # r转化成R
                            R_err=float(once[headlist[3]])
                            one=[float(headlog),float(once[headlist[0]]),float(once[headlist[1]]),R_once,R_err] 
                            #得到一颗数据库中被选中的星的序数，坐标，R星等及误差的一行列表
                        else: #若星表i星等不存在(-999)，则用粗略公式把r星等转化为R星等
                            continue
                            one=[float(headlog)]
                            for j in headlist[0:4]:
                                one.append(float(once[int(j)]))
                            one[2]=one[2]-0.2 # r转化成R
                        result.append(one) #星表的一行读取完毕，将所需的结果列表添加到总的结果列表中
            except:
                pass
    elif mm == 'Im': #同上
        my_head=[ram,decm,im,im_err,rm,rm_err]
        for i in my_head :
            headlist.append(db_head.index(i))
        #print(db_head)
        print(my_head,'\n',headlist)
        headlog=0
        for once in db_data:
            dblen=dblen+1
            headlog=headlog+1
            #print(once)
            try:
                if rmag[0] < float(once[headlist[2]]) < rmag[1] : 
                    if 0 < float(once[headlist[3]]) < rmag_err :
                        if  float(once[headlist[4]]) > 0  :
                            i_once=float(once[headlist[2]])
                            r_once=float(once[headlist[4]])
                            I_once=r_once-1.2444*(r_once-i_once)-0.3820
                            I_err=float(once[headlist[3]])
                            one=[float(headlog),float(once[headlist[0]]),float(once[headlist[1]]),I_once,I_err]
                        else:
                            continue
                            one=[float(headlog)]
                            for j in headlist[0:4]:
                                one.append(float(once[int(j)]))
                            one[2]=one[2]-0.45
                        result.append(one)
            except:
                pass
    else:#如果是其它波段，同上
        my_head=[ram,decm,mm,mm_err]
        #print(my_head)
        for i in my_head :
            headlist.append(db_head.index(i))
        #print(db_head)
        print(my_head,'\n',headlist)
        headlog=1
        for once in db_data:
            dblen=dblen+1
            #print(once)
            try:
                if rmag[0] < float(once[headlist[2]]) < rmag[1] :
                    if 0 < float(once[headlist[3]]) < rmag_err :
                        one=[float(headlog)]
                        for j in headlist: #得到星表一行中所需的坐标，星等以及星等误差
                            one.append(float(once[int(j)]))
                        #print(one)
                        result.append(one)
                headlog=headlog+1
            except:
                pass
    result=random.sample(result,min(30,len(result)))
    db.close()
    print('db : ',len(result),' / ',dblen)
    return np.array(result) #将总结果列表转换成numpy数组并返回

'''
Get a cutout of the region from DSS survey and create a simple FC
To be checked in case the image is not available in PanSTARRS
'''
def dsscut(name,time,ra,dec,radius,fol):

    plt.rc('text', usetex=False)
    plt.rc('font', family='serif') #设定字体
    #
    # basic parameters, can be changed in principle
    #
    size=5 # [arcmin] the size of the retrieved and saved image
    size1=5 # [arcmin] the size of the image used for the FC
    pix=1.008 # approx pixel scale
    #
    # get the cutout image from the ESO archive
    #
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
    try:
        #with urllib.request.urlopen(link) as response, open(outf, 'wb') as outf:
        response, outf = urllib.request.urlopen(link), open(outf_path, 'wb') #返回一个reponse对象，保存网页信息；新建fits文件
        shutil.copyfileobj(response, outf) #将网页内容复制到上一步新建的fits文件
        print('\t... image saved to:', outf_path)

        #
        # load image and make a FC
        #
        fh=fits.open(outf_path)

        

        fim = fh[0].data
        fhe = fh[0].header

        #
        # cut image and apply scale
        #
        imsize_list=[10,]
        if ( float(radius)*120 < 3 ):
            imsize_list.append(3)
        for imsize in imsize_list:
            size1=imsize
            x1=int(30*(size - size1))
            x2=int(30*(size + size1))
            y1=int(30*(size - size1))
            y2=int(30*(size + size1))
            fim=fim[y1:y2,x1:x2]

            fim[np.isnan(fim)] = 0.0
            transform = AsinhStretch() + PercentileInterval(99.7)
            bfim = transform(fim)

            with warnings.catch_warnings():    #because there are deprecated keywords in the header, no need to write it out
                warnings.simplefilter("ignore")
                global wcs
                wcs = WCS(fhe)

            #
            # produce and save the FC
            #
            fig=plt.figure(2,figsize=(5,5))
            fig1=fig.add_subplot(111,aspect='equal')
            plt.imshow(bfim,cmap='gray_r',origin='lower')
            s_world = wcs.wcs_world2pix(np.array([[float(ra),float(dec)],]), 1)[0]
            theta = np.linspace(0, 2*np.pi,8000) #???
            x, y =  s_world[0]-x1+np.cos(theta)*float(radius)*3600, s_world[1]-y1+np.sin(theta)*float(radius)*3600 #???
            fig1.plot(x, y, color='red', linewidth=0.5)
            try: #先尝试下载panstarrs星表
                os.system('wget -nd -nc "https://catalogs.mast.stsci.edu/api/v0.1/panstarrs/dr1/mean?ra='+str(raS)+'&amp;dec='+str(decS)+'&radius='+str((size)/120.)+'&nDetections.gte=1&amp&pagesize=50001&format=csv"  ')
                os.system('mv ./mean\?ra\='+str(raS)+'\&amp\;dec\='+str(decS)+'\&radius\='+str(size/120.)+'\&nDetections.gte\=1\&amp\&pagesize\=50001\&format\=csv  ./'+str(csv_outf))
                print('1')
                db_data = rdb(csv_outf)
                print('2')
                #sextab = make_asc_runsex(outf_path)
                print(len(db_data))
                for i in db_data: #在FC上标星等
                    db_ra = i[1]
                    db_dec = i[2]
                    db_mag = format(i[3], '0.2f')
                    db_world = wcs.wcs_world2pix(np.array([[float(db_ra),float(db_dec)],]), 1)[0]
                    fig1.text(db_world[0]-x1, db_world[1]-y1, str(db_mag), color='green', fontsize=7)
                    #print(db_world)
                    #fig1.plot(db_world[0], db_world[1], color='red', linewidth=0.5)
                    #fig.text(db_world[0]/(size*60.),db_world[1]/(size*60.),str(format(db_mag, '0.2f')),fontsize=5,color='green')
                #txtb=fig.text(0.06, 0.06, mm, fontsize=10, color='black')
                #txtb.set_path_effects([PathEffects.withStroke(linewidth=0.1, foreground='k')])
            except: #如果panstarrs星表下载失败，尝试下载skymapper星表（skymapper数据主要是南天的）
                try:
                    os.system('wget -nd -nc "http://skymapper.anu.edu.au/sm-cone/public/query?RA='+str(raS)+'&DEC='+str(decS)+'&SR='+str((size)/120.)+'&format=csv"  ')
                    os.system('mv ./query\?RA\='+str(raS)+'\&DEC\='+str(decS)+'\&SR\='+str(size/120.)+'\&format\=csv  ./'+str(csv_outf))
                    #skymapper keys
                    globals()['ram'] = 'raj2000'
                    globals()['ra_err'] = 'e_raj2000'
                    globals()['decm'] = 'dej2000'
                    globals()['dec_err'] = 'e_dej2000'
                    # u g r i z
                    globals()['mm'] = 'r_psf'
                    globals()['mm_err'] = 'e_r_psf'
                    print('1')
                    db_data = rdb(csv_outf)
                    print('2')
                    #sextab = make_asc_runsex(outf_path)
                    print(len(db_data))
                    for i in db_data:
                        db_ra = i[1]
                        db_dec = i[2]
                        db_mag = format(i[3], '0.2f')
                        db_world = wcs.wcs_world2pix(np.array([[float(db_ra),float(db_dec)],]), 1)[0]
                        fig1.text(db_world[0]-x1, db_world[1]-y1, str(db_mag), color='green', fontsize=7)
                except:
                    txtb=fig.text(0.45,0.06,'NO Panstarrs AND skymapper',fontsize=10,color='black')
            fig2=plt.axes([0.0, 0.0, 0.4, 0.12]) #在fig的左下角画一个小框，里面写GRB的信息（时间，坐标，图像视场等）
            fig2.set_facecolor('w')
            txta=fig.text(0.02,0.08,'GRB'+time+'  DSS '+str(imsize)+'\' x '+str(imsize)+'\'',fontsize=7,color='black')
            txta=fig.text(0.5,0.95,'N',fontsize=18,color='black')
            txta=fig.text(0.01,0.5,'E',fontsize=18,color='black')
            txta=fig.text(0.02,0.05,'GRB   ra = '+ra_hms+' ('+raS+')',fontsize=7,color='black')
            txta=fig.text(0.02,0.02,'GRB dec = '+dec_dms+' ('+decS+')',fontsize=7,color='black')
            #txta.set_path_effects([PathEffects.withStroke(linewidth=0.1, foreground='k')])
            #txtb=fig.text(0.9,0.95,'DSS',fontsize=10,color='black')
            #txtb.set_path_effects([PathEffects.withStroke(linewidth=0.1, foreground='k')])
            fig1.add_patch(FancyArrowPatch((size1*60-70-10,20),(size1*60-10,20),arrowstyle='-',color='k',linewidth=1.5))
            #fig1.add_patch(FancyArrowPatch((size1*60-15/pix-10,20),(size1*60-10,20),arrowstyle='-',color='black',linewidth=2.0))
            txtc=fig.text(0.9,0.06,'60\'\'',fontsize=10,color='black')
            txtc.set_path_effects([PathEffects.withStroke(linewidth=0.1, foreground='k')])
            #plt.gca().xaxis.set_major_locator(plt.NullLocator())
            #plt.gca().yaxis.set_major_locator(plt.NullLocator())
            #fig2=plt.axes([0.0, 0.64, 0.1, 0.65])
            #lena = mpimg.imread('a.jpg')
            #lena.shape #(512, 512, 3)
            #plt.imshow(lena)
            plt.gca().xaxis.set_major_locator(plt.NullLocator())
            plt.gca().yaxis.set_major_locator(plt.NullLocator())
            plt.subplots_adjust(top=1,bottom=0,left=0,right=1,hspace=0,wspace=0)
            globals()['fname'+str(imsize)]=name+str(imsize)+'_dss.png'
            plt.savefig(fol+'/'+name+'/'+globals()['fname'+str(imsize)],dpi=300,format='PNG')
            fig.clear()

        if ( float(radius)*120 < 3 ):
            return {'pngname10':fol+'/'+name+'/'+globals()['fname10'], 'pngname3':fol+'/'+name+'/'+globals()['fname3'], 'dssname':outf_path, 'dsslink':link}
        else:
            return {'pngname10':fol+'/'+name+'/'+globals()['fname10'], 'dssname':outf_path, 'dsslink':link}


    except Exception as e:
        print(str(e))
        return {'dss_err':'-99','dsslink':link}



if __name__ == "__main__":
    name='test'
    time='191106.584'
    ra='198.5560'
    dec='11.2698'
    radius='0.0003'
    #radius='0.0015'
    fol='./'
    # identification_keys = dsscut(name,time,ra,dec,radius,fol)
    # print(identification_keys)

