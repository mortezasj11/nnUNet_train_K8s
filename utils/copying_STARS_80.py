import os
from shutil import copyfile
import nibabel as nib

path_ct = '/Data7/mbsaad/Datasets/SABR/STARS/SAM/CT'
path_rts = '/Data7/mbsaad/Datasets/SABR/STARS/SAM/SAMR'

path_des_im_tr = '/Data7/Mori/nnUnet2_Sep2024/Task101_LungTumor/imagesTr' 
path_des_lb_tr = '/Data7/Mori/nnUnet2_Sep2024/Task101_LungTumor/labelsTr'

not_loaded_all = []
if __name__ == '__main__':
    for idx, ct_file in enumerate(os.listdir(path_ct)):
        try:
            # Extract the numeric part from the filename (CT_XXXX.nii.gz)
            ct_id = ct_file.split('_')[1].split('.')[0]
            print(idx, '. ', ct_id)

            # Construct full paths for the CT and RTS (segmentation) files
            path_ct_src = os.path.join(path_ct, ct_file)
            path_rts_src = os.path.join(path_rts, f'SAMR_{ct_id}.nii.gz')

            # Load the CT NIfTI file
            ct_nifti = nib.load(path_ct_src)

            # Load the segmentation file and binarize (convert all non-zero values to 1)
            seg_nifti = nib.load(path_rts_src)
            seg_data = seg_nifti.get_fdata()
            seg_data[seg_data != 0] = 1

            # Define destination paths for saving the CT and segmentation
            path_ct_des = os.path.join(path_des_im_tr, f'{ct_id}_STAR_0000.nii.gz')
            path_seg_des = os.path.join(path_des_lb_tr, f'{ct_id}_STAR.nii.gz')

            # Copy the CT file as it is
            copyfile(path_ct_src, path_ct_des)

            # Create and save the new binarized segmentation NIfTI image
            seg_nifti_bin = nib.Nifti1Image(seg_data, ct_nifti.affine)
            nib.save(seg_nifti_bin, path_seg_des)

        except Exception as e:
            print(f"Error processing {ct_file}: {e}")
            not_loaded_all.append(ct_file)
            continue

    print(not_loaded_all)
    


# docker run -it --rm --gpus all --user root --shm-size=200G  --cpuset-cpus=225-230 \
# -v /rsrch1/ip/msalehjahromi/codes/nnUnet2_Sep2024:/Code \
# -v /rsrch7/wulab/:/Data7 \
# --name mori12346 founctt:msalehjahromi

# --user $(id -u):$(id -g)


