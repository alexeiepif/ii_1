#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Методом полного перебора решите задачу коммивояжёра

import itertools
import json

import numpy as np
import pandas as pd


def read_matrix_from_excel(file_path):
    """
    Считывает матрицу из Excel файла.
    """

    df = pd.read_excel(file_path, header=None)
    city_names = df.iloc[0, 1:11].tolist()
    df = df.iloc[1:11, 1:11]
    matrix = df.values
    return matrix, city_names


def lower_triangle_to_full_matrix(lower_triangle_matrix: np.ndarray):
    """
    Преобразует нижнюю треугольную матрицу в полную симметричную матрицу.
    """

    num_cities = lower_triangle_matrix.shape[0]
    full_matrix = np.zeros((num_cities, num_cities))

    for i in range(num_cities):
        for j in range(i + 1):
            full_matrix[i][j] = lower_triangle_matrix[i][j]
            full_matrix[j][i] = lower_triangle_matrix[i][j]  # Симметрично

    return full_matrix


def preprocess_matrix(matrix):
    """
    Преобразует знаки '-' в 0 в матрице
    и возвращает матрицу с числовыми значениями.
    """

    matrix = np.where(matrix == "-", 0, matrix)
    return matrix.astype(float)


def calculate_path_length(matrix, path):
    """
    Рассчитывает длину пути по матрице расстояний.
    """

    length = 0
    for i in range(len(path) - 1):
        k = matrix[path[i]][path[i + 1]]
        if np.isnan(k):
            return np.inf

        length += k
    length += matrix[path[-1]][path[0]]
    return length


def traveling_salesman(matrix, names_cities):
    """
    Решает задачу коммивояжёра методом полного перебора.
    """

    num_cities = len(matrix)
    cities = list(range(num_cities))
    shortest_path = None
    min_length = np.inf

    permutations = [
        ([0] + list(perm)) for perm in itertools.permutations(cities[1:])
    ]

    for perm in permutations:
        current_length = calculate_path_length(matrix, perm)
        if current_length < min_length:
            min_length = current_length
            shortest_path = perm

    shortest_path_named = [names_cities[i] for i in shortest_path]
    return shortest_path_named, shortest_path, min_length


if __name__ == "__main__":
    file_path = (
        "/Users/aleksejepifanov/Desktop/пары/пары_5_сем/ИИвПС/graph2.xlsx"
    )
    lower_triangle_matrix, names_cities = read_matrix_from_excel(file_path)
    processed_matrix = preprocess_matrix(lower_triangle_matrix)
    full_matrix = lower_triangle_to_full_matrix(processed_matrix)
    print(full_matrix)

    shortest_path_named, shorted_path, min_length = traveling_salesman(
        full_matrix, names_cities
    )

    with open("kommivoyager_path.json", "w") as f:
        json.dump(shorted_path, f)

    print(f"Самый короткий путь: {shortest_path_named},")
    print(f"Длина самого короткого пути: {min_length}")
