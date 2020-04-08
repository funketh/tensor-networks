#!/usr/bin/env python
import argparse

from tensor_networks.patched_numpy import np
from PIL import Image

from tensor_networks.annotations import *
from tensor_networks.svd import truncated_svd


def img_to_array(path: str) -> Array:
    img = Image.open(path)
    return np.array(img)


def compress(array: Array) -> Array:
    u, s, v = truncated_svd(array, max_chi=max(array.shape))
    return (u @ np.diag(s) @ v).astype(array.dtype)


def save_array_as_img(array: Array, path: str):
    new_img = Image.fromarray(array)
    new_img.save(path)


def main(infile, outfile):
    arr = img_to_array(infile)
    compressed_arr = compress(arr)
    save_array_as_img(compressed_arr, outfile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infile')
    parser.add_argument('outfile')
    args = parser.parse_args()
    main(args.infile, args.outfile)
