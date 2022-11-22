"""
Delete images with size 0.

"""
import os
from os.path import join
import shutil
import argparse
import subprocess
from tqdm import tqdm

DATASET_PATHS = {
    # for FaceForencics++
    'Deepfakes': 'FakeImgDatasets/Deepfakes',
    'Face2Face': 'FakeImgDatasets/Face2Face',
    'FaceSwap': 'FakeImgDatasets/FaceSwap',
    'YouTube' : 'FakeImgDatasets/YouTube',
    'FaceShifter': 'FakeImgDatasets/FaceShifter',
    'NeuralTextures': 'FakeImgDatasets/NeuralTextures',
    
    # Celeb-DF-v2
    'Celeb-real': 'Celeb-DF/Celeb-real',
    'YouTube-real': 'Celeb-DF/YouTube-real',
    'Celeb-synthesis': 'Celeb-DF/Celeb-synthesis'
}

def delete_zerosize_images(dataset,splt):
    data_path = 'DataSet/train_test_images_cropped'
    path = join(data_path, DATASET_PATHS[dataset],splt)
    all_imgs = os.listdir(path)
    for img in tqdm(all_imgs):
        imgpath = join(path,img)
        if os.path.getsize(imgpath) == 0:    # Size (In bytes)
            os.remove(imgpath)
    

if __name__ == '__main__':
    p = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    p.add_argument('--dataset', '-d', type=str,
                   choices=list(DATASET_PATHS.keys()) + ['all'],
                   default='all')
    p.add_argument('--splt', type=str)
    # splt has value train or test or valid
    args = p.parse_args()

    if args.dataset == 'all':
        for dataset in DATASET_PATHS.keys():
            args.dataset = dataset
            delete_zerosize_images(**vars(args))
    else:
        delete_zerosize_images(**vars(args))