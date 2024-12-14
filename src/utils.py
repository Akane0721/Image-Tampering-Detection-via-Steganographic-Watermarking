import numpy as np

block_height, block_width = 2, 4

def partition(image):
    return [image[i:i+block_height, j:j+block_width] for i in range(0, image.shape[0], block_height) for j in range(0, image.shape[1], block_width)]

def padding(image):
    pad_height = (block_height - (image.shape[0] % block_height)) % block_height
    pad_width = (block_width - (image.shape[1] % block_width)) % block_width

    image = np.pad(
        image,
        ((0, pad_height), (0, pad_width)),
        mode="constant",
        constant_values=0,
    )

    return image
