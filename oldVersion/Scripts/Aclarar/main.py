import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def ajuste_gamma(image, gamma=1.0):
    # Normalizar los valores de píxeles al rango [0, 1]
    image = image / 255.0
    # Aplicar la función de potencia gamma
    adjusted_image = np.power(image, gamma)
    # Escalar nuevamente los valores de píxeles al rango [0, 255]
    adjusted_image = (adjusted_image * 255).astype(np.uint8)
    return adjusted_image

# Cargar una imagen
image = Image.open('homomorfico1.jpg')

# Aplicar el ajuste gamma
gamma = 0.4  # Puedes ajustar este valor según tus necesidades
adjusted_image = ajuste_gamma(np.array(image), gamma)

# Mostrar la imagen original y la imagen ajustada
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(image)
plt.title('Original Image')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(adjusted_image)
plt.title('Adjusted Image (Gamma={})'.format(gamma))
plt.axis('off')

plt.show()