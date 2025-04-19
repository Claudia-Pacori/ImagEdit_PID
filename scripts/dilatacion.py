import time

import cv2
import numpy as np


def dilate_image(input_image):
    height, width = input_image.shape
    # Primera fila de ceros
    padded_image = [[0] * (width + 2)]
    # Añadir ceros a cada fila
    padded_image.extend([[0] + list(row) + [0] for row in input_image])
    # Última fila de ceros
    padded_image.append([0] * (width + 2))
    kernel = np.ones((3, 3), np.uint8)

    # Dilatacion
    output_image = np.zeros_like(input_image)
    for i in range(1, height + 1):
        for j in range(1, width + 1):
            # Por ventanas
            neighbors = [
                padded_image[i + k][j + col] * kernel[k, col]
                for k in range(-1, 2)
                for col in range(-1, 2)
            ]
            output_image[i - 1, j - 1] = max(neighbors)

    return output_image


def dilate_image_opencv(input_image):
    kernel = np.ones((3, 3), np.uint8)
    dilated_image = cv2.dilate(input_image, kernel, iterations=1)

    return dilated_image


if __name__ == "__main__":
    import time

    import cv2

    def calculate_mean_time(func):
        def wrapper(*args, **kwargs):
            times = []
            for _ in range(10):
                start_time = time.perf_counter()
                func(*args, **kwargs)
                end_time = time.perf_counter()
                times.append(end_time - start_time)

            mean_time = sum(times) / len(times)
            print(f"Mean time: {1000 * mean_time:.2f} milliseconds")

        return wrapper

    # Cargar la imagen
    image = cv2.imread("images/lena.png", cv2.IMREAD_GRAYSCALE)

    # Dilatacion manual
    @calculate_mean_time
    def manual_dilation():
        return dilate_image(image)

    # Dilatacion con OpenCV
    @calculate_mean_time
    def opencv_dilation():
        return dilate_image_opencv(image)

    # Aplicar dilatacion manual
    manual_dilation()

    # Aplicar dilatacion con OpenCV
    opencv_dilation()

    # Guardar la imagen dilatada
    img_output = dilate_image(image)
    cv2.imwrite("images/lena_dilated.png", img_output)
