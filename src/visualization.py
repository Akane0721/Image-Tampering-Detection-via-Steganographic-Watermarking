from utils import block_height, block_width
import matplotlib.pyplot as plt
import random

def randomly_tamper_image(image, min_size=(20, 40)):
    """
    Randomly tamper an image by selecting a rectangular area with size > min_size and coloring it white.

    Args:
    - image (numpy.ndarray): The input image (H, W, C).
    - min_size (tuple): Minimum size (height, width) of the tampered area.

    Returns:
    - numpy.ndarray: The tampered image.
    - tuple: Coordinates of the tampered area (start_y, start_x, end_y, end_x).
    """
    # Get image dimensions
    height, width = image.shape
    min_height, min_width = min_size

    # Ensure the tampered area fits within the image
    if height < min_height or width < min_width:
        raise ValueError("Image is too small for the specified tampered area size.")

    # Randomly select top-left corner of the tampered area
    start_y = random.randint(0, height - min_height)
    start_x = random.randint(0, width - min_width)

    # Randomly determine size of the tampered area
    end_y = random.randint(start_y + min_height, min(height, start_y + min_height + 50))
    end_x = random.randint(start_x + min_width, min(width, start_x + min_width + 100))

    # Create a copy of the image to modify
    tampered_image = image.copy()

    # Color the selected area white
    tampered_image[start_y:end_y, start_x:end_x] = 255  # White in RGB

    return tampered_image


def color_tampered_blocks(image, tampered_blocks):
    """
    Color tampered blocks in the image black.
    
    Args:
    - image (numpy.ndarray): The input image (H, W, C).
    - tampered_blocks (list of tuples): List of (row, col) indices of tampered blocks.
    - block_size (tuple): Size of each block (height, width).

    Returns:
    - numpy.ndarray: Image with tampered blocks colored black.
    """
    # Create a copy of the image to modify
    output_image = image.copy()
    
    for row, col in tampered_blocks:
        # Calculate the block's top-left and bottom-right corners
        start_y, start_x = row * block_height, col * block_width
        end_y, end_x = start_y + block_height, start_x + block_width
        
        # Color the block black
        output_image[start_y:end_y, start_x:end_x] = 0  # Black is [0, 0, 0] in RGB
    
    return output_image

def plot_detection_result(tampered_image, result_image, recovery = False):
    # Plot the original and result side by side
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))

    # Original image
    axs[0].imshow(tampered_image, cmap='gray', vmin=0, vmax=255)
    axs[0].set_title('Original Tampered Image(Randomly Whited Out)')
    axs[0].axis('off')

    # Result image
    axs[1].imshow(result_image, cmap='gray', vmin=0, vmax=255)
    axs[1].set_title('Detected Tampered Blocks(Blacked Out)' if not recovery else "Recoverd Image")
    axs[1].axis('off')

    plt.savefig('result.png')

    # Show the subplot
    plt.tight_layout()
    plt.show()
