#!/usr/bin/env python3
"""
Extracts facial image from key farmes in videos

"""
import os
from os.path import join
import argparse
import subprocess
import numpy as np
import cv2
import dlib # Automatic face tracking library
from tqdm import tqdm


DATASET_PATHS = {
    # for FaceForencics++
    'Deepfakes': 'FaceForencics++/manipulated_sequences/Deepfakes',
    'Face2Face': 'FaceForencics++/manipulated_sequences/Face2Face',
    'FaceSwap': 'FaceForencics++/manipulated_sequences/FaceSwap',
    'FaceShifter': 'FaceForencics++/manipulated_sequences/FaceShifter',
    'NeuralTextures': 'FaceForencics++/manipulated_sequences/NeuralTextures',
    'YouTube' : 'FaceForencics++/original_sequences/youtube',
    
    # Celeb-DF-v2
    'Celeb-real': 'Celeb-DF-v2/Celeb-real',
    'YouTube-real': 'Celeb-DF-v2/YouTube-real',
    'Celeb-synthesis': 'Celeb-DF-v2/Celeb-synthesis'
}
COMPRESSION = ['c0', 'c23', 'c40','nc']  # 'nc' means no compression; it is used for Celeb-DF-v2 dataset

face_detector = dlib.get_frontal_face_detector() # instantiating face detector class from dlib library

def get_boundingbox(face, width, height, scale=1.3, minsize=None):
    """
    Expects a dlib face to generate a quadratic bounding box.
    :param face: dlib face class
    :param width: frame width
    :param height: frame height
    :param scale: bounding box size multiplier to get a bigger face region
    :param minsize: set minimum bounding box size
    :return: x, y, bounding_box_size in opencv form
    """
    x1 = face.left() # Taking lines numbers around face
    y1 = face.top()
    x2 = face.right()
    y2 = face.bottom()
    size_bb = int(max(x2 - x1, y2 - y1) * scale) # scaling size of box to 1.3
    if minsize:
        if size_bb < minsize:
            size_bb = minsize
    center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2

    # Check for out of bounds, x-y top left corner
    x1 = max(int(center_x - size_bb // 2), 0)
    y1 = max(int(center_y - size_bb // 2), 0)
    # Check for too big bb size for given x, y
    size_bb = min(width - x1, size_bb)
    size_bb = min(height - y1, size_bb)

    return x1, y1, size_bb

def extract_frames(data_path, output_path, video_name, method='cv2'):
    """Method to extract frames, either with ffmpeg or opencv. FFmpeg won't
    start from 0 so we would have to rename if we want to keep the filenames
    coherent."""
    if method == 'ffmpeg':  # this sec. needs editing. I am only considering CV2 so i changed  in cv2 sec only.
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
            
        # =========== Face detection  ====================
               
            # assuming each frame image has only 1 face
            height, width = image.shape[:2]  # original image shape
            try: # If face is detected at any frame 
                # returns bounding box having cord.(left,top,right,bottom) of detected face.
                face = face_detector(image, 1)[0]   # 1 is for upscaling
                x, y, size = get_boundingbox(face=face, width=width, height=height) # Calling to get bound box around the face
            except IndexError:  # If in case face is not detected at any frame
                continue
            cropped_img = image[y:y+size, x:x+size] # cropping the face
            image_name = video_name +'--'+ str(frame_num)
            cv2.imwrite(join(output_path, '{}.png'.format(image_name)), cropped_img) # saving the cropped image
            frame_num += 1
        reader.release()
    else:
        raise Exception('Wrong extract frames method: {}'.format(method))



def extract_method_videos(dataset, start, end, compression):
    """Extracts all videos of a specified method and compression in the
    DataSet file structure"""
    data_path = 'DataSet'
    if compression == 'nc' :  # i.e if celeb-df datasets
        videos_path = join(data_path, DATASET_PATHS[dataset])
        images_path = join('DataSet/Images_cropped/Celeb-DF', dataset)        
        
    else:
        videos_path = join(data_path, DATASET_PATHS[dataset], compression, 'videos')
        images_path = join('DataSet/Images_cropped/FakeImgDatasets', dataset)
    
    print('Saving facial images in Directory : DataSet/Images_cropped/')
    start = int(start)
    end = int(end)
    
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

    all_videos = os.listdir(videos_path)[start:end]
    for video in tqdm(all_videos): # here video has value like '999.mp4'
        video_name = video.split('.')[0] # has value like '999'
        if video_name not in fully_extracted_videos:
            extract_frames(join(videos_path, video),images_path,video_name)
            
        
if __name__ == '__main__':
    p = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    p.add_argument('--start', type=str)
    p.add_argument('--end', type=str)
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