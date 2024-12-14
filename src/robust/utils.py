import numpy as np

def padding(image, block_height = 2, block_width = 4):
    pad_height = (block_height - (image.shape[0] % block_height)) % block_height
    pad_width = (block_width - (image.shape[1] % block_width)) % block_width

    image = np.pad(
        image,
        ((0, pad_height), (0, pad_width)),
        mode="constant",
        constant_values=0,
    )

    return image

def pad_to_square(image):
    h, w = image.shape
    size = max(h, w) 
    padded_image = np.zeros((size, size), dtype=image.dtype)
    padded_image[:h, :w] = image 
    return padded_image

def arnold_transform(image):
    """
    Apply Arnold Transform on a given image for K1 iterations.

    Parameters:
        image (ndarray): Input image (2D binary or grayscale array, e.g., 32x32).
        K1 (int): Number of iterations of Arnold Transform.

    Returns:
        ndarray: Image after K1 iterations of Arnold Transform.
    """
    image = pad_to_square(image)
    N = image.shape[0]
    transformed_image = np.copy(image) # no need?
    
    # Create a new array to store the transformed coordinates
    new_image = np.zeros_like(transformed_image)
    
    # Apply Arnold Transform for each pixel
    for x in range(N):
        for y in range(N):
            # Arnold Transform formula
            x_new = (x + y) % N
            y_new = (x + 2 * y) % N
            new_image[x_new, y_new] = transformed_image[x, y]
    
    return new_image

def inverse_arnold_transform(image):
    N = image.shape[0]
    transformed_image = np.copy(image)
    
    new_image = np.zeros_like(transformed_image)
    for x in range(N):
        for y in range(N):
            x_new = (2 * x - y) % N
            y_new = (-x + y) % N
            new_image[x_new, y_new] = transformed_image[x, y]

    return new_image

def smooth(image_height, image_width, block_height, block_width, tampered_blocks):
    num_blocks_row = image_height // block_height
    num_blocks_col = image_width // block_width
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
    return smoothed_tampered