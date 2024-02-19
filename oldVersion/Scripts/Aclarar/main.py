import numpy as np
import matplotlib.pyplot as plt

def fft2(image):
    return np.fft.fftshift(np.fft.fft2(image))

def ifft2(image):
    return np.fft.ifft2(np.fft.ifftshift(image))

def apply_homomorphic_filter(image, alpha=0.5, cutoff=50):
    # Convertir la imagen a escala de grises y luego a punto flotante
    gray_image = np.float32(image)
    
    # Aplicar la transformada logarítmica para aumentar el rango dinámico
    log_image = np.log1p(gray_image)
    
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

# Cargar la imagen y convertirla a escala de grises
image = plt.imread('homomorfico2.jpg')
gray_image = np.mean(image, axis=2)

# Aplicar el filtro homomórfico
filtered_image = apply_homomorphic_filter(gray_image)

# Mostrar la imagen original y la imagen filtrada
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(gray_image, cmap='gray')
plt.title('Original Image')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(filtered_image, cmap='gray')
plt.title('Filtered Image')
plt.axis('off')

plt.show()
