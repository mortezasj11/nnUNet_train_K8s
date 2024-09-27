import os
from shutil import copyfile
import nibabel as nib

path = '/Data7/nnUNET_non_smoker_March/data'
# path_des_im_tr = '/Data1/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task501_LungTumorVessel/imagesTr' 
# path_des_lb_tr = '/Data1/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task501_LungTumorVessel/labelsTr'

path_des_im_tr = '/Data7/nnUnet2_Sep2024/Task101_LungTumor/imagesTr' 
path_des_lb_tr = '/Data7/nnUnet2_Sep2024/Task101_LungTumor/labelsTr'

not_loaded_all = []
if __name__=='__main__':
    for idx, mrn in enumerate(os.listdir(path)):
        print(idx, '. ', mrn)

        path_mrn = os.path.join(path, mrn)

        try:
            # ct
            path_ct_src = os.path.join(path_mrn, 'CT.nii.gz')

            # Segs
            # path_lung_src = os.path.join(path_mrn, 'CT_LungSeg.nii.gz')
            # seg_all = nib.load(path_lung_src).get_fdata()
            # seg_all[seg_all!=0] = 1
            
            # path_vessel_1 = os.path.join(path_mrn, 'CT_VesselSeg.nii.gz')
            # seg_vessel_1 = nib.load(path_vessel_1).get_fdata()
            # seg_all[seg_vessel_1 != 0] = 2

            # path_vessel_2 = os.path.join(path_mrn, 'CT_bloodvesselANSI_r.nii.gz')
            # seg_vessel_2 = nib.load(path_vessel_2).get_fdata()
            # seg_all[seg_vessel_2 != 0] = 2

            # path_tumor_src = os.path.join(path_mrn, 'CT_Tumor.nii.gz')
            # seg_tumor = nib.load(path_tumor_src).get_fdata()
            # seg_all[seg_tumor!=0] = 1

            path_tumor_src = os.path.join(path_mrn, 'CT_Tumor.nii.gz')
            seg_tumor = nib.load(path_tumor_src).get_fdata()
            seg_tumor[seg_tumor!=0] = 1

        except:
            not_loaded_all.append(mrn)
            continue

        #copy ct
        path_ct_des = os.path.join(path_des_im_tr, mrn + '_0000.nii.gz')
        copyfile(path_ct_src, path_ct_des)

        #copy seg
        path_seg_des = os.path.join(path_des_lb_tr, mrn + '.nii.gz')
        seg_nifti = nib.Nifti1Image(seg_tumor, nib.load(path_ct_src).affine)
        seg_nifti.to_filename(path_seg_des)
    print(not_loaded_all)
    


# docker run -it --rm --gpus all --user root --shm-size=200G  --cpuset-cpus=200-224 \
# -v /rsrch1/ip/msalehjahromi/codes:/Code \
# -v /rsrch7/wulab/Mori/:/Data7 \
# --name mori1234 founctt:msalehjahromi

# --user $(id -u):$(id -g)


