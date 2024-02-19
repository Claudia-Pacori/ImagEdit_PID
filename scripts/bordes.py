import numpy as np
from PIL import Image


def gaussian_kernel(kernel_size, sigma):
    # Funcion del filtro gaussiano
    kernel = np.fromfunction(
        lambda x, y: (1 / (2 * np.pi * sigma**2))
        * np.exp(
            -((x - (kernel_size - 1) / 2) ** 2 + (y - (kernel_size - 1) / 2) ** 2)
            / (2 * sigma**2)
        ),
        (kernel_size, kernel_size),
    )
    return kernel / np.sum(kernel)


def convolucion(image, kernel):
    image_height, image_width = image.shape
    kernel_height, kernel_width = kernel.shape

    # Calcular el padding necesario
    pad_height = kernel_height // 2
    pad_width = kernel_width // 2

    output = np.zeros_like(image)

    # Pad de la imagen
    padded_image = np.pad(
        image, ((pad_height, pad_height), (pad_width, pad_width)), mode="constant"
    )

    # Convolucion
    for i in range(image_height):
        for j in range(image_width):
            output[i, j] = np.sum(
                padded_image[i : i + kernel_height, j : j + kernel_width] * kernel
            )

    return output


def gaussian_highpass_filter(image, kernel_size, sigma):
    kernel = gaussian_kernel(kernel_size, sigma)
    filtered_image = convolucion(image, kernel)
    highpass_image = image - filtered_image
    return highpass_image


if __name__ == "__main__":
    # Cargar imagen
    image = Image.open("Logo-UTEC.png").convert("L")

    # Convertir imagen a arreglo de numpy
    image = np.array(image)

    # Aolica el filtro de alta frecuencia
    kernel_size = 5
    sigma = 1.0
    highpass_image = gaussian_highpass_filter(image, kernel_size, sigma)
