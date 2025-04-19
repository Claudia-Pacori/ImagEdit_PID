import time

import cv2
import numpy as np


def erode_image(input_image_path, output_eroded_image_path):
    # Escala de grises
    img = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)

    # Kernel
    kernel = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]], dtype=np.uint8)

    start_time = time.time()

    # Erosión
    eroded_image = np.zeros_like(img)
    for i in range(2, img.shape[0] - 2):
        for j in range(2, img.shape[1] - 2):
            eroded_image[i, j] = np.min(img[i - 1 : i + 2, j - 1 : j + 2] * kernel)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Erosion completada en {execution_time:.5f} segundos")

    # Mostrar las imágenes# Guardar imagen
    cv2.imwrite(output_eroded_image_path, eroded_image)
    cv2.imshow("Eroded Image", eroded_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Uso de la función
erode_image("temp.png", "output_eroded_image.png")
