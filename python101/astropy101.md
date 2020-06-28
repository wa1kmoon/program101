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
