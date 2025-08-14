# -*- coding: utf-8 -*-

import os
import subprocess

# Define paths
fa_root = "/media/UG2/yqw/fa_ants/fa/"
wmparc_dir = "/media/UG2/yqw/fa_ants/MNI/individual/"

# Iterate over each subject folder in fa_root
for subject in os.listdir(fa_root):
    sub_path = os.path.join(fa_root, subject)
    fa_path = os.path.join(sub_path, "fa.nii.gz")
    mni_path = os.path.join(sub_path, "MNI")
    reference_fa_dir = os.path.join(sub_path, "reference_fa")
    os.makedirs(reference_fa_dir, exist_ok=True)

    warp_file = os.path.join(mni_path, "Atlas2SubWarpWarp.nii")
    affine_file = os.path.join(mni_path, "Atlas2SubWarpAffine.txt")

    if not (os.path.exists(fa_path) and os.path.exists(warp_file) and os.path.exists(affine_file)):
        print(f"[Skip] Missing FA image or transform files for {subject}, skipping...")
        continue

    # Iterate over each wmparc file in wmparc_dir
    for wm_file in os.listdir(wmparc_dir):
        wmparc_path = os.path.join(wmparc_dir, wm_file)

        if not wm_file.endswith(".nii.gz"):
            continue

        wm_name = os.path.splitext(os.path.splitext(wm_file)[0])[0]  # remove .nii.gz
        output_image = os.path.join(reference_fa_dir, f"{subject}_{wm_name}_0000.nii.gz")

        warp_cmd = [
            "WarpImageMultiTransform", "3",
            wmparc_path, output_image,
            "-R", fa_path,
            warp_file, affine_file,
            "--use-NN"
        ]

        try:
            subprocess.run(warp_cmd, check=True)
            print(f"[Done] {subject}{wm_file} mapped to FA space.")
        except subprocess.CalledProcessError as e:
            print(f"[Error] {subject}{wm_file} warp failed: {e}")
