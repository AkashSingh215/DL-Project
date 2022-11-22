"""
Divide images into train test and valid

"""
import random
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

def train_test_split(dataset):
    data_path = 'DataSet/Images_cropped'
    images_folder = join(data_path, DATASET_PATHS[dataset])
    all_images = os.listdir(images_folder)
    unique_videos = [e for e in set(i.split('--')[0] for i in all_images)] # every run will have diff. order bec. of set()
    # to fix the order in ascending order
    unique_videos.sort()  # it will change unique_videos with its sorted version
    #unique_videos_copy = unique_videos.copy()
    random.seed(2)   # it will make sure that the order of shuffling remains fixed in any run
    random.shuffle(unique_videos) # it will change unique_videos with its shuffled version
    
    print('Saving train_test_images in Directory : DataSet/train_test_images/')
    if dataset in ['Celeb-real','YouTube-real','Celeb-synthesis'] :  # i.e if celeb-df datasets
        # testing videos names
        if dataset == 'Celeb-real':
            unique_videos_testing = unique_videos[0:108]
            unique_videos_training = unique_videos[108:]

        if dataset == 'YouTube-real' : 
            unique_videos_testing = unique_videos[0:69]
            unique_videos_training = unique_videos[69:]

        if dataset == 'Celeb-synthesis' :
            unique_videos_testing = unique_videos[0:340]
            unique_videos_training = unique_videos[340:]
            
            
        # training and testing
        for i in [0,1]:
            if i == 0: # training
                unique_videos_tvt = unique_videos_training
                images_path_tvt = join('DataSet/train_test_images_cropped/Celeb-DF', dataset, 'train')

            else : # testing
                unique_videos_tvt = unique_videos_testing
                images_path_tvt = join('DataSet/train_test_images_cropped/Celeb-DF', dataset, 'test')

            if not os.path.exists(images_path_tvt):
                os.makedirs(images_path_tvt)
            
            # to know how many videos get completely splitted
            fully_extracted_videos = []
            extracted_images = os.listdir(images_path_tvt) 
            if len(extracted_images) > 0:
                extracted_videos = []   # video names with duplicates which has been splitted in train test
                for images in (extracted_images): # here image has value like '999_008--45.png'
                    video_name = images.split('--')[0] # has value like '999_008'
                    extracted_videos.append(video_name)                        
                
                last_video = extracted_videos[-1]
                already_extracted_videos = list(set(extracted_videos)) # unique video names which has been splitted in train test
                already_extracted_videos.remove(last_video)
                fully_extracted_videos = already_extracted_videos # fully splitted videos will be till 2nd last videos
            
            for vid in tqdm(unique_videos_tvt):
                if vid not in fully_extracted_videos:
                    for img in all_images:
                        if vid in img: # checking vid substring is in string img or not
                            ip_img_path = join(data_path, DATASET_PATHS[dataset],img)
                            shutil.copy(ip_img_path, images_path_tvt)     


    else:
        for i in [0,1,2]:
            if i == 0: # training
                unique_videos_tvt = unique_videos[0:720]
                images_path_tvt = join('DataSet/train_test_images_cropped/FakeImgDatasets', dataset, 'train')

            elif i == 1: # validation
                unique_videos_tvt = unique_videos[720:860]
                images_path_tvt = join('DataSet/train_test_images_cropped/FakeImgDatasets', dataset, 'valid')

            else : # testing
                unique_videos_tvt = unique_videos[860:1000]
                images_path_tvt = join('DataSet/train_test_images_cropped/FakeImgDatasets', dataset, 'test')


            if not os.path.exists(images_path_tvt):
                os.makedirs(images_path_tvt)

            # to know how many videos get completely splitted
            fully_extracted_videos = []
            extracted_images = os.listdir(images_path_tvt) 
            if len(extracted_images) > 0:
                extracted_videos = []   # video names with duplicates which has been splitted in train test
                for images in (extracted_images): # here image has value like '999_008--45.png'
                    video_name = images.split('--')[0] # has value like '999_008'
                    extracted_videos.append(video_name)                        
                
                last_video = extracted_videos[-1]
                already_extracted_videos = list(set(extracted_videos)) # unique video names which has been splitted in train test
                already_extracted_videos.remove(last_video)
                fully_extracted_videos = already_extracted_videos # fully extracted videos will be till 2nd last videos
               
            for vid in tqdm(unique_videos_tvt):
                if vid not in fully_extracted_videos:
                    for img in all_images:
                        if vid in img: # checking vid substring is in string img or not
                            ip_img_path = join(data_path, DATASET_PATHS[dataset],img)
                            shutil.copy(ip_img_path, images_path_tvt)       
    

if __name__ == '__main__':
    p = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    p.add_argument('--dataset', '-d', type=str,
                   choices=list(DATASET_PATHS.keys()) + ['all'],
                   default='all')
    args = p.parse_args()

    if args.dataset == 'all':
        for dataset in DATASET_PATHS.keys():
            args.dataset = dataset
            train_test_split(**vars(args))
    else:
        train_test_split(**vars(args))
        