import numpy as np
from PIL import Image


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
    import cv2

    # # Cargar la imagen y convertirla a escala de grises
    # image = np.array(Image.open("homomorfico1.jpg"))

    # # Aplicar el filtro homomórfico
    # filtered_image = apply_homomorphic_filter(image)

    path = "D:\DocumentosUTEC\Books\Procesamiento de Imagenes Digitales\ImagEdit_PID\images\Lenna.png"
    original = cv2.imread(path, cv2.IMREAD_COLOR)
    # original = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
    print(type(original))
    filtered_image = apply_homomorphic_filter(original)
    print(f"Original: {original.shape}, Filtered: {filtered_image.shape}")
    print("success")
    cv2.imshow("Original", original)
    cv2.imshow("Filtered", filtered_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
