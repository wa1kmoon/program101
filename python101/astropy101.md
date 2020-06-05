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