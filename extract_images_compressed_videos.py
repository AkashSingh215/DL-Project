#!/usr/bin/env python3
"""
github https://github.com/ondyari/FaceForensics/blob/master/dataset/extract_compressed_videos.py
script edited by Akash Singh, 19023, Data Sci. & Engineering, IISERB

Extracts facial image from key farmes in videos
"""
import os
from os.path import join
import argparse
import subprocess
import numpy as np
import cv2
from tqdm import tqdm


DATASET_PATHS = {
    # for FaceForencics++
    'original': 'original_sequences',
    'Deepfakes': 'manipulated_sequences/Deepfakes',
    'Face2Face': 'manipulated_sequences/Face2Face',
    'FaceSwap': 'manipulated_sequences/FaceSwap',
    'YouTube' : 'original_sequences/youtube',
    'FaceShifter': 'manipulated_sequences/FaceShifter',
    'NeuralTextures': 'manipulated_sequences/NeuralTextures',
    
    # Celeb-DF-v2
    'Celeb-real': 'Celeb-real',
    'YouTube-real': 'YouTube-real',
    'Celeb-synthesis': 'Celeb-synthesis'
}
COMPRESSION = ['c0', 'c23', 'c40','nc']  # 'nc' means no compression; it is used for Celeb-DF-v2 dataset

def extract_frames(data_path, output_path, video_name, method='cv2'):
    """Method to extract frames, either with ffmpeg or opencv. FFmpeg won't
    start from 0 so we would have to rename if we want to keep the filenames
    coherent."""
    os.makedirs(output_path, exist_ok=True)
    if method == 'ffmpeg':
        subprocess.check_output(
            'ffmpeg -i {} {}'.format(
                data_path, join(output_path, '%04d.png')),
            shell=True, stderr=subprocess.STDOUT)
    elif method == 'cv2':
        reader = cv2.VideoCapture(data_path)
        frame_num = 0
        while reader.isOpened():
            success, image = reader.read()
            if not success:
                break
            image_name = video_name +'--'+ str(frame_num)
            cv2.imwrite(join(output_path, '{}.png'.format(image_name)), image)
            frame_num += 1
        reader.release()
    else:
        raise Exception('Wrong extract frames method: {}'.format(method))

def extract_method_videos(data_path, dataset, compression):
    """Extracts all videos of a specified method and compression in different datasets"""
    if compression == 'nc' :  # i.e if celeb-df datasets
        videos_path = join(data_path, DATASET_PATHS[dataset])
        images_path = join('DataSet/extracted_Images/Celeb-DF', dataset)        
        
    else: # i.e for FaceForencics++ datasets
        videos_path = join(data_path, DATASET_PATHS[dataset], compression, 'videos')
        images_path = join('DataSet/extracted_Images/FakeImgDatasets', dataset)
    
    print('Saving extracted images in Directory : DataSet/extracted_Images/')
    os.makedirs(images_path, exist_ok=True)
    
    # to know how many videos get completely extracted
    fully_extracted_videos = []
    extracted_images = os.listdir(images_path) 
    if len(extracted_images) > 0:
        extracted_videos = []
        for images in (extracted_images): # here video has value like '999_008--45.png'
            video_name = images.split('--')[0] # has value like '999_008'
            extracted_videos.append(video_name)
        
        last_video = extracted_videos[-1]
        already_extracted_videos = list(set(extracted_videos))
        already_extracted_videos.remove(last_video)
        fully_extracted_videos = already_extracted_videos # fully extracted videos will be till 2nd last videos; since
        # it may happen that the last videos in extracted_videos is not fully extracted bec. code intruption by network error.
    
    all_videos = os.listdir(videos_path)
    for video in tqdm(all_videos): # here video has value like '999.mp4'
        video_name = video.split('.')[0] # has value like '999'
        if video_name not in fully_extracted_videos:
            extract_frames(join(videos_path, video),images_path,video_name)

if __name__ == '__main__':
    p = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    p.add_argument('--data_path', type=str)
    # eg. data_path for Celeb-DF-v2 will be 'DataSet/Celeb-DF-v2' & for FaceForencics++ 
    # will be : 'DataSet/FaceForencics++'. So pass acordingly.
    
    p.add_argument('--dataset', '-d', type=str,
                   choices=list(DATASET_PATHS.keys()) + ['all'],
                   default='all')
    p.add_argument('--compression', '-c', type=str, choices=COMPRESSION,
                   default='c0')
    args = p.parse_args()

    if args.dataset == 'all':
        for dataset in DATASET_PATHS.keys():
            args.dataset = dataset
            extract_method_videos(**vars(args))
    else:
        extract_method_videos(**vars(args))