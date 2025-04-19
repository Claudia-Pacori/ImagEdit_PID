import numpy as np


def canny_edge_detection(image, sigma=0.8, low_threshold=10, high_threshold=90):
    # Aplicar suavizado Gaussiano para reducir el ruido
    smoothed = gaussian_smoothing(image, sigma)

    # Gradientes en dirección x e y
    sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

    # Convolución para calcular gradientes en ambas direcciones
    gradient_x = convolve_2d(smoothed, sobel_x)
    gradient_y = convolve_2d(smoothed, sobel_y)

    # Magnitud y dirección de gradiente
    magnitude = np.sqrt(gradient_x**2 + gradient_y**2)
    angle = np.arctan2(gradient_y, gradient_x) * (180 / np.pi)

    # Supresión de no máximos
    suppressed = non_maximum_suppression(magnitude, angle)

    # Umbralización de histéresis
    edges = hysteresis_thresholding(suppressed, low_threshold, high_threshold)

    return edges


def gaussian_kernel(size, sigma=1):
    kernel = np.fromfunction(
        lambda x, y: (1 / (2 * np.pi * sigma**2))
        * np.exp(
            -((x - (size - 1) / 2) ** 2 + (y - (size - 1) / 2) ** 2) / (2 * sigma**2)
        ),
        (size, size),
    )
    return kernel / np.sum(kernel)


def gaussian_smoothing(image, sigma):
    kernel = gaussian_kernel(5, sigma)
    smoothed = convolve_2d(image, kernel)
    return smoothed


def convolve_2d(image, kernel):
    # Realizar la convolución utilizando fft para mejorar la eficiencia
    return np.fft.ifftshift(
        np.real(np.fft.ifft2(np.fft.fft2(image) * np.fft.fft2(kernel, image.shape)))
    )


def non_maximum_suppression(magnitude, angle):
    angle[angle < 0] += 180
    suppressed = np.zeros_like(magnitude)

    for i in range(1, magnitude.shape[0] - 1):
        for j in range(1, magnitude.shape[1] - 1):
            q, r = 255, 255
            if (0 <= angle[i, j] < 22.5) or (157.5 <= angle[i, j] <= 180):
                q, r = magnitude[i, j + 1], magnitude[i, j - 1]
            elif 22.5 <= angle[i, j] < 67.5:
                q, r = magnitude[i + 1, j - 1], magnitude[i - 1, j + 1]
            elif 67.5 <= angle[i, j] < 112.5:
                q, r = magnitude[i + 1, j], magnitude[i - 1, j]
            elif 112.5 <= angle[i, j] < 157.5:
                q, r = magnitude[i - 1, j - 1], magnitude[i + 1, j + 1]

            suppressed[i, j] = (
                magnitude[i, j]
                if (magnitude[i, j] >= q) and (magnitude[i, j] >= r)
                else 0
            )

    return suppressed


def hysteresis_thresholding(image, low_threshold, high_threshold):
    strong_edges = image >= high_threshold
    weak_edges = (image <= high_threshold) & (image >= low_threshold)
    final_edges = np.zeros_like(image)
    final_edges[strong_edges] = 255

    for i in range(1, image.shape[0] - 1):
        for j in range(1, image.shape[1] - 1):
            if weak_edges[i, j] and np.any(strong_edges[i - 1 : i + 2, j - 1 : j + 2]):
                final_edges[i, j] = 255

    return final_edges.astype(np.uint8)


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

    @calculate_mean_time
    def detect_edges_with_canny(image, sigma, low_threshold, high_threshold):
        return canny_edge_detection(image, sigma, low_threshold, high_threshold)

    # Aplicar detección de bordes con Canny
    detect_edges_with_canny(image, sigma=1.4, low_threshold=20, high_threshold=60)

    # Aplicar detección de bordes con OpenCV
    @calculate_mean_time
    def detect_edges_with_opencv(image, low_threshold, high_threshold):
        return cv2.Canny(image, low_threshold, high_threshold)

    detect_edges_with_opencv(image, low_threshold=20, high_threshold=60)

    # Guardar la imagen edges
    # cv2.imwrite("images/edges.png", edges)
