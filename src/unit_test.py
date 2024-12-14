import numpy as np
from preparation import prep
from embedding import embed_watermark
from extraction import extr
from utils import block_height, block_width

from visualization import randomly_tamper_image, color_tampered_blocks, plot_detection_result

from recovery import recover_image

from PIL import Image

def getTampered(filename):
    host_im = Image.open(filename)   
    host_image = np.array(host_im)

    k3, k4 = 12345, 54321
    watermark = prep(host_image, k3, k4)
    watermarked_image = embed_watermark(host_image, watermark)

    tampered_image = watermarked_image
    for _ in range(3):
        tampered_image = randomly_tamper_image(tampered_image)
        
    tampered_blocks, EW_recovs_sorted = extr(tampered_image, k3, k4)

    return tampered_image, tampered_blocks, EW_recovs_sorted

def test_prep():
    # Test parameters
    host_image = np.random.randint(0, 256, (8, 8))  # 8x8 test image
    k3, k4 = 12345, 54321
    
    # Test watermark preparation
    watermark = prep(host_image, k3, k4)
    assert isinstance(watermark, str), "Watermark should be a binary string."

    assert len(watermark) == 12 * (host_image.size // (block_height * block_width)), "Incorrect watermark length."
    print("prep module passed.")

def test_embd():
    # Test parameters

    # host_image = np.random.randint(0, 256, (8, 8))  # 8x8 test image
    host_im = Image.open('253.tif')
    host_image = np.array(host_im)

    k3, k4 = 12345, 54321
    watermark = prep(host_image, k3, k4)
    
    # Test watermark embedding
    watermarked_image = embed_watermark(host_image, watermark)
    assert watermarked_image.shape == host_image.shape, "Watermarked image should match host image shape."
    print("embd module passed.")

    print(host_image[0])
    print(watermarked_image[0])

    host_im.show()
    Image.fromarray(watermarked_image).show()

def test_extr():
    # Test parameters
    # host_image = np.ones((8, 8), dtype=int)  # 8x8 test image
    host_im = Image.open('253.tif')   
    host_image = np.array(host_im)

    k3, k4 = 12345, 54321
    watermark = prep(host_image, k3, k4)
    watermarked_image = embed_watermark(host_image, watermark)

    #host_im.show()
    # Image.fromarray(watermarked_image).show()
    
    # Simulate tampering by modifying one block
    watermarked_image[0:block_height, 0:block_width] += 10
    
    # Test watermark extraction and tamper detection
    tampered_blocks, _ = extr(watermarked_image, k3, k4)
    assert len(tampered_blocks) > 0, "There should be at least one tampered block."

    n = watermarked_image.shape[1] // block_width
    print("Tampered blocks: in 2d: ", tampered_blocks)
    assert (0, 0) in tampered_blocks, "block 0 should be detected as tampered!"

    print("extr module passed.")

def test_visualization():

    tampered_image, tampered_blocks, _ = getTampered('253.tif')

    print(tampered_blocks)

    colored_image = color_tampered_blocks(tampered_image, tampered_blocks)

    plot_detection_result(tampered_image, colored_image)

def test_recovery():

    tampered_image, tampered_blocks, EW_recovs_sorted = getTampered('253.tif')

    valid_blocks = set([idx for idx in zip(range(tampered_image.shape[0] // block_height), range(tampered_image.shape[1] // block_width)) if idx not in tampered_blocks])

    recovered_image = tampered_image.copy()

    recover_image(recovered_image, tampered_blocks, valid_blocks, EW_recovs_sorted)

    plot_detection_result(tampered_image, recovered_image, "recovery")

def run_tests():
    # test_prep()
    # test_embd()
    test_extr()
    #test_visualization()
    test_recovery()
    print("All tests passed.")

# Running tests
run_tests()
