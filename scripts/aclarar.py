import numpy as np
from PIL import Image


def ajuste_gamma(image, gamma=1.0):
    # Normalizar los valores de píxeles al rango [0, 1]
    image = image / 255.0
    # Aplicar la función de potencia gamma
    adjusted_image = np.power(image, gamma)
    # Escalar nuevamente los valores de píxeles al rango [0, 255]
    adjusted_image = (adjusted_image * 255).astype(np.uint8)
    return adjusted_image


if __name__ == "__main__":
    # Cargar una imagen
    image = Image.open("homomorfico1.jpg")

    # Aplicar el ajuste gamma
    gamma = 0.4  # Puedes ajustar este valor según tus necesidades
    adjusted_image = ajuste_gamma(np.array(image), gamma)
