import os
import subprocess
import argparse

def train(fold):
    try:

        command = ["pip", "install", "torch"]
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        command = ["pip", "install", "nnunetv2"]
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        os.environ["nnUNet_preprocessed"] = "/rsrch1/ip/msalehjahromi/nnUnet2_Sep2024/nnUNet_preprocessed"
        os.environ["nnUNet_raw"] = "/rsrch1/ip/msalehjahromi/nnUnet2_Sep2024/nnUNet_raw"
        os.environ["nnUNet_results"] = "/rsrch1/ip/msalehjahromi/nnUnet2_Sep2024/nnUNet_results"

        #command = ["nnUNetv2_train", "101", "3d_fullres", str(fold)]
        command = ["nnUNetv2_train", "102", "3d_fullres", str(fold), "-tr","nnUNetTrainer_2000epochs"]
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        print("Command output:\n", result.stdout)

    except subprocess.CalledProcessError as e:
        
        print("Error occurred while running the command:\n", e.stderr)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train nnUNet with a specific fold")
    parser.add_argument('--fold', type=str, default = "0",  help='Fold number for training')
    args = parser.parse_args()
    train(args.fold)