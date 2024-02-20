import numpy as np
import cv2, math, time


def get_rotation_matrix(angle_pitch, angle_yaw, angle_roll):
    theta_pitch, theta_yaw, theta_roll = (
        np.radians(angle_pitch),
        np.radians(angle_yaw),
        np.radians(angle_roll),
    )

    rotation_matrix_pitch = np.array(
        [
            [1, 0, 0],
            [0, math.cos(theta_pitch), -math.sin(theta_pitch)],
            [0, math.sin(theta_pitch), math.cos(theta_pitch)],
        ]
    )

    rotation_matrix_yaw = np.array(
        [
            [math.cos(theta_yaw), 0, math.sin(theta_yaw)],
            [0, 1, 0],
            [-math.sin(theta_yaw), 0, math.cos(theta_yaw)],
        ]
    )

    rotation_matrix_roll = np.array(
        [
            [math.cos(theta_roll), -math.sin(theta_roll), 0],
            [math.sin(theta_roll), math.cos(theta_roll), 0],
            [0, 0, 1],
        ]
    )

    return np.dot(
        rotation_matrix_pitch, np.dot(rotation_matrix_yaw, rotation_matrix_roll)
    )


def rotate_image(image, angle_roll, angle_pitch, angle_yaw):
    height, width = image.shape[:2]
    center = (width // 2, height // 2)

    # Matriz de rotación
    rotation_matrix = get_rotation_matrix(angle_pitch, angle_yaw, angle_roll)

    # Coordenadas de los píxeles en la imagen original
    y_coords, x_coords = np.mgrid[0:height, 0:width]
    coords = np.stack((x_coords - center[0], y_coords - center[1], np.zeros_like(x_coords)), axis=-1)
    
    # Aplicar rotacion y ajustar centro
    rotated_coords = np.dot(coords, rotation_matrix.T).astype(int)
    rotated_x_coords = rotated_coords[:, :, 0] + center[0]
    rotated_y_coords = rotated_coords[:, :, 1] + center[1]

    # Crear imagen rotada
    rotated_image = np.zeros_like(image)
    mask = (rotated_x_coords >= 0) & (rotated_x_coords < width) & (rotated_y_coords >= 0) & (rotated_y_coords < height)
    rotated_image[rotated_y_coords[mask], rotated_x_coords[mask]] = image[y_coords[mask], x_coords[mask]]

    return rotated_image

def rotate_image_opencv(image, angle_roll, angle_pitch, angle_yaw):
    rotation_matrix = get_rotation_matrix(angle_pitch, angle_yaw, angle_roll)
    rows, cols = image.shape[:2]
    center = (cols // 2, rows // 2)

    # Ajustar el centro como punto de referencia
    rotation_matrix[0, 2] += center[0] - center[0] * rotation_matrix[0, 0] - center[1] * rotation_matrix[0, 1]
    rotation_matrix[1, 2] += center[1] - center[0] * rotation_matrix[1, 0] - center[1] * rotation_matrix[1, 1]

    # Aplicar la rotación respecto al centro
    rotated_image = cv2.warpAffine(image, rotation_matrix[:2], (cols, rows), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))

    return rotated_image



if __name__ == "__main__":
    input_image_path = "C://Users//Claudia//Documents//01 UTEC stuff//PID//Proyecto//ImagEdit_PID//temp//images//test.jpg"
    output_rotated_image_path = "output_rotated_image.png"

    image = cv2.imread(input_image_path)

    start_time = time.time()

    # Uso de la función
    rotated_image = rotate_image(image, 120, 60, 122)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Rotacion completada en {execution_time:.5f} segundos")
    cv2.imwrite(output_rotated_image_path, rotated_image)
    cv2.imshow("Rotated Image", rotated_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    start_time = time.time()
    rotated_image2 = rotate_image_opencv(image, 120, 60, 122)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Rotacion completada en {execution_time:.5f} segundos")

    # Guardar imagen
    cv2.imwrite(output_rotated_image_path, rotated_image2)
    cv2.imshow("Rotated Image", rotated_image2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

