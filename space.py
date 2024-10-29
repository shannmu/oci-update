import sys
import os
import json
import argparse
import subprocess


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Docker Image Dynamic Update')
    
    parser.add_argument('--oci_image_root', type=str, required=True, help='Root path to OCI Image')
    parser.add_argument('--diff_tar_path', type=str, required=True, help='Path to OCI Image tar')
    parser.add_argument('--image_name', type=str, required=True, help='Docker Image Name')
    parser.add_argument("--tag", type=str, required=True, help='OCI Image tag')
    
    args = parser.parse_args()
    
    # Check whether the `Root Path to OCI Image` is absolute path
    if not os.path.isabs(args.oci_image_root):
        print('Root Path to OCI Image must be an absolute path')
        sys.exit(1)
    
    # Check the diff_tar_path is a tar file and exists
    if not os.path.isfile(args.diff_tar_path):
        print('Diff tar file does not exist')
        sys.exit(1)

    # tar the OCI Image tar into oic_image_root
    path = args.diff_tar_path
    subprocess.run(['tar', '-xzvf', path, '-C', args.oci_image_root])

    # update the docker image using the OCI Image
    oci_image_path = f"{args.oci_image_root}:{args.image_name}:{args.tag}"
    docker_archive_path = f"{args.image_name}.tar"
    subprocess.run(['skopeo', 'copy', f'oci:{oci_image_path}', f'docker-daemon:{args.image_name}:latest'])

    print('This program is being run by itself')