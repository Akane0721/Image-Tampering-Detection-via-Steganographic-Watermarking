import numpy as np
import pywt
from utils import inverse_arnold_transform, smooth

def extract_robust(attacked_image, K1, K2, watermark):
    """
    Extract the robust watermark from the attacked image.
    :param attacked_image: 2D numpy array, the attacked image
    :param K1: int, number of AT transform iterations
    :param K2: int, seed for random binary sequence
    :param watermark: 2D numpy array, the original watermark (shape: (32, 32))
    """
    h, w = attacked_image.shape
    extracted_bits = []
    blocks = [(i, j) for i in range(0, h, 16) for j in range(0, w, 16)]
    watermark_flatten = watermark.flatten()
    tampered_blocks = []

    for idx, (i, j) in enumerate(blocks):
        block = attacked_image[i:i+16, j:j+16]
        coeffs = pywt.dwt2(block, 'haar')  # First level IWT
        _, (LH, HL, _) = coeffs
        _, (LH1, HL1, _) = pywt.dwt2(LH, 'haar')  # Second level IWT

        LH1_avg = np.mean(LH1)
        HL1_avg = np.mean(HL1)

        # Extract bit using comparison
        extracted_bit = 1 if HL1_avg > LH1_avg else 0
        extracted_bits.append(extracted_bit)

        if len(extracted_bits) >= np.prod(watermark.shape):
            break

    # Reshape bits into watermark shape and reverse encryption
    Wextracted = np.array(extracted_bits, dtype=np.uint8).reshape(watermark.shape)

    # Generate the same random binary sequence
    np.random.seed(K2)
    Wran_1 = np.random.randint(0, 2, size=watermark.shape, dtype=np.uint8)

    # Reverse XOR and AT transform to recover the original watermark
    WAT = np.bitwise_xor(Wextracted, Wran_1)
    for _ in range(K1):
        WAT = inverse_arnold_transform(WAT)  # Reverse AT transform
    
    WAT = WAT.flatten()
    for idx in range(len(WAT)):
        if WAT[idx] != watermark_flatten[idx]:
            tampered_blocks.append(idx)
            
    return smooth(h, w, 16, 16, tampered_blocks)