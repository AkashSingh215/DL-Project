            ## By Akash Singh (19023, Data Sci. & Engineering, IISER Bhopal)

        ------------ My Project Steps -----------------

========== ALL Datasets ARE STORED IN DataSet folder ======================
1. Download dataset having videos from internet or by python script. These are stored here in Folder Celeb-DF-v2 (downloaded from internet by filling official g-form),
   DDFD (downloaded from internet by filling official g-form), FaceForencics++ (downloaded through faceforencics.py obtained after filling official g-form).
    
    # Here in FaceForencics++ I just downloaded dataset : 'original', 'Deepfakes', 'Face2Face', 'FaceShifter', 'FaceSwap', 'NeuralTextures' ; of compression 'c23'.

    eg. say to download FaceShifter dataset with c23 compression in the DataSet/FaceForencics++ folder :
    run the below code in terminal :
        python3 faceforensics.py DataSet/FaceForencics++ -d FaceShifter -c c23

2. run extract_facialimage.py to get facial images from key frames of videos. 
    These images are stored in Folder 'Images_cropped' in DataSet.
    run the below code in terminal for eaxtracting first 500 celeb-real videos:
            python3 extract_facialimage.py -d Celeb-real --start 0 --end 500 -c nc
    run the below code in terminal for eaxtracting next 500 celeb-real videos:
            python3 extract_facialimage.py -d Celeb-real --start 500 --end 1000 -c nc

4. run delete_zero_size_images.py to remove images of size zero in the Folder 'Images_cropped'.
    run the below code in terminal for deleting celeb-real images :
            python3 delete_zero_size_images.py -d Celeb-real


3. run train_test_split.py to divide images in train,valid and test. The o/p of this step, images
    is stored in folder train_test_images_cropped.
    run the below code in terminal for train,test,split the images present in 
    folder DataSet/Images_cropped/Celeb-DF/Celeb-real :
        python3 train_test_split.py -d Celeb-real

5. run delete.py to remove images of size zero in the Folder train or test or valid in diff. dataset in 'train_test_images_cropped'.
    run the below code in terminal for deleting celeb-real train images :
            python3 delete.py -d Celeb-real --splt train

6. run model train_<accordingly>.py for according Class mentioned in utilscopy/datasets_profiles.py or in paper
    for eg. run python3 train_dffd_original.py on dffd dataset with cropped images with RFM.

    NOTE: Always change the path in resume_model & resume_optim a/c to the latest model and optim saved 
    in the train_().py file. Since i changed the default value to not None.

    ** Models and optimizers are saved in their respective folder in models folder

7. NOTE: I am saving output we get printed on terminal to respective text file in filder op_save.

##### 
NOTE : You can run sh file accordingly. !!!!!!!!!! for above point 6.