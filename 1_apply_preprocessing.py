import os
import subprocess
import numpy as np


# import numpy as np
# a = np.array([1, 2, 3, 4])



def run_nnunetv2():
    try:
        command = ["pip", "install", "nnunetv2"]
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        os.environ["nnUNet_preprocessed"] = "/rsrch1/ip/msalehjahromi/nnUnet2_Sep2024/nnUNet_preprocessed"
        os.environ["nnUNet_raw"] = "/rsrch1/ip/msalehjahromi/nnUnet2_Sep2024/nnUNet_raw"
        os.environ["nnUNet_results"] = "/rsrch1/ip/msalehjahromi/nnUnet2_Sep2024/nnUNet_results"

        # Define the command as a list of arguments
        command = ["nnUNetv2_plan_and_preprocess", "-d", "101", "--verify_dataset_integrity"]

        # Run the command
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Print the output
        print("Command output:\n", result.stdout)


    except subprocess.CalledProcessError as e:
        #np.save("/rsrch1/ip/msalehjahromi/nnUnet2_Sep2024/nnUNet_raw/Dataset101_LungTumor/K8S/zzz_Except.npy", a)

        print(f"Error occurred: {e}")
        print("Standard Output:\n", e.stdout)
        print("Standard Error:\n", e.stderr)

if __name__ == "__main__":
    # if os.path.exists("/rsrch1/ip/msalehjahromi/nnUnet2_Sep2024/nnUNet_raw/Dataset101_LungTumor"):
    #     np.save("/rsrch1/ip/msalehjahromi/nnUnet2_Sep2024/nnUNet_raw/Dataset101_LungTumor/K8S/zzz_Dataset101_LungTumor_EXIST.npy", a)###### Test

    # if os.path.exists("/rsrch1/ip/msalehjahromi/nnUnet2_Sep2024/nnUNet_raw/Dataset101_LungTumor/imagesTr"):
    #     np.save("/rsrch1/ip/msalehjahromi/nnUnet2_Sep2024/nnUNet_raw/Dataset101_LungTumor/K8S/zzz_imagesTr_EXIST.npy", a)###### Test

    # if os.path.exists("/rsrch1/ip/msalehjahromi/nnUnet2_Sep2024/nnUNet_raw/Dataset101_LungTumor/imagesTr/0001_STAR_0000.nii.gz"):
    #     np.save("/rsrch1/ip/msalehjahromi/nnUnet2_Sep2024/nnUNet_raw/Dataset101_LungTumor/K8S/zzz_0001_STAR_0000.nii.gz_EXIST.npy", a)###### Test
        
    run_nnunetv2()
