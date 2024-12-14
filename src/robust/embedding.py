import numpy as np
import pywt
from utils import padding

def embed_robust(host_image, Wencrypted, alpha):
    """
    Embed the robust watermark (Wencrypted) into the host image.
    :param host_image: 2D numpy array, the host image
    :param Wencrypted: 2D numpy array (binary, size 32x32), encrypted watermark
    :param alpha: float, embedding parameter
    :return: 2D numpy array, watermarked image
    """
    host_image = padding(host_image, 16, 16)
    host_image = host_image.astype(np.float32)
    h, w = host_image.shape
    watermarked_image = host_image.copy()
    
    # Divide the host image into non-overlapping 16x16 blocks
    blocks = [(i, j) for i in range(0, h, 16) for j in range(0, w, 16)]
    watermark_bits = Wencrypted.flatten()
    
    for idx, (i, j) in enumerate(blocks):
        if idx >= len(watermark_bits):  # Stop if all bits are embedded
            break
        
        block = host_image[i:i+16, j:j+16]
        coeffs = pywt.dwt2(block, 'haar')  # First level IWT
        LL, (LH, HL, HH) = coeffs
        LL1, (LH1, HL1, HH1) = pywt.dwt2(LH, 'haar')  # Second level IWT   

        LH1_avg = np.mean(LH1)
        HL1_avg = np.mean(HL1)
        Mcoeff1 = (alpha - (HL1_avg - LH1_avg)) / 2
        Mcoeff2 = (alpha - (LH1_avg - HL1_avg)) / 2
        
        if watermark_bits[idx] == 1 and HL1_avg - LH1_avg < alpha:
            LH1 -= Mcoeff1
            HL1 += Mcoeff1
        elif watermark_bits[idx] == 0 and LH1_avg - HL1_avg < alpha:
            LH1 += Mcoeff2
            HL1 -= Mcoeff2
        
        # Inverse IWT twice to reconstruct the block
        LH = pywt.idwt2((LL1, (LH1, HL1, HH1)), 'haar')
        block = pywt.idwt2((LL, (LH, HL, HH)), 'haar')       
        watermarked_image[i:i+16, j:j+16] = block

    return watermarked_image
