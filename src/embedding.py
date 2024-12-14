import numpy as np
from utils import padding, partition, block_width

def get_F_embed(unit):
    return (3**0 * unit[0] + 3**1 * unit[1]) % 3**2

def embed_watermark(image, watermark_bits):
    """
    Embed fragile watermark data into the given image.
    
    Parameters:
        image (np.ndarray): Grayscale image array.
        watermark_bits (list): List of 12-bit watermark data to embed in each block.
    
    Returns:
        np.ndarray: Watermarked image.
    """
    # Copy image to avoid modifying the original
    watermarked_image = image.copy()
    
    # Block size (2x4)
    watermarked_image = padding(watermarked_image)
    blocks = partition(watermarked_image)
    
    # Iterate over each block in the image
    for i, block in enumerate(blocks):
        
        # [TODO: maintain unchanged or warning?] Get the next 12-bit watermark data and convert to base-9 digits
        watermark_12bit = watermark_bits[i * 12 : (i + 1) * 12]

        watermark_4_base9 = [int(watermark_12bit[i: i + 3], 2) for i in range(0, 12, 3)]

        # Embed watermark in each unit (2 pixels) of the block
        units = [block[:, col] for col in range(block_width)]  # U1, U2, U3, U4
        for unit, digit in zip(units, watermark_4_base9):
            embed_digit_in_unit(unit, digit)
    

    # bit maybe < 0?
    return watermarked_image

def convert_to_base_digits(value, base, nfill):
    # range check
    if value < 0 or value >= base**nfill:
        raise Warning("Base conversion out of range!")
    return [int(digit) for digit in np.base_repr(value, base=base).zfill(nfill)]

def embed_digit_in_unit(unit, d):
    """
    Embed a base-9 digit into a 2-pixel unit according to the fragile embedding scheme.
    
    Parameters:
        unit (np.ndarray): Array containing 2 pixels of the unit.
        d (int): Base-9 digit to embed.
    """
    F_embed = get_F_embed(unit)
    
    # Calculate x
    n = 2
    x = (d - F_embed) % 3**n # simplified by 4 == (11)_3
    
    # Convert x to base-3
    x_base3 = convert_to_base_digits(x, 3, n)
    
    # Update unit pixels with x'' digits
    unit[0] += x_base3[1]
    unit[1] += x_base3[0]

# Example usage
# Load a grayscale image as a 2D numpy array (e.g., with OpenCV or PIL)
# image = np.array(...)  

# List of 12-bit watermark data for each block, e.g., [2456, 1234, ...]
# watermark_bits = [...]

# watermarked_image = embed_watermark(image, watermark_bits)
# Note: Save or display watermarked_image as needed.
