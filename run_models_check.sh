# Usage: sh run_models_check.sh    -- will run program from commandline within  Workspace


### ********************* Base Paper Results ↓ *****************

#### on DFFD dataset of paper ↓ #########

# 1.  Xception results on DFFD dataset of paper
python3 train_xception.py > op_check/dffd_xception_check.txt

# 2.  +Ours, w/o MEB|FAM results on DFFD dataset of paper
python3 train_dffd_ablation_wMEB_FAM.py > op_check/wMEB_FAM_check.txt

# 3.  +Ours, w/ MEB results on DFFD dataset of paper
python3 train_dffd_ablation_wMEB.py > op_check/wMEB_check.txt

# 4.  +Ours, w/ FAM results on DFFD dataset of paper
python3 train_dffd_ablation.py > op_check/wFAM_check.txt

# 5.  +Ours, w/ FAM&MEB results on DFFD dataset of paper
python3 train_dffd_original.py > op_check/wFAMMEB_check.txt

#### on DFFD dataset of paper ↑ #########




##### on Celeb-DF dataset of paper ↓ ############

# 6.  Xception on Celeb-DF dataset of paper
python3 train_xception_celeb.py > op_check/xception_celeb_check.txt

# 7.  +RE on Celeb-DF dataset of paper
python3 randomerasing_celebdf.py > op_check/xception_celeb_RE_check.txt

# 8.  +Ours (RFM) on Celeb-DF dataset of paper
python3 train_celeb_original.py > op_check/celeb_original_check.txt

##### on Celeb-DF dataset of paper ↑ ############



##### on DFFD (Group A) dataset of paper ↓ ############

# 9.  Xception on DFFD (Group A) dataset of paper
python3 train_xception_grpA.py > op_check/dffd_xception_grpA_check.txt

# 10.  +RE on DFFD (Group A) dataset of paper
python3 train_random_erasing.py > op_check/dffd_xception_RE_grpA_check.txt

# 11.  +Ours (RFM) on DFFD (Group A) dataset of paper
python3 train_dffd_grpA.py > op_check/dffd_grpA_check.txt

##### on DFFD (Group A) dataset of paper ↑ ############




##### on DFFD (Group B) dataset of paper ↓ ############

# 12.  Xception on DFFD (Group B) dataset of paper
python3 train_xception_grpB.py > op_check/dffd_xception_grpB_check.txt

# 13.  +RE on DFFD (Group B) dataset of paper
python3 randomerasing_grpB.py > op_check/dffd_xception_RE_grpB_check.txt

# 14.  +Ours (RFM) on DFFD (Group B) dataset of paper
python3 train_dffd_grpB.py > op_check/dffd_grpB_check.txt

##### on DFFD (Group B) dataset of paper ↑ ############


### ********************* Base Paper Results ↑ *****************




### ***************** FUTURE WORK RESULTS ↓ ***********************

#### Novelty in DataSet (Face Shifter and Neural Textures) ↓ ####

# 15.  Xception on Face Shifter and Neural Textures
python3 train_dffd_future_xception.py > op_check/dffd_future_xception_check.txt

# 16.  +Ours (RFM) on Face Shifter and Neural Textures
python3 train_dffd_future.py > op_check/dffd_future_check.txt


#### Novelty in DataSet (Face Shifter and Neural Textures) ↑ ####


#### Novelty in  Method (applied gaussian occulusion) ↓ ####

# 17.  
python3 train_dffd_future_gaussian.py > op_check/dffd_future_gaussian_check.txt

#### Novelty in  Method (applied gaussian occulusion) ↑ ####



#### Novelty in Model (Efficient Net V2 S) on DFFD ↓ ####

# 18.  
python3 train_dffd_future_effnet_v2_s.py > op_check/dffd_future_effnetv2s_check.txt

#### Novelty in Model (Efficient Net V2 S) on DFFD ↑ ####


### ***************** FUTURE WORK RESULTS ↑ ***********************
