# astropy notebook

- 使用astropy更改关键字的值

    ```py
    from astropy.io import fits
    fits_file='1.fits'
    fits.setval(fits_file, 'TELESCOP', value='xl216')
    # or, if something goes wrong, do as following
    with fits.open(output,mode='update') as comp:
        comp[0].header['COVERFRA'] = frac
        comp.flush()
    ```


- 如何打开本地fits图像：

    ```python
    from astropy.io import fits
    _dataimg, _hdr = fits.getdata(_img+'.fits', header=True)
    ```

- 如何打开本地fits图像，查看图像层数，并将图像变成一层？ & 如何创建新的fits图像并写如数据?

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
    >>> c1 = SkyCoord(ra1,dec1, unit=(u.hourangle, u.deg))## 时分秒,度分秒格式
    >>> c2 = SkyCoord(ra=11*u.degree, dec=10*u.degree, frame='fk5')
    >>> c1.separation(c2)  # Differing frames handled correctly  
    <Angle 1.40453359 deg>
    >>> dist = (c1.separation(c2)*u.degree).value #float value in degree
    ```

- write table to fits file

    ```python
    from astropy.table import Table
    t = Table([[1, 2], [4, 5], [7, 8]], names=('a', 'b', 'c'))
    t.write('table1.fits', format='fits')
    ```

- 读取fits table文件

    ```python
    >>> from astropy.table import Table
    >>> psfcat=Table.read('ztf_20180327208819_000841_zg_c06_o_q1_psfcat.fits')
    >>> psfcat.info()

    <Table length=1989>
    name    dtype  unit
    -------- ------- ----
    sourceid   int32     
        xpos float32  pix
        ypos float32  pix
        ra float64  deg
        dec float64  deg
        flux float32   DN
    sigflux float32   DN
        mag float32  mag
    sigmag float32  mag
        snr float32     
        chi float32     
    sharp float32

    # Create a table
    >>> from astropy.table import QTable
    >>> import astropy.units as u
    >>> import numpy as np

    >>> a = np.array([1, 4, 5], dtype=np.int32)
    >>> b = [2.0, 5.0, 8.5]
    >>> c = ['x', 'y', 'z']
    >>> d = [10, 20, 30] * u.m / u.s

    >>> t = QTable([a, b, c, d],
    ...            names=('a', 'b', 'c', 'd'),
    ...            meta={'name': 'first table'})

    # Access the data by column or row using familiar numpy structured array syntax:
    >>> t['a']       # Column 'a'
    <Column name='a' dtype='int32' length=3>
    1
    4
    5

    >>> t['a'][1]    # Row 1 of column 'a'
    4

    >>> t[1]         # Row object for table row index=1
    <Row index=1>
    a      b     c      d
                        m / s
    int32 float64 str1 float64
    ----- ------- ---- -------
        4   5.000    y    20.0


    >>> t[1]['a']    # Column 'a' of row 1
    4

    # You can retrieve a subset of a table by rows (using a slice) or by columns (using column names), where the subset is returned as a new table:
    >>> print(t[0:2])      # Table object with rows 0 and 1
    a     b     c    d
                    m / s
    --- ------- --- -----
    1   2.000   x  10.0
    4   5.000   y  20.0


    >>> print(t['a', 'c'])  # Table with cols 'a', 'c'
    a   c
    --- ---
    1   x
    4   y
    5   z

    # Modifying a Table in place is flexible and works as you would expect:
    >>> t['a'][:] = [-1, -2, -3]    # Set all column values in place
    >>> t['a'][2] = 30              # Set row 2 of column 'a'
    >>> t[1] = (8, 9.0, "W", 4 * u.m / u.s) # Set all row values
    >>> t[1]['b'] = -9              # Set column 'b' of row 1
    >>> t[0:2]['b'] = 100.0         # Set column 'b' of rows 0 and 1
    >>> print(t)
    a     b     c    d
                    m / s
    --- ------- --- -----
    -1 100.000   x  10.0
    8 100.000   W   4.0
    30   8.500   z  30.0

    # Replace, add, remove, and rename columns with the following:
    >>> t['b'] = ['a', 'new', 'dtype']   # Replace column b (different from in-place)
    >>> t['e'] = [1, 2, 3]               # Add column d
    >>> del t['c']                       # Delete column c
    >>> t.rename_column('a', 'A')        # Rename column a to A
    >>> t.colnames
    ['A', 'b', 'd', 'e']

    # Adding a new row of data to the table is as follows. 

    >>> t.add_row([-8, 'string', 10 * u.cm / u.s, 10])
    >>> len(t)
    4
    ```

- 如何查询某坐标的消光值？
  > 与astropy无关,来源为杨圣师兄的pstools程序。
  ```python
    def query_ebv(ra,dec,size=2,thresh=.25,verbose=False):
        """
        Take ra,dec and return the E(B-V) number
        URL query, see https://irsa.ipac.caltech.edu/applications/DUST
        """
        import urllib2
        import xmltodict
        url = "https://irsa.ipac.caltech.edu/cgi-bin/DUST/nph-dust?"
        url += "locstr=%.2f+%.2f+equ+j2000"%(ra,dec)
        if size<2:size=2
        if size>37.5:size=37.5
        url += '&regSize=%.2f'%size # size between 2.0 and 37.5    

        _file = urllib2.urlopen(url)
        data = _file.read()
        _file.close()

        _dict = xmltodict.parse(data)
        _ebv = _dict['results']['result'][0]['statistics']['meanValueSFD']

        ebvalue = float(_ebv.split('(mag)')[0])
        if ebvalue<thresh:
            if verbose:
                print("ra=%.2f dec=%.2f:\tebv=%.2f\tOK"%\
                    (ra,dec,float(_ebv.split('(mag)')[0])))
            return ebvalue
        else:
            if verbose:
                print("ra=%.2f dec=%.2f:\tebv=%.2f\tNo"%\
                    (ra,dec,float(_ebv.split('(mag)')[0])))
            return
  ```

- 如何计算大致月相？
  > 与astropy无关,来源为杨圣师兄的pstools程序pstdef模块。
  ```python
    def moon_phase(month, day, year):
        ages = [18, 0, 11, 22, 3, 14, 25, 6, 17, 28, 9, 20, 1, 12, 23, 4, 15, 26, 7]
        offsets = [-1, 1, 0, 1, 2, 3, 4, 5, 7, 7, 9, 9]
        description = ["new (totally dark)",
        "waxing crescent (increasing to full)",
        "in its first quarter (increasing to full)",
        "waxing gibbous (increasing to full)",
        "full (full light)",
        "waning gibbous (decreasing from full)",
        "in its last quarter (decreasing from full)",
        "waning crescent (decreasing from full)"]
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        if day == 31:day = 1
        days_into_phase = ((a2ges[(year + 1) % 19] +
                            ((day + offsets[month-1]) % 30) +
                            (year < 1900)) % 30)
        index = int((days_into_phase + 2) * 16/59.0)  # 月相
        if index > 7:index = 7
        status = description[index]
        # light should be 100% 15 days into phase
        # 计算当前日期月相百分比
        light = int(2 * days_into_phase * 100/29)
        if light > 100:
            light = abs(light - 200)
        date = "%d%s%d" % (day, months[month-1], year)
        return date, status, light
  ```
