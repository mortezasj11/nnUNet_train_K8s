import os
import subprocess
import argparse

def predict(in_path, out_path, model):


    command = ["pip", "install", "torch"]
    result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    command = ["pip", "install", "nnunetv2"]
    result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    os.environ["nnUNet_preprocessed"] = "/rsrch1/ip/msalehjahromi/nnUnet2_Sep2024/nnUNet_preprocessed"
    os.environ["nnUNet_raw"] = "/rsrch1/ip/msalehjahromi/nnUnet2_Sep2024/nnUNet_raw"
    os.environ["nnUNet_results"] = "/rsrch1/ip/msalehjahromi/nnUnet2_Sep2024/nnUNet_results"

    command = ["nnUNetv2_predict", "-i", in_path, "-o", out_path, "-d", model, "-c", "3d_fullres"]
    #           nnUNetv2_predict    -i / in_path   -o  /out_path   -d    501    -c    3d_fullres

    result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print("Command output:\n", result.stdout)


if __name__ == "__main__":
    in_path = "/rsrch1/ip/msalehjahromi/nnUnet2_Sep2024/nnUNet_raw/Dataset102_LungTumor/imagesTs"
    out_path = "/rsrch1/ip/msalehjahromi/nnUnet2_Sep2024/nnUNet_raw/Dataset102_LungTumor/labelsTs"

    parser = argparse.ArgumentParser(description="Train nnUNet with a specific fold")
    parser.add_argument('--in_path' , type=str, default = in_path,  help='input nifti files path')
    parser.add_argument('--out_path', type=str, default = out_path,  help='predicted nifti files path')
    parser.add_argument('--model', type=str, default = "101",  help='model 101, 102, ...')
    args = parser.parse_args()
    predict(args.in_path, args.out_path, args.model)