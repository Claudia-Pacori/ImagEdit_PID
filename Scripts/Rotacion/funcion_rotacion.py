import numpy as np
import cv2, math, time

def get_rotation_matrix(angle_pitch, angle_yaw, angle_roll):
    theta_pitch, theta_yaw, theta_roll = np.radians(angle_pitch), np.radians(angle_yaw), np.radians(angle_roll)

    rotation_matrix_pitch = np.array([[1, 0, 0],
                                      [0, math.cos(theta_pitch), -math.sin(theta_pitch)],
                                      [0, math.sin(theta_pitch), math.cos(theta_pitch)]])

    rotation_matrix_yaw = np.array([[math.cos(theta_yaw), 0, math.sin(theta_yaw)],
                                    [0, 1, 0],
                                    [-math.sin(theta_yaw), 0, math.cos(theta_yaw)]])

    rotation_matrix_roll = np.array([[math.cos(theta_roll), -math.sin(theta_roll), 0],
                                     [math.sin(theta_roll), math.cos(theta_roll), 0],
                                     [0, 0, 1]])

    return np.dot(rotation_matrix_pitch, np.dot(rotation_matrix_yaw, rotation_matrix_roll))

def get_dimensions(rotation_matrix, width, height):
    corners = np.array([[0, 0], [0, height], [width, height], [width, 0]], dtype=np.float32)
    rotated_corners = np.dot(rotation_matrix[:2, :2], corners.T).T + rotation_matrix[:2, 2]

    rotated_width = int(np.ceil(max(rotated_corners[:, 0]) - min(rotated_corners[:, 0])))
    rotated_height = int(np.ceil(max(rotated_corners[:, 1]) - min(rotated_corners[:, 1])))

    return rotated_width, rotated_height

def rotate_image(input_image_path, output_image_path, angle_pitch, angle_yaw, angle_roll):
    image = cv2.imread(input_image_path)
    height, width = image.shape[:2]
    start_time = time.time()

    # Matriz de rotación
    rotation_matrix = get_rotation_matrix(angle_pitch, angle_yaw, angle_roll)

    # Dimensiones de imagen rotada
    rotated_width, rotated_height = get_dimensions(rotation_matrix, width, height)
    
    # Crear imagen
    rotated_image = np.zeros((rotated_height, rotated_width, 3), dtype=np.uint8)
    y_coords, x_coords = np.mgrid[0:height, 0:width] # Coordenadas originales
    coords = np.vstack((x_coords.flatten(), y_coords.flatten(), np.ones(height*width)))

    new_coords = np.dot(rotation_matrix, coords) # Rotacion
    new_coords = new_coords[:2, :].astype(int)

    mask = (new_coords[0, :] >= 0) & (new_coords[0, :] < rotated_image.shape[1]) & \
           (new_coords[1, :] >= 0) & (new_coords[1, :] < rotated_image.shape[0])

    rotated_coords = np.round(new_coords[:, mask]).astype(int)
    original_coords = np.round(coords[:2, mask]).astype(int)

    # Ajustar dimensiones
    rotated_image[rotated_coords[1, :], rotated_coords[0, :]] = image[original_coords[1, :], original_coords[0, :]]

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Rotacion completada en {execution_time:.5f} segundos")

    # Guardar imagen
    cv2.imwrite(output_image_path, rotated_image)
    cv2.imshow("Rotated Image", rotated_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Uso de la función
# Pitch - Yaw - Roll (-90, 90)
rotate_image("temp.png", "output_rotated_image.png", 60, 60, 30)