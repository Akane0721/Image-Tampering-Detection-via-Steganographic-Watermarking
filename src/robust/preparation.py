import numpy as np
from utils import arnold_transform


def prep_robust(Wrobust, K1, K2):
    """
    Prepare the encrypted watermark.
    :param Wrobust: 2D numpy array (binary watermark, size 32x32)
    :param K1: int, number of AT transform iterations
    :param K2: int, seed for random binary sequence
    :return: 2D numpy array, encrypted watermark (Wencrypted)
    """
    # Step 1: Apply AT transform (simulated as a series of flips)
    WAT = Wrobust.copy()
    for _ in range(K1):
        WAT = arnold_transform(WAT)  # Example AT transform: flip vertically & horizontally

    # Step 2: Generate random binary sequence
    np.random.seed(K2)
    Wran_1 = np.random.randint(0, 2, size=Wrobust.shape, dtype=np.uint8)

    # Step 3: Perform XOR operation
    Wencrypted = np.bitwise_xor(WAT, Wran_1)
    return Wencrypted
