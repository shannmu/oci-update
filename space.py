import sys
import os
import json
import argparse
import subprocess

# NOTE: The palce storing the OCI Image is fixed: /data/oci-image
oic_image_root = '/data/oci-image'
# oic_image_root = '/home/shanmu/data/oci-image/'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Docker Image Dynamic Update')

    parser.add_argument('--path', type=str, help='Path to OCI Image tar')
    parser.add_argument('--image', type=str, help='Docker Image Name')
    
    args = parser.parse_args()

    # tar the OCI Image tar into oic_image_root
    path = args.path
    subprocess.run(['tar', '-xzvf', path, '-C', oic_image_root])

    # update the docker image using the OCI Image
    subprocess.run(['skopeo', 'copy', 'oci:{}'.format(oic_image_root + args.image), 'docker-archive:{}'.format(args.image) + '.tar'])

    # load the docker image
    subprocess.run(['docker', 'load', '-i', args.image + '.tar'])

    # remove the docker image tar
    subprocess.run(['rm', args.image + '.tar'])

    print('This program is being run by itself')