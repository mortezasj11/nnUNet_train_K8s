
## Dockerfile and image
Reminder: I need to make image first in harbor and then push to it. <br>
The combination of both the container and installing nnunet in .py file, make the nnuUNetv2 work here! (At least how I get it top work!)<br>

docker tag nnunetv2:msalehjahromi hpcharbor.mdanderson.edu/nnunetv2/nnunetv2:msalehjahromi<br>
docker push hpcharbor.mdanderson.edu/nnunetv2/nnunetv2:msalehjahromi<br>

hpcharbor.mdanderson.edu/nnunetv2/nnunetv2@sha256:4ab016ba4b356842be74fbf58159480598bfc015c8454339022aa0fcbfdc196d<br>

## running
```sh
job-runner.sh 0_jason.yaml<br>
job-runner.sh 1_pre_preprocessing.yaml<br>
job-runner.sh 2_train0.yaml<br>
job-runner.sh 2_train1.yaml<br>
job-runner.sh 2_train2.yaml<br>
job-runner.sh 2_train3.yaml<br>
job-runner.sh 2_train4.yaml<br>
```

## PVC (commands)
```sh
kubectl get pvc -n yn-gpu-workload -l k8s-user=msalehjahromi<br>
kubectl describe pvc msalehjahromi-gpu-rsrch7-home-ip-rsrch -n yn-gpu-workload
```

## bashrc
```sh
export PATH="/rsrch1/ip/msalehjahromi/.kube:$PATH"
source ~/.bashrc
```

## Good K8S Commands
```sh
kubectl get jobs<br>
kubectl config use-context msalehjahromi_yn-gpu-workload@research-prd<br>
kubectl delete job -n yn-gpu-workload msalehjahromi-gpu-nnunetv2
```

## yaml A100 vs H100
```sh
        "nvidia.com/gpu.machine": "DGXH100"<br>
        "nvidia.com/gpu.machine": "DGXA100-920-23687-2530-000"
```

## nnUNetor 2000 epochs!
```sh
nnUNetv2_train dataset_id 3d_fullres num_fold -tr nnUNetTrainer_2000epochs
```

## nnUNetv2
I needed to use my docker file, I needed to install torch and nnUNet in my .py file also.<br>
I needed to use A100, could not use H100 with some pytorch and H100 issue.

This is going to be run on K8S

### 1. setting_up_paths<br>
    https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/setting_up_paths.md<br>
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


### 2. modify the json file for k8s based on '/rsrch7/home/ip_rsrch/wulab/Mori'<br>
    https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/set_environment_variables.md<br>

    ```sh
    RUN pip install nnunetv2<br>
    ENV nnUNet_preprocessed="/rsrch7/home/ip_rsrch/wulab/Mori/nnUnet2_Sep2024/nnUNet_preprocessed"<br>
    ENV nnUNet_raw="/rsrch7/home/ip_rsrch/wulab/Mori/nnUnet2_Sep2024/nnUNet_raw"<br>
    ENV nnUNet_results="/rsrch7/home/ip_rsrch/wulab/Mori/nnUnet2_Sep2024/nnUNet_results"<br>
    ```

### 3. Training<br>
    https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/how_to_use_nnunet.md<br>

    #### Let's change these
    nnUNetv2_plan_and_preprocess -d 501 --verify_dataset_integrity

    ####
    For FOLD in [0, 1, 2, 3, 4], run:<br>

    ```sh
    nnUNetv2_train DATASET_NAME_OR_ID 3d_fullres FOLD [--npz]<br>

    nnUNetv2_train 101 3d_fullres 0<br>
    CUDA_VISIBLE_DEVICES=0 nnUNetv2_train 101 3d_fullres 0<br>
    CUDA_VISIBLE_DEVICES=0 nnUNetv2_train 101 3d_fullres 1<br>
    CUDA_VISIBLE_DEVICES=0 nnUNetv2_train 101 3d_fullres 2<br>
    CUDA_VISIBLE_DEVICES=0 nnUNetv2_train 101 3d_fullres 3<br>
    CUDA_VISIBLE_DEVICES=0 nnUNetv2_train 101 3d_fullres 4<br>
    ```

### 4. prediction<br>
    #### will be changed later!<br>
    ```sh
    nnUNetv2_predict \<br>
    -i /Data/nnUNet2/nnUNet_raw/Dataset501_LungTumorVessel/imagesTs \<br>
    -o /Data/nnUNet2/nnUNet_raw/Dataset501_LungTumorVessel/pred \<br>
    -d 501 \<br>
    -c 3d_fullres<br>

    CUDA_VISIBLE_DEVICES=6 nnUNetv2_predict -i /Data/test_nnunet2 -o /Data/test_nnunet23 -d 501 -c 3d_fullres<br>





### 5. K8s
    ```sh
    #### Build the docker image<br>
    docker build -t nnunet2:msalehjahromi .<br>
    docker build --platform linux/x86_64 -t nnunet2:msalehjahromi .

    #### Push the docker image to hpcharbor.mdanderson.edu<br>
    docker login hpcharbor.mdanderson.edu<br>
    docker tag nnunet2:msalehjahromi hpcharbor.mdanderson.edu/msalehjahromi/nnunet2:msalehjahromi<br>
    docker push hpcharbor.mdanderson.edu/msalehjahromi/nnunet2:msalehjahromi 
    ```

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


### 101 --> 102 to 2000 epoch<br>
0. main folder raw name: 101 to 102<br>
1. in dataset.json, 101 to 102<br>
2. in preprocess folder name: 101 to 102<br>
3. in 2_train0 101 to 102 and add 2000<br>
4. in .yaml the command<br>
5. in preprocess folder in its dataset..json and Plans.jason<br>
6. yaml of 0_ and 1_ (not necessary as I changed their results, but anyway for later ... )<br>
