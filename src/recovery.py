import numpy as np
from random import Random

from utils import block_height, block_width

def get_neighbors(block_idx, valid_blocks_set):
    """Find the valid neighbors of a given block."""
    i, j = block_idx
    neighbors = [
        (i - 1, j - 1), (i - 1, j), (i - 1, j + 1),
        (i, j - 1),                 (i, j + 1),
        (i + 1, j - 1), (i + 1, j), (i + 1, j + 1)
    ]
    return [nb for nb in neighbors if nb in valid_blocks_set]

def calculate_block_average(image, block_idx):
    """Calculate the average intensity of a block."""
    i, j = block_idx
    block = image[i * block_height:(i + 1) * block_height, j * block_width:(j + 1) * block_width]
    return np.mean(block)

def recover_reserved_feature_blocks(tampered_image, tampered_blocks, valid_blocks, EW_recovs_sorted):
    ruined_feature_blocks = []
    for i, j in tampered_blocks:
        if EW_recovs_sorted[i][j] != -1:
            tampered_image[i * block_height:(i + 1) * block_height, j * block_width:(j + 1) * block_width] = EW_recovs_sorted[i][j]

            valid_blocks.add((i, j))
        else:
            ruined_feature_blocks.append((i, j))
    return ruined_feature_blocks

def recover_ruined_feature_blocks(tampered_image, tampered_blocks, valid_blocks):
    for block_idx in tampered_blocks:
        neighbors = get_neighbors(block_idx, valid_blocks)
        if not neighbors:
            continue  # Skip if no valid neighbors

        # Compute average intensity for valid neighbors
        mu_values = [calculate_block_average(tampered_image, nb) for nb in neighbors]
        X = np.mean(mu_values)

        # Replace tampered block with average X
        i, j = block_idx
        tampered_image[i * block_height:(i + 1) * block_height, j * block_width:(j + 1) * block_width] = X

        # Mark this block as recovered
        valid_blocks.add(block_idx)
    
def recover_image(tampered_image, tampered_blocks, valid_blocks, EW_recovs_sorted):
    """
    Recover an image using the described ANBA process.
    
    Args:
        tampered_image (np.array): The tampered image as a 2D numpy array.
        tampered_blocks [unchanged] (list of tuple): List of (i, j) indices for tampered blocks.
        valid_blocks (set of tuple): set of (i, j) indices for non-tampered or recovered blocks.
    
    Returns:
        np.array: Recovered image.
    """
    
    # Recovery process
    ## reserved feature blocks
    ruined_feature_blocks = recover_reserved_feature_blocks(tampered_image, tampered_blocks, valid_blocks, EW_recovs_sorted)

    ## ruined feature blocks
    for _ in range(10):
        recover_ruined_feature_blocks(tampered_image, ruined_feature_blocks, valid_blocks)

    return tampered_image
