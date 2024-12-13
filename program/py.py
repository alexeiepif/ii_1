#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Методом полного перебора решите задачу коммивояжёра h

import itertools
import json
from dataclasses import dataclass
from typing import Any

import numpy as np


@dataclass
class Nodes:
    nodes: dict[int, str]

    def __getitem__(self, key: int) -> str:
        return self.nodes.get(key, "")


@dataclass
class Edges:
    edges: dict[tuple[int, int], float]

    def __getitem__(self, key: tuple[int, int]) -> float:
        return self.edges.get(key) or self.edges.get(key[::-1]) or np.inf


def calculate_path_length(edges: Edges, path: list[int]) -> float:
    """
    Рассчитывает длину пути по матрице расстояний.
    """

    def find_edge_weight(source: int, target: int) -> float:
        edge_weight = edges[source, target]
        if edge_weight:
            return edge_weight
        return np.inf

    length = sum(find_edge_weight(i, j) for i, j in zip(path, path[1:]))
    length += find_edge_weight(path[-1], path[0])

    return length


def traveling_salesman(data: list[dict[str, Any]]) -> Any:
    """
    Решает задачу коммивояжёра методом полного перебора.
    """
    data = [x["data"] for x in data]
    node_count = len([x for x in data if "id" in x])
    nodes = Nodes({int(x["id"]): x["label"] for x in data[:node_count]})
    edges = Edges(
        {(int(x["source"]), int(x["target"])): x["weight"] for x in data[node_count:]}
    )

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

    shortest_path_named = []
    for i in shortest_path:
        name = nodes[i]
        if name:
            shortest_path_named.append(name)
    return shortest_path_named, shortest_path, min_length


if __name__ == "__main__":
    file_path = "data/graph2.xlsx"
    with open("json/elem_full.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    shortest_path_named, shortest_path, min_length = traveling_salesman(data)
    print(f"Самый короткий путь: {shortest_path_named}")
    print(f"Длина самого короткого пути: {min_length}")
