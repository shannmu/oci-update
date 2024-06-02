import sys
import os
import json
import argparse
import subprocess

class ImageDiff():
    def __init__(self, index, oci_layout, menifest, config, layers):
        self.index = index
        self.oci_layout = oci_layout
        self.menifest = menifest
        self.config = config
        self.layers = layers

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Docker Image Dynamic Update')

    # parser.add_argument('--image', type=str, help='Docker Image Name')
    # parser.add_argument('--tag', type=str, help='Docker Image Tag')
    parser.add_argument('--path', type=str, help='Path to OCI Image')

    args = parser.parse_args()

    diff = []

    # add path into diff
    path: str = args.path

    # step 1. get index.json and oci-layout
    index = path + '/' + 'index.json'
    oci_layout = path + '/' + 'oci-layout'

    menifests = []
    # step 2. get manifest
    with open(index) as f:
        index_content = json.load(f)
        for item in index_content['manifests']:
            menifest = path + '/' + 'blobs/' + item['digest'].replace(':', '/')
            menifests.append(menifest)

    # step 3. get config and different layers
    if len(menifests) == 1:
        print('No need to update')
        sys.exit(0)

    newer = menifests[-1]
    older = menifests[-2]

    with open(newer) as f_new, open(older) as f_old:
        newer_content = json.load(f_new)
        older_content = json.load(f_old)

        # get config
        config = path + '/' + 'blobs/' + newer_content['config']['digest'].replace(':', '/')

        # get layers
        layers = []
        for i in range(len(newer_content['layers']) - len(older_content['layers'])):
            layer = path + '/' + 'blobs/' + newer_content['layers'][len(older_content['layers']) + i]['digest'].replace(':', '/')
            layers.append(layer)
            

    diff = ImageDiff(index, oci_layout, newer, config, layers)

    # step 4. exec tar command to tar the diff
    res = subprocess.run(['tar', '-czf', 'diff.tar.gz', diff.index, diff.config, diff.oci_layout, diff.index] + diff.layers)
