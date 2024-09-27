import os
import nibabel as nib

# Define the paths to the directories
images_dir = '/rsrch7/home/ip_rsrch/wulab/Mori/nnUnet2_Sep2024/nnUNet_raw/Dataset101_LungTumor/imagesTr'
labels_dir = '/rsrch7/home/ip_rsrch/wulab/Mori/nnUnet2_Sep2024/nnUNet_raw/Dataset101_LungTumor/labelsTr'

# Function to update the affine matrix of segmentation files if necessary
def update_seg_affine(ct_path, seg_path):
    try:
        # Load the CT and segmentation NIfTI files using nibabel
        ct_nifti = nib.load(ct_path)
        seg_nifti = nib.load(seg_path)

        ct_affine = ct_nifti.affine
        # Get the CT affine matrix and check if the header is present
        if 'pixdim' in ct_nifti.header and ct_affine[2, 2] != ct_nifti.header['pixdim'][3]:
            ct_affine[0, 0] = ct_nifti.header['pixdim'][1]
            ct_affine[1, 1] = ct_nifti.header['pixdim'][2]
            ct_affine[2, 2] = ct_nifti.header['pixdim'][3]

            # Correct the CT's affine matrix based on its header
            updated_ct_nifti = nib.Nifti1Image(ct_nifti.get_fdata(), ct_affine)
            nib.save(updated_ct_nifti, ct_path)
            print("CT corrected!     " , ct_path)

        # Update the segmentation's affine matrix to match the CT's affine matrix
        updated_seg_nifti = nib.Nifti1Image(seg_nifti.get_fdata(), ct_affine)
        nib.save(updated_seg_nifti, seg_path)

    except Exception as e:
        print(f"Error processing file {seg_path}: {str(e)}")

# Loop through all CT files in the images directory
count = 0
for ct_file in os.listdir(images_dir):
    if ct_file.endswith('_0000.nii.gz'):
        # Extract the base filename (xxxx)
        base_name = ct_file.split('_0000.nii.gz')[0]

        # Define the corresponding segmentation file name
        seg_file = f"{base_name}.nii.gz"

        # Full paths to the CT and segmentation files
        ct_path = os.path.join(images_dir, ct_file)
        seg_path = os.path.join(labels_dir, seg_file)

        # Check if the segmentation file exists
        if os.path.exists(seg_path):
            # Update the affine matrix to match the CT file
            update_seg_affine(ct_path, seg_path)
            count += 1
        else:
            print(f"Segmentation file not found for: {base_name}")

print(f"Processed {count} files.")
