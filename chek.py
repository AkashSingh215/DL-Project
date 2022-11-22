"""
Delete truncated images from FaceShifter and NeuralTextures.

"""
from PIL import Image
import os
from os.path import join
import shutil
import argparse
import subprocess
from tqdm import tqdm

DATASET_PATHS = {
    # for FaceForencics++
    'FaceShifter': 'FakeImgDatasets/FaceShifter',
    'NeuralTextures': 'FakeImgDatasets/NeuralTextures'
}

def delete_truncated_images(dataset,splt):
    data_path = 'DataSet/train_test_images_cropped'
    path = join(data_path, DATASET_PATHS[dataset],splt)
    all_imgs = os.listdir(path)
    for img in tqdm(all_imgs):
        imgpath = join(path,img)
        try:
            img = Image.open(imgpath)
            img.load()
        except OSError as error:
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
            delete_truncated_images(**vars(args))
    else:
        delete_truncated_images(**vars(args))