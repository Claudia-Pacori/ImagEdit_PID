import time

import cv2
import numpy as np


def dilate_image(input_image_path, output_dilated_image_path):
    # Escala de grises
    img = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)

    # Kernel
    kernel = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]], dtype=np.uint8)

    start_time = time.time()

    # Dilatación
    dilated_image = np.zeros_like(img)
    for i in range(2, img.shape[0] - 2):
        for j in range(2, img.shape[1] - 2):
            dilated_image[i, j] = np.max(img[i - 1 : i + 2, j - 1 : j + 2] * kernel)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Dilatacion completada en {execution_time:.5f} segundos")

    # Guardar imagen
    cv2.imwrite(output_dilated_image_path, dilated_image)
    cv2.imshow("Dilated Image", dilated_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Uso de la función
dilate_image("temp.png", "output_dilated_image.png")
