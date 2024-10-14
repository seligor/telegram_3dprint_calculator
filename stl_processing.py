from stl import mesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import art3d
import numpy as np
from matplotlib.colors import LightSource

def load_stl(file_path):
    """Загружает модель STL из файла."""
    return mesh.Mesh.from_file(file_path)

def visualize_stl(stl_mesh, output_path='stl_visualization.png'):
    """Визуализирует модель STL и сохраняет результат в указанный файл."""
    figure = plt.figure()
    axes = figure.add_subplot(111, projection='3d')

    # Получаем координаты всех вершин модели
    points = stl_mesh.points

    # Определяем границы модели
    min_x = points[:, 0].min()
    max_x = points[:, 0].max()
    min_y = points[:, 1].min()
    max_y = points[:, 1].max()
    min_z = points[:, 2].min()
    max_z = points[:, 2].max()

    # Определяем центр модели
    center_x = (max_x + min_x) / 2
    center_y = (max_y + min_y) / 2

    # Вычисляем смещения для центрирования по x и y
    offset_x = 127.5 - center_x
    offset_y = 105.0 - center_y

    # Смещаем модель так, чтобы центр совпадал с (127.5, 105) и нижняя точка была на уровне 0 по z
    stl_mesh.vectors[:, :, 0] += offset_x
    stl_mesh.vectors[:, :, 1] += offset_y
    stl_mesh.vectors[:, :, 2] -= min_z  # Смещение вниз, чтобы нижняя точка была на 0 по z

    # Создание источника света
    ls = LightSource(azdeg=315, altdeg=45)

    # Рассчитываем нормали для каждого треугольника
    normals = np.cross(
        stl_mesh.vectors[:, 1] - stl_mesh.vectors[:, 0],
        stl_mesh.vectors[:, 2] - stl_mesh.vectors[:, 0]
    )
    normals = normals / np.linalg.norm(normals, axis=1)[:, np.newaxis]

    # Применение освещения к нормалям
    intensity = ls.shade_normals(normals)
    # Преобразование интенсивности в RGB (с использованием оттенков серого)
    face_colors = np.repeat(intensity[:, np.newaxis], 3, axis=1)  # Измените 3 на 4, если требуется альфа-канал
    face_colors = np.hstack((face_colors, np.ones((face_colors.shape[0], 1))))  # Добавление альфа-канала

    # Создание коллекции с градиентной окраской
    collection = art3d.Poly3DCollection(stl_mesh.vectors, facecolors=face_colors, edgecolor='w', linewidths=0.001, alpha=0.9)
    axes.add_collection3d(collection)

    # Устанавливаем пределы по заданным размерам
    axes.set_xlim([0, 255])
    axes.set_ylim([0, 210])
    axes.set_zlim([0, 190])

    # Настраиваем оси
    axes.set_xlabel('X')
    axes.set_ylabel('Y')
    axes.set_zlabel('Z')
    axes.grid(True)  # Включаем сетку для понимания размера

    # Сохраняем изображение в файл
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
    plt.close(figure)
