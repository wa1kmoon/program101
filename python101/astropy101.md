# astropy notebook

- 使用astropy更改关键字的值

    ```py
    from astropy.io import fits
    fits_file='1.fits'
    fits.setval(fits_file, 'TELESCOP', value='xl216')
    ```

- 如何打开本地fits图像：

    ```python
    from astropy.io import fits
    _dataimg, _hdr = fits.getdata(_img+'.fits', header=True)
    ```

- 如何打开本地fits图像，查看图像层数，并将图像变成一层？

    ```python
    from astropy.io import fits
    fitsfile=fits.open('1.fits')
    fitsfile.info()
    data=fitsfile[0].data
    header=fitsfile[0].header
    fits.writeto('1.new.fits',data,header=header)
    ```

- 如何创建一个新的fits头文件并往其中添加内容？

    ```python
    hdulist=fits.open(fitsfile)
    wcshdr=fits.Header()

    for key in hdulist[0].header:
        if ('CTYPE' in key) or ('CRVAL' in key) or ('CRPIX' in key) or ('CD' in key and '_' in key) or ('NAXIS' in key): 
            wcshdr[key]=(hdulist[0].header[key],hdulist[0].header.comments[key])
    ```

- 如何用另一个np.array替换原图象中的数据？

    ```python
    from astropy.io import fits
    import numpy as np

    with fits.open('1.1.fits', mode='update') as new:
        data = new[0].data
        datapos = np.maximum(data,0)
        new[0].data = datapos
        
        new.flush()
    ```

- how to draw 3D figure from fits image?

    ```python
    from astropy.io import fits
    import numpy as np
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import pyplot as plt


    refim = '2.1.fits'
    refdata = fits.getdata(refim)
    size = refdata.shape

    fig = plt.figure(figsize=(10,10))
    #ax = fig.add_subplot(111, projection='3d')
    ax=fig.gca(projection='3d') 
    ax.view_init(elev=0., azim=270.) #adjust view angle. elev: around x axis; azim: around z axis

    x = np.arange(0,size[1],1)
    y = np.arange(0,size[0],1)
    X,Y = np.meshgrid(x,y)

    ax.plot_surface(X,Y,refdata)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.savefig('3d.png',dpi=100)
    plt.show()
    ```

- 求两点距离

```python
>>> from astropy import units as u
>>> from astropy.coordinates import SkyCoord

>>> c1 = SkyCoord(ra=10*u.degree, dec=9*u.degree, distance=10*u.pc, frame='icrs')
>>> c2 = SkyCoord(ra=11*u.degree, dec=10*u.degree, distance=11.5*u.pc, frame='icrs')
>>> c1.separation_3d(c2)  
<Distance 1.52286024 pc>

>>> c1 = SkyCoord(ra=10*u.degree, dec=9*u.degree, frame='icrs')
>>> c2 = SkyCoord(ra=11*u.degree, dec=10*u.degree, frame='fk5')
>>> c1.separation(c2)  # Differing frames handled correctly  
<Angle 1.40453359 deg>
>>> dist = (c1.separation(c2)*u.degree).value #float value in degree
```