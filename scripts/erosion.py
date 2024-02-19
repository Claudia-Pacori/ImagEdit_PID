import numpy as np
import cv2, time


def erode_image(input_image):
    # Kernel
    kernel = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]], dtype=np.uint8)

    # Erosión
    output_image = np.zeros_like(input_image)
    for i in range(2, input_image.shape[0] - 2):
        for j in range(2, input_image.shape[1] - 2):
            output_image[i, j] = np.min(
                input_image[i - 1 : i + 2, j - 1 : j + 2] * kernel
            )
    return output_image


if __name__ == "__main__":
    input_image_path = "temp.png"
    output_eroded_image_path = "output_dilated_image.png"

    # Escala de grises
    img = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)

    start_time = time.time()

    # Uso de la función
    eroded_image = erode_image(input_image_path)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Erosion completada en {execution_time:.5f} segundos")

    # Mostrar las imágenes# Guardar imagen
    cv2.imwrite(output_eroded_image_path, eroded_image)
    cv2.imshow("Eroded Image", eroded_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
