import numpy as np
from preparation import prep_robust
from embedding import embed_robust
from extraction import extract_robust

from PIL import Image

    
def test_robust():
    K1, K2 = 5, 42
    np.random.seed(K1)
    Wrobust = np.random.randint(0, 2, size=(32, 32), dtype=np.uint8)
    host_im = Image.open('src/253.tif')   
    host_image = np.array(host_im)
    alpha = 0.1

    Wencrypted = prep_robust(Wrobust, K1, K2)
    watermarked_image = embed_robust(host_image, Wencrypted, alpha)
    Image.fromarray(watermarked_image).show()

    # Simulate tampering by modifying one block
    watermarked_image[0:5, 0:16] += 10
    
    # Test watermark extraction and tamper detection
    tampered_blocks = extract_robust(watermarked_image, K1, K2, Wrobust)
    assert len(tampered_blocks) > 0, "There should be at least one tampered block."
    print("Tampered blocks: in 2d: ", tampered_blocks)
    assert (0, 0) in tampered_blocks, "block 0 should be detected as tampered!"

def test_AT():
    from utils import arnold_transform, inverse_arnold_transform
    host_im = Image.open('src/253.tif')   
    original_image = np.array(host_im)
    K1 = 5
    K2 = 42
    transformed_image = original_image.copy()
    for _ in range(K1):
        transformed_image = arnold_transform(transformed_image)
        
    np.random.seed(K2)
    Wran_1 = np.random.randint(0, 2, size=transformed_image.shape, dtype=np.uint8)
    transformed_image = np.bitwise_xor(transformed_image, Wran_1)

    recovered_image = transformed_image.copy()
    np.random.seed(K2)
    Wran_1 = np.random.randint(0, 2, size=recovered_image.shape, dtype=np.uint8)
    recovered_image = np.bitwise_xor(recovered_image, Wran_1)
    for _ in range(K1):
        recovered_image = inverse_arnold_transform(recovered_image)
    
    recovered_image=recovered_image[:original_image.shape[0], :original_image.shape[1]]

    print(original_image.shape, recovered_image.shape)
    print(np.array_equal(original_image, recovered_image))

def run_tests():
    test_robust()
    #test_AT()
    print("All tests passed.")

# Running tests
run_tests()
