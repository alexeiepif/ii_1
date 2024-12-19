#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Методом полного перебора решите задачу коммивояжёра h

import itertools
import json
from typing import Any

import numpy as np


def calculate_path_length(
    edges: dict[tuple[int, int], float], path: list[int]
) -> float:
    """
    Рассчитывает длину пути по матрице расстояний.
    """

    length = sum(
        edges.get((i, j), 0) or edges.get((j, i), 0) or np.inf
        for i, j in zip(path, path[1:])
    )
    length += (
        edges.get((path[-1], path[0]), 0) or edges.get((path[0], path[-1]), 0) or np.inf
    )

    return length


def traveling_salesman(data: list[dict[str, Any]]) -> tuple[list[str], float]:
    """
    Решает задачу коммивояжёра методом полного перебора.
    """
    data = [x["data"] for x in data]
    node_count = sum(1 for x in data if "id" in x)
    nodes = {int(x["id"]): x["label"] for x in data[:node_count]}
    edges = {
        (int(x["source"]), int(x["target"])): x["weight"] for x in data[node_count:]
    }

    shortest_path = []
    min_length = np.inf

    permutations = [
        ([1] + list(perm)) for perm in itertools.permutations(range(2, node_count + 1))
    ]

    for perm in permutations:
        current_length = calculate_path_length(edges, perm)
        if current_length < min_length:
            min_length = current_length
            shortest_path = perm

    shortest_path_named: list[str] = []
    for i in shortest_path:
        name = nodes[i]
        if name:
            shortest_path_named.append(name)
    return shortest_path_named, min_length


if __name__ == "__main__":
    with open("json/elem_full.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    shortest_path_named, min_length = traveling_salesman(data)
    print(f"Самый короткий путь: {shortest_path_named}")
    print(f"Длина самого короткого пути: {min_length}")
