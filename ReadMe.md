
# Dockerfile and image
Reminder: I need to make image first in harbor and then push to it. 
The combination of both the container and installing nnunet in .py file, make the nnuUNetv2 work here! (At least how I get it top work!)

docker tag nnunetv2:msalehjahromi hpcharbor.mdanderson.edu/nnunetv2/nnunetv2:msalehjahromi
docker push hpcharbor.mdanderson.edu/nnunetv2/nnunetv2:msalehjahromi

hpcharbor.mdanderson.edu/nnunetv2/nnunetv2@sha256:4ab016ba4b356842be74fbf58159480598bfc015c8454339022aa0fcbfdc196d

# running
job-runner.sh 0_jason.yaml
job-runner.sh 1_pre_preprocessing.yaml
job-runner.sh 2_train0.yaml
job-runner.sh 2_train1.yaml
job-runner.sh 2_train2.yaml
job-runner.sh 2_train3.yaml
job-runner.sh 2_train4.yaml

# PVC (commands)
kubectl get pvc -n yn-gpu-workload -l k8s-user=msalehjahromi
kubectl describe pvc msalehjahromi-gpu-rsrch7-home-ip-rsrch -n yn-gpu-workload

# bashrc
export PATH="/rsrch1/ip/msalehjahromi/.kube:$PATH"
source ~/.bashrc

# Good K8S Commands
kubectl get jobs
kubectl config use-context msalehjahromi_yn-gpu-workload@research-prd
kubectl delete job -n yn-gpu-workload msalehjahromi-gpu-nnunetv2

# yaml A100 vs H100
        "nvidia.com/gpu.machine": "DGXH100"
        "nvidia.com/gpu.machine": "DGXA100-920-23687-2530-000"

# nnUNetor 2000 epochs!
nnUNetv2_train dataset_id 3d_fullres num_fold -tr nnUNetTrainer_2000epochs

# nnUNetv2
I needed to use my docker file, I needed to install torch and nnUNet in my .py file also.
I needed to use A100, could not use H100 with some pytorch and H100 issue.

This is going to be run on K8S

1. setting_up_paths
    https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/setting_up_paths.md
    nnUNet_results
    nnUNet_preprocessed
    nnUNet_raw/Dataset101_LungTumor/
    ├── dataset.json
    ├── imagesTr
    │   ├── la_003_0000.nii.gz
    │   ├── la_004_0000.nii.gz
    │   ├── ...
    ├── imagesTs
    │   ├── la_001_0000.nii.gz
    │   ├── la_002_0000.nii.gz
    │   ├── ...
    └── labelsTr
        ├── la_003.nii.gz
        ├── la_004.nii.gz
        ├── ...


2. modify the json file for k8s based on '/rsrch7/home/ip_rsrch/wulab/Mori'
    https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/set_environment_variables.md

    RUN pip install nnunetv2
    ENV nnUNet_preprocessed="/rsrch7/home/ip_rsrch/wulab/Mori/nnUnet2_Sep2024/nnUNet_preprocessed"
    ENV nnUNet_raw="/rsrch7/home/ip_rsrch/wulab/Mori/nnUnet2_Sep2024/nnUNet_raw"
    ENV nnUNet_results="/rsrch7/home/ip_rsrch/wulab/Mori/nnUnet2_Sep2024/nnUNet_results"

3. Training
    https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/how_to_use_nnunet.md

    # Let's change these
    nnUNetv2_plan_and_preprocess -d 501 --verify_dataset_integrity

    #
    For FOLD in [0, 1, 2, 3, 4], run:
    nnUNetv2_train DATASET_NAME_OR_ID 3d_fullres FOLD [--npz]

    nnUNetv2_train 101 3d_fullres 0
    CUDA_VISIBLE_DEVICES=0 nnUNetv2_train 101 3d_fullres 0
    CUDA_VISIBLE_DEVICES=0 nnUNetv2_train 101 3d_fullres 1
    CUDA_VISIBLE_DEVICES=0 nnUNetv2_train 101 3d_fullres 2
    CUDA_VISIBLE_DEVICES=0 nnUNetv2_train 101 3d_fullres 3
    CUDA_VISIBLE_DEVICES=0 nnUNetv2_train 101 3d_fullres 4


4. prediction
    # will be changed later!
    nnUNetv2_predict \
    -i /Data/nnUNet2/nnUNet_raw/Dataset501_LungTumorVessel/imagesTs \
    -o /Data/nnUNet2/nnUNet_raw/Dataset501_LungTumorVessel/pred \
    -d 501 \
    -c 3d_fullres

    CUDA_VISIBLE_DEVICES=6 nnUNetv2_predict -i /Data/test_nnunet2 -o /Data/test_nnunet23 -d 501 -c 3d_fullres





5. K8s
    <!-- 
    # Build the docker image
    docker build -t nnunet2:msalehjahromi .
    docker build --platform linux/x86_64 -t nnunet2:msalehjahromi .

    # Push the docker image to hpcharbor.mdanderson.edu
    docker login hpcharbor.mdanderson.edu
    docker tag nnunet2:msalehjahromi hpcharbor.mdanderson.edu/msalehjahromi/nnunet2:msalehjahromi
    docker push hpcharbor.mdanderson.edu/msalehjahromi/nnunet2:msalehjahromi 
    -->

<!-- kubectl config get-contexts -->

kubectl config use-context msalehjahromi_yn-gpu-workload@research-prd
<!-- kubectl config use-context msalehjahromi_yn-cpu-workload@research-prd -->

# Jason File
job-runner.sh /rsrch7/home/ip_rsrch/wulab/Mori/nnUnet2_Sep2024/nnUNet_raw/Dataset101_LungTumor/K8S/jason.yaml
kubectl delete job -n yn-gpu-workload msalehjahromi-gpu-nnunetv2



# Training
# Observing your GPU job(s)
kubectl get jobs -n yn-gpu-workload -l k8s-user=msalehjahromi
kubectl get pods -o wide -n yn-gpu-workload

# Deleting your GPU job(s)
kubectl delete job -n yn-gpu-workload msalehjahromi-gpu-nnunetv2


# 101 --> 102 to 2000 epoch
0. main folder raw name: 101 to 102
1. in dataset.json, 101 to 102
2. in preprocess folder name: 101 to 102
3. in 2_train0 101 to 102 and add 2000
4. in .yaml the command
5. in preprocess folder in its dataset..json and Plans.jason
6. yaml of 0_ and 1_ (not necessary as I changed their results, but anyway for later ... )
