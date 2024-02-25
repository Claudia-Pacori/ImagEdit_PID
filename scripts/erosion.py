import numpy as np
import cv2, time


def erode_image(input_image):
    height, width = input_image.shape
    padded_image = [[0] * (width + 2)]  # Primera fila de ceros
    padded_image.extend([[0] + list(row) + [0] for row in input_image])  # Añadir ceros a cada fila
    padded_image.append([0] * (width + 2))  # Última fila de ceros

    kernel = np.ones((3, 3), np.uint8)

    # Erosion
    output_image = np.zeros_like(input_image)
    for i in range(1, height + 1):
        for j in range(1, width + 1):
            # Por ventanas
            neighbors = [padded_image[i + k][j + l] * kernel[k, l]
                         for k in range(-1, 2) for l in range(-1, 2)]
            output_image[i - 1, j - 1] = min(neighbors)

    #print(input_image.shape, output_image.shape)
    return output_image


def erode_image_opencv(input_image):
    kernel = np.ones((3, 3), np.uint8)
    eroded_image = cv2.erode(input_image, kernel, iterations=1)

    return eroded_image

if __name__ == "__main__":
    input_image_path = "temp/images/test.png"
    img = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)

    # Erosion manual
    manual_total_time = 0
    for _ in range(10):
        start_time = time.time()
        eroded_image = erode_image(img)
        end_time = time.time()
        execution_time = end_time - start_time
        manual_total_time += execution_time
    manual_avg_time = manual_total_time * 10
    print(f"Erosion manual - Promedio de tiempo: {manual_avg_time:.3f} ms")

    # Erosion con OpenCV
    opencv_total_time = 0
    for _ in range(10):
        start_time = time.time()
        eroded_image = erode_image_opencv(img)
        end_time = time.time()
        execution_time = end_time - start_time
        opencv_total_time += execution_time
    opencv_avg_time = opencv_total_time * 10
    print(f"Erosion con OpenCV - Promedio de tiempo: {opencv_avg_time:.3f} ms")