# -*- coding: utf-8 -*-
import os
import subprocess

mni_path = "/media/UG5/Atlas/MNI"
atlas_path = os.path.join(mni_path, "mni_icbm152_t1_tal_nlin_asym_09a_brain.nii")

t1_root = "/media/UG2/yqw/fa_ants/fa/"


for subdir in os.listdir(t1_root):
    sub_path = os.path.join(t1_root, subdir)
    t1_path = os.path.join(sub_path, "fa.nii.gz")
    mni_output_path = os.path.join(sub_path, "MNI")
    output_prefix = os.path.join(mni_output_path, "Atlas2SubWarp.nii")


    if os.path.exists(t1_path):
        if os.path.exists(output_prefix):
            print(f"MNI result already exists for: {subdir}, skipping...")
            continue

        os.makedirs(mni_output_path, exist_ok=True)

        ants_cmd = [
            "ANTS", "3",
            "-m", f"PR[{t1_path},{atlas_path},1,2]",
            "-o", output_prefix,
            "-i", "30x99x11",
            "-t", "SyN[0.5]",
            "-r", "Gauss[2,0]",
            "--use-Histogram-Matching",
            "--continue-affine", "true"
        ]

        try:
            subprocess.run(ants_cmd, check=True)
            print(f"ANTS registration completed for: {subdir}")
        except subprocess.CalledProcessError as e:
            print(f"Error running ANTS for {subdir}: {e}")
    else:
        print(f"T1 image not found for: {subdir}")
