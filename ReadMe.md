# nnUNetv2 Setup and Usage Guide
## Dockerfile and image
#### Build and Push Docker Image
Before running the setup, build the Docker image and push it to the harbor registry:
```sh
docker tag nnunetv2:msalehjahromi hpcharbor.mdanderson.edu/nnunetv2/nnunetv2:msalehjahromi<br>
docker push hpcharbor.mdanderson.edu/nnunetv2/nnunetv2:msalehjahromi<br>
```
#### Image Location:
hpcharbor.mdanderson.edu/nnunetv2/nnunetv2@sha256:4ab016ba4b356842be74fbf58159480598bfc015c8454339022aa0fcbfdc196d<br>

#### Important Notes
- Ensure that nnUNet is installed inside the Docker container as specified in your .py file for proper functionality. (At least this is how I get it to work!)
- Use the A100 GPU for training due to compatibility issues with H100 for some PyTorch setups.



## Running Jobs
Submit jobs sequentially using the job-runner.sh script:
```sh
job-runner.sh 0_jason.yaml

job-runner.sh 1_pre_preprocessing.yaml

job-runner.sh 2_train0.yaml
job-runner.sh 2_train1.yaml
job-runner.sh 2_train2.yaml
job-runner.sh 2_train3.yaml
job-runner.sh 2_train4.yaml

job-runner.sh 3_predict.yaml

```

## List and describe the PVCs with the following commands:
```sh
kubectl get pvc -n yn-gpu-workload -l k8s-user=msalehjahromi
kubectl describe pvc msalehjahromi-gpu-rsrch7-home-ip-rsrch -n yn-gpu-workload
```

## Environment Configuration
```sh
export PATH="/rsrch1/ip/msalehjahromi/.kube:$PATH"
source ~/.bashrc
```

## Useful Kubernetes (K8s) Commands
- View jobs:
```sh
kubectl get jobs
```
- Switch context:
```sh
kubectl config use-context msalehjahromi_yn-gpu-workload@research-prd
```
- Delete a job:
```sh
kubectl delete job -n yn-gpu-workload msalehjahromi-gpu-nnunetv2
```

## YAML Configurations for Different GPU Types
```sh
        "nvidia.com/gpu.machine": "DGXH100"
        "nvidia.com/gpu.machine": "DGXA100-920-23687-2530-000"
```

## nnUNetor 2000 epochs!
```sh
nnUNetv2_train dataset_id 3d_fullres num_fold -tr nnUNetTrainer_2000epochs
```

# From nnUNetv2 (Helping to set up)
I needed to use my docker file, I needed to install torch and nnUNet in my .py file also.<br>
I needed to use A100, could not use H100 with some pytorch and H100 issue.

This is going to be run on K8S

##  [Setting Up nnUNet Paths](https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/setting_up_paths.md)

    Directory structure:<br>
    <br>
    nnUNet_results<br>
    nnUNet_preprocessed<br>
    nnUNet_raw/Dataset101_LungTumor/<br>
    ├── dataset.json<br>
    ├── imagesTr<br>
    │   ├── la_003_0000.nii.gz<br>
    │   ├── la_004_0000.nii.gz<br>
    │   ├── ...<br>
    ├── imagesTs<br>
    │   ├── la_001_0000.nii.gz<br>
    │   ├── la_002_0000.nii.gz<br>
    │   ├── ...<br>
    └── labelsTr<br>
        ├── la_003.nii.gz<br>
        ├── la_004.nii.gz<br>
        ├── ...<br>


## Modify the json file for k8s based on '/rsrch7/home/ip_rsrch/wulab/Mori'
    [nnUNet help](https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/set_environment_variables.md) 

    ```sh
    RUN pip install nnunetv2
    ENV nnUNet_preprocessed="/rsrch7/home/ip_rsrch/wulab/Mori/nnUnet2_Sep2024/nnUNet_preprocessed"
    ENV nnUNet_raw="/rsrch7/home/ip_rsrch/wulab/Mori/nnUnet2_Sep2024/nnUNet_raw"
    ENV nnUNet_results="/rsrch7/home/ip_rsrch/wulab/Mori/nnUnet2_Sep2024/nnUNet_results"
    ```

## [Training](https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/how_to_use_nnunet.md)

    #### Verify dataset integrity:
    ```sh
    nnUNetv2_plan_and_preprocess -d 501 --verify_dataset_integrity
    ```

    #### Train for each fold:
    For FOLD in [0, 1, 2, 3, 4], run:<br>

    ```sh
    nnUNetv2_train DATASET_NAME_OR_ID 3d_fullres FOLD [--npz]

    nnUNetv2_train 101 3d_fullres 0<br>
    CUDA_VISIBLE_DEVICES=0 nnUNetv2_train 101 3d_fullres 0
    CUDA_VISIBLE_DEVICES=0 nnUNetv2_train 101 3d_fullres 1
    CUDA_VISIBLE_DEVICES=0 nnUNetv2_train 101 3d_fullres 2
    CUDA_VISIBLE_DEVICES=0 nnUNetv2_train 101 3d_fullres 3
    CUDA_VISIBLE_DEVICES=0 nnUNetv2_train 101 3d_fullres 4
    ```

### 4. prediction<br>
    #### will be changed later!<br>
    ```sh
    nnUNetv2_predict \
    -i /Data/nnUNet2/nnUNet_raw/Dataset501_LungTumorVessel/imagesTs \
    -o /Data/nnUNet2/nnUNet_raw/Dataset501_LungTumorVessel/pred \
    -d 501 \
    -c 3d_fullres

    CUDA_VISIBLE_DEVICES=6 nnUNetv2_predict -i /Data/test_nnunet2 -o /Data/test_nnunet23 -d 501 -c 3d_fullres
    ```




### 5. K8s
```sh
#### Build the docker image
docker build -t nnunet2:msalehjahromi .
docker build --platform linux/x86_64 -t nnunet2:msalehjahromi .

#### Push the docker image to hpcharbor.mdanderson.edu
docker login hpcharbor.mdanderson.edu
docker tag nnunet2:msalehjahromi hpcharbor.mdanderson.edu/msalehjahromi/nnunet2:msalehjahromi
docker push hpcharbor.mdanderson.edu/msalehjahromi/nnunet2:msalehjahromi 

kubectl config get-contexts 

kubectl config use-context msalehjahromi_yn-gpu-workload@research-prd<br>
kubectl config use-context msalehjahromi_yn-cpu-workload@research-prd

### Jason File
job-runner.sh /rsrch7/home/ip_rsrch/wulab/Mori/nnUnet2_Sep2024/nnUNet_raw/Dataset101_LungTumor/K8S/jason.yaml<br>
kubectl delete job -n yn-gpu-workload msalehjahromi-gpu-nnunetv2

### Training
### Observing your GPU job(s)
kubectl get jobs -n yn-gpu-workload -l k8s-user=msalehjahromi<br>
kubectl get pods -o wide -n yn-gpu-workload<br>

### Deleting your GPU job(s)<br>
kubectl delete job -n yn-gpu-workload msalehjahromi-gpu-nnunetv2
```

### 6. which parts I change to train another nnUNET with 2000 101 --> 102 to 2000 epoch<br>
0. main folder raw name: 101 to 102<br>
1. in dataset.json, 101 to 102<br>
2. in preprocess folder name: 101 to 102<br>
3. in 2_train0 101 to 102 and add 2000<br>
4. in .yaml the command<br>
5. in preprocess folder in its dataset..json and Plans.jason<br>
6. yaml of 0_ and 1_ (not necessary as I changed their results, but anyway for later ... )<br>
