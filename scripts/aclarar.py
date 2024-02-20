import numpy as np
from PIL import Image


def fft2(image):
    return np.fft.fftshift(np.fft.fft2(image))

def ifft2(image):
    return np.fft.ifft2(np.fft.ifftshift(image))

def apply_homomorphic_filter(image, alpha=0.5, cutoff=50):
    # Convertir la imagen a escala de grises y luego a punto flotante
    # gray_image = np.float32(image)
    
    # Aplicar la transformada logarítmica para aumentar el rango dinámico
    # log_image = np.log1p(gray_image)
    log_image = np.log1p(image)
    
    # Aplicar la transformada de Fourier bidimensional
    fft_image = fft2(log_image)
    
    # Filtrar el espectro de Fourier con un filtro homomórfico
    rows, cols = log_image.shape
    x = np.linspace(-0.5, 0.5, cols)
    y = np.linspace(-0.5, 0.5, rows)
    X, Y = np.meshgrid(x, y)
    
    H = alpha + (1 - alpha) * (1 - np.exp(-cutoff * ((X ** 2) + (Y ** 2))))
    filtered_fft_shifted = fft_image * H
    
    # Aplicar la transformada inversa de Fourier bidimensional
    filtered_image = ifft2(filtered_fft_shifted)
    
    # Calcular la magnitud de la parte real de la imagen filtrada
    filtered_image = np.abs(filtered_image)
    
    # Normalizar la imagen filtrada al rango 0-255
    filtered_image = (filtered_image - np.min(filtered_image)) / (np.max(filtered_image) - np.min(filtered_image)) * 255
    
    # Convertir la imagen de vuelta a tipo uint8
    filtered_image = np.uint8(filtered_image)
    
    return filtered_image


if __name__ == "__main__":
    # Cargar la imagen y convertirla a escala de grises
    image = Image.open('homomorfico1.jpg').convert('L')
    gray_image = np.array(image)

    # Aplicar el filtro homomórfico
    filtered_image = apply_homomorphic_filter(gray_image)
