



# import numpy as np
# a = np.array([1, 2, 3, 4])
# np.save("/rsrch7/home/ip_rsrch/wulab/Mori/nnUnet2_Sep2024/nnUNet_raw/Dataset101_LungTumor/K8S/arraySaved.npy", a)

from collections import OrderedDict
#import SimpleITK as sitk
import os
import json

# I'm tired of typing these out
join = os.path.join

def save_json(obj, file: str, indent: int = 4, sort_keys: bool = True) -> None:
    with open(file, 'w') as f:
        json.dump(obj, f, sort_keys=sort_keys, indent=indent)

if __name__ == "__main__":

    json_dict = OrderedDict()
    json_dict['name'] = "Task101_LungTumor"
    json_dict['description'] = ""
    json_dict['tensorImageSize'] = "3D"
    json_dict['reference'] = ""
    json_dict['licence'] = ""
    json_dict['release'] = "0.0"

    #json_dict['modality'] = {"0": "CT"}
    # json_dict['labels'] = {
    #     "0": "background",
    #     "1": "Lung",
    #     "2": "Vessel",
    #     "3": "Tumor"}

    json_dict["channel_names"] = {"0": "CT"}
    json_dict['labels'] = {
                           "background": "0" ,
                            "Tumor":"1"}


    json_dict['file_ending'] = ".nii.gz"


    out_folder = '/rsrch1/ip/msalehjahromi/nnUnet2_Sep2024/nnUNet_raw/Dataset101_LungTumor'
    folder     = '/rsrch1/ip/msalehjahromi/nnUnet2_Sep2024/nnUNet_raw/Dataset101_LungTumor'
    current_dir = join(folder, "imagesTr")
    raw_data = [i for i in os.listdir(current_dir) if  i.endswith(".nii.gz")]
    json_dict['numTraining'] = len(raw_data)
    current_dir_Ts = join(folder, "imagesTs")
    test_data = [i for i in os.listdir(current_dir_Ts) if  i.endswith(".nii.gz")]
    json_dict['numTest'] = len(test_data)
    json_dict['training'] = [{'image': "./imagesTr/%s.nii.gz" % i[:-12], "label": "./labelsTr/%s.nii.gz" % i[:-12]} for i in os.listdir(current_dir)]
    json_dict['test'] = ["./imagesTs/%s.nii.gz" % i[:-12] for i in os.listdir(current_dir_Ts)]
    save_json(json_dict, os.path.join(out_folder, "dataset.json"))