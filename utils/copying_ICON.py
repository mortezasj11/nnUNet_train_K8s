import os
from shutil import copyfile
import nibabel as nib

path = '/Data7/JWu11/Sheeba/Sheeba_databases_Final/ICON/Pre_updated_3/'
# path_des_im_tr = '/Data1/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task501_LungTumorVessel/imagesTr' 
# path_des_lb_tr = '/Data1/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task501_LungTumorVessel/labelsTr'

path_des_im_tr = '/Data7/Mori/nnUnet2_Sep2024/Task101_LungTumor/imagesTr' 
path_des_lb_tr = '/Data7/Mori/nnUnet2_Sep2024/Task101_LungTumor/labelsTr'

not_loaded_all = []
if __name__=='__main__':
    for idx, mrn in enumerate(os.listdir(path)):
        print(idx, '. ', mrn)

        path_mrn = os.path.join(path, mrn)

        try:
            # ct
            path_ct_src = os.path.join(path_mrn, 'CT.nii')
            ct_nifti = nib.load(path_ct_src)

            # Segs
            path_tumor_src = os.path.join(path_mrn, 'Seg_tumor.nii')
            seg_tumor = nib.load(path_tumor_src).get_fdata()
            seg_tumor[seg_tumor!=0] = 1

            # Destination paths for the new compressed files
            path_ct_des = os.path.join(path_des_im_tr, f'{mrn}_IC_0000.nii.gz')
            path_seg_des = os.path.join(path_des_lb_tr, f'{mrn}_IC.nii.gz')

            # Compress and save the CT file to .nii.gz
            nib.save(ct_nifti, path_ct_des)

            # Create and compress the new segmentation NIfTI image with the same affine as the CT
            seg_nifti = nib.Nifti1Image(seg_tumor, ct_nifti.affine)
            seg_nifti.to_filename(path_seg_des)

        except Exception as e:
            print(f"Error processing {mrn}: {e}")
            not_loaded_all.append(mrn)
            continue

    print(not_loaded_all)
    


# docker run -it --rm --gpus all --user root --shm-size=200G  --cpuset-cpus=200-224 \
# -v /rsrch1/ip/msalehjahromi/codes/nnUnet2_Sep2024:/Code \
# -v /rsrch7/wulab/:/Data7 \
# --name mori12345 founctt:msalehjahromi

# --user $(id -u):$(id -g)


