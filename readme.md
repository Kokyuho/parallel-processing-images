# Satellite imagery parallel processing renderizations

Satellite imagery from the ESA Copernicus Sentinel 2 MSI instrument can be freely downloaded and used. Once we download an image product, corresponding with a certain world area and date taken, we will find in its containing folder the data corresponding to several spectral bands, each coming from different sensors able to perceive a certain wavelength and spacial resolution.

Each spectral band can be seen as a grey-scale image. A true color image can therefore be obtained combining the red, green and blue bands (RGB). However, many other combinations using e.g. infrared or ultraviolet bands can be used to obtain an image with certain interesting properties, such as cloud penetration or vegetation or water body detection. 

This example program lets the user choose the spacial resolution and the three bands to be combined to obtain the rendered image. Moreover, the user can give more than one combination. Then, the program will make use of parallel processing capabilities to process all the jobs and store the images in an output folder. A list with the filenames of the images will be returned. This behaviour is modelled as to be later possibly integrated with a REST API that provides the same inputs and recieves the outputs.

Install requirements:
1) Clone the repository.
2) Download and extract the following satellite image product in the same folder (large file, +900Mb): https://scihub.copernicus.eu/dhus/odata/v1/Products('bc88e6f3-7934-407a-82ab-2bbb26ec2cfe')/$value
3) Install dependencies (pip install -r requirements.txt)

Usage:
```
python main.py
```
