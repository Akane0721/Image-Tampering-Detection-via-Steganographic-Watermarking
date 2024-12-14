import numpy as np
from preparation import generate_random_sequence
from embedding import get_F_embed
from utils import padding, partition, block_height, block_width

from random import Random

def extr(watermarked_image, k3, k4):
    # [TODO: padding]
    blocks = partition(padding(watermarked_image))
    TB = len(blocks)
    
    # Generate W_ran_2 for comparison
    W_ran_2 = generate_random_sequence(TB, k3)
    #print("extr ran: ", W_ran_2)
    
    tampered_blocks = []
    EW_recovs = []
    for i, block in enumerate(blocks):
        F_ext = [get_F_embed(block[:, col]) for col in range(block_width)]
        extracted_digits = "".join([f"{f:03b}" for f in F_ext])

        EW_ran_2 = extracted_digits[:6]
        EW_recov = extracted_digits[6:]

        EW_recovs.append(int(EW_recov + "00", 2))
        
        # Compare to authenticate
        #print(EW_ran_2, W_ran_2[i])
        if EW_ran_2 != W_ran_2[i]:
            tampered_blocks.append(i)
            EW_recovs[-1] = -1
    
    # [TODO] Neighborhood smoothing
    num_blocks_row = watermarked_image.shape[0] // block_height
    num_blocks_col = watermarked_image.shape[1] // block_width
    tampered_coords = [
        (idx // num_blocks_col, idx % num_blocks_col) for idx in tampered_blocks
    ]

    smoothed_tampered = set()

    # Add surrounding blocks
    for row, col in tampered_coords:
        for dr in [-1, 0, 1]:  # row offset
            for dc in [-1, 0, 1]:  # column offset
                r, c = row + dr, col + dc
                if 0 <= r < num_blocks_row and 0 <= c < num_blocks_col:
                    smoothed_tampered.add((r, c))  # Convert back to 1D index

    smoothed_tampered = list(smoothed_tampered)

    TB = len(EW_recovs)
    order = Random(k4).sample(list(range(TB)), TB)

    EW_recovs_sorted = [0] * TB
    for i in range(TB):
        EW_recovs_sorted[order[i]] = EW_recovs[i]
    
    return smoothed_tampered, np.reshape(np.array(EW_recovs_sorted), (watermarked_image.shape[0] // block_height, -1))
