import os
import numpy as np
from datetime import datetime
from multiprocessing import Process
from PIL import Image, ImageEnhance

def renderImage(i, res_list, r_list, g_list, b_list, imagePath):

    # Get res in path
    imagePathRes = imagePath + 'R' + res_list[i] + 'm/'

    # Import bands
    print(f'Starting job {i+1} of {len(res_list)}...')
    bandR = Image.open(imagePathRes + 'T29TQH_20210605T110619_' + r_list[i] + '_' + res_list[i] + 'm.jp2')
    bandG = Image.open(imagePathRes + 'T29TQH_20210605T110619_' + g_list[i] + '_' + res_list[i] + 'm.jp2')
    bandB = Image.open(imagePathRes + 'T29TQH_20210605T110619_' + b_list[i] + '_' + res_list[i] + 'm.jp2')

    print(f'Bands read. Rendering image {i+1} of {len(res_list)}...')

    # We divide by 2^8 to transform from uint16 to uint8 range
    b_r = np.asarray(bandR)/256
    b_g = np.asarray(bandG)/256
    b_b = np.asarray(bandB)/256

    # We assemble the combined color rgb image
    RGB_gt = np.zeros([len(b_r), len(b_r[0]), 3], np.uint8)
    RGB_gt[:, :, 0] = b_r
    RGB_gt[:, :, 1] = b_g
    RGB_gt[:, :, 2] = b_b

    # Get pillow object again and increase brightness
    RGB_gt = Image.fromarray(RGB_gt)
    enhancer = ImageEnhance.Brightness(RGB_gt)
    factor = 10
    im_output = enhancer.enhance(factor)

    # Crop area of interest
    im_crop = im_output.crop((im_output.size[0]*1/4, im_output.size[1]*2/7, im_output.size[0]*3/4, im_output.size[1]*5/7))

    # Get datetime now
    now = datetime.now().strftime('%Y%m%d-%H%M%S')   
    im_crop.save(f'./Output/{now}_R{res_list[i]}m_{r_list[i]}_{g_list[i]}_{b_list[i]}.jpg')

    print(f'Done job {i+1} of {len(res_list)}...')

if __name__ == '__main__':

    # Get user input (or API)
    res_list, r_list, g_list, b_list = ([] for i in range(4))
    res, r, g, b = ('' for i in range(4))
    pendingInput = True
    while pendingInput:

        while res not in ('10', '20', '60'):
            res = input('Input spacial resolution (10, 20 or 60):')

            if res == '10':
                res_list.append(res)
                accepted_list = ('B02', 'B03', 'B04', 'B08') 
                while r not in accepted_list:
                    r = input(f'Input R band {accepted_list}:')
                r_list.append(r)
                while g not in accepted_list:
                    g = input(f'Input G band {accepted_list}:')
                g_list.append(g)
                while b not in accepted_list:
                    b = input(f'Input B band {accepted_list}:')
                b_list.append(b)

            elif res == '20':
                res_list.append(res)
                accepted_list = ('B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B8A', 'B11', 'B12')
                while r not in accepted_list:
                    r = input(f'Input R band {accepted_list}:')
                r_list.append(r)
                while g not in accepted_list:
                    g = input(f'Input G band {accepted_list}:')
                g_list.append(g)
                while b not in accepted_list:
                    b = input(f'Input B band {accepted_list}:')
                b_list.append(b)

            elif res == '60':
                res_list.append(res)
                accepted_list = ('B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B8A', 'B09', 'B11', 'B12')
                while r not in accepted_list:
                    r = input(f'Input R band {accepted_list}:')
                r_list.append(r)
                while g not in accepted_list:
                    g = input(f'Input G band {accepted_list}:')
                g_list.append(g)
                while b not in accepted_list:
                    b = input(f'Input B band {accepted_list}:')
                b_list.append(b)

            else:
                print("ERROR: Spacial resolution not valid.")

        answer = input("Do you want to add another job? (y/n):")
        if answer in ('y', 'Y'):
            res, r, g, b = ('' for i in range(4))
        else:
            pendingInput = False

    # Define image path
    imagePath = './S2B_MSIL2A_20210605T110619_N0300_R137_T29TQH_20210605T143100.SAFE/GRANULE/L2A_T29TQH_A022185_20210605T111526/IMG_DATA/'

    # Check if Output folder exists, else create it
    if not os.path.exists('./Output'):
        os.makedirs('Output')

    processes = []
    for i in range(len(res_list)):
        p = Process(target=renderImage, args=[i, res_list, r_list, g_list, b_list, imagePath])
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    print("Done batch job.")

# 3) Implement parallel processing of this jobs for batches.
# 4) Integrate with Django REST API
