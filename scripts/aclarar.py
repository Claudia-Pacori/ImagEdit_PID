import numpy as np


def fft2(image):
    return np.fft.fftshift(np.fft.fft2(image))


def ifft2(image):
    return np.fft.ifft2(np.fft.ifftshift(image))


def apply_homomorphic_filter(image, alpha=0.2, cutoff=50):
    # Separar los canales de color
    r, g, b = image[:, :, 0], image[:, :, 1], image[:, :, 2]

    # Aplicar el filtro homomórfico a cada canal por separado
    filtered_r = apply_filter(r, alpha, cutoff)
    filtered_g = apply_filter(g, alpha, cutoff)
    filtered_b = apply_filter(b, alpha, cutoff)

    # Combinar los canales filtrados para obtener la imagen en color
    filtered_image = np.stack((filtered_r, filtered_g, filtered_b), axis=2)

    # Normalizar los valores entre 0 y 255
    filtered_image = (
        (filtered_image - np.min(filtered_image))
        / (np.max(filtered_image) - np.min(filtered_image))
        * 255
    )

    # Convertir la imagen de vuelta a tipo uint8
    filtered_image = np.uint8(filtered_image)
    return filtered_image


def apply_filter(channel, alpha, cutoff):
    # Aplicar la transformada logarítmica para aumentar el rango dinámico
    log_channel = np.log1p(channel)

    # Aplicar la transformada de Fourier bidimensional
    fft_channel = fft2(log_channel)

    # Filtrar el espectro de Fourier con un filtro homomórfico
    rows, cols = log_channel.shape
    x = np.linspace(-0.5, 0.5, cols)
    y = np.linspace(-0.5, 0.5, rows)
    X, Y = np.meshgrid(x, y)

    H = alpha + (1 - alpha) * (1 - np.exp(-cutoff * ((X**2) + (Y**2))))
    filtered_fft_shifted = fft_channel * H

    # Aplicar la transformada inversa de Fourier bidimensional
    filtered_channel = ifft2(filtered_fft_shifted)

    # Calcular la magnitud de la parte real de la imagen filtrada
    filtered_channel = np.abs(filtered_channel)

    return filtered_channel


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
    image = cv2.imread("images/lena.png", cv2.IMREAD_COLOR)

    # Filtro manual
    @calculate_mean_time
    def manual_homomorphic_filter(image, alpha, cutoff):
        return apply_homomorphic_filter(image, alpha, cutoff)

    manual_homomorphic_filter(image, alpha=0.2, cutoff=50)

    # # Filtro con OpenCV
    # @calculate_mean_time
    # def opencv_homomorphic_filter(image, alpha, cutoff):
    #     return cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(image)

    # opencv_homomorphic_filter(image, alpha=0.2, cutoff=50)

    image_out = apply_homomorphic_filter(image, alpha=0.2, cutoff=50)
    cv2.imwrite("images/lena_homomorphic.png", image_out)
