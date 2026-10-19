import random
import string
import sys
import time

import matplotlib.pyplot as plt

from avl import SearchTree
from dictionary import ArrayDictionary, LinkedListDictionary

sys.setrecursionlimit(20000)   # BST ที่เอียงเป็นเส้นตรงต้องใช้ recursion ลึก

SIZES = [250, 500, 1000, 2000, 4000]
NUM_QUERIES = 100


def make_keys(n):
    keys = set()
    while len(keys) < n:
        keys.add("".join(random.choices(string.ascii_lowercase, k=6)))
    return list(keys)


def build(structure, keys):
    for k in keys:
        structure.insert(k)
    return structure


def search_time_us(structure, queries):
    """เวลาค้นหาเฉลี่ยต่อคำ (ไมโครวินาที)"""
    start = time.perf_counter()
    for q in queries:
        structure.search(q)
    return (time.perf_counter() - start) / len(queries) * 1e6


def main():
    random.seed(1)
    names = ["Array", "Linked List", "BST (random order)",
             "BST (sorted order)", "AVL"]
    results = {name: [] for name in names}
    heights = {}

    print(f"{'n':>6} | " + " | ".join(f"{n:>18}" for n in names))
    for n in SIZES:
        keys = make_keys(n)
        shuffled = keys[:]
        random.shuffle(shuffled)
        ordered = sorted(keys)

        # คำที่มีอยู่ 50 คำ + คำที่ไม่มี 50 คำ
        queries = random.sample(keys, NUM_QUERIES // 2)
        queries += [k + "0" for k in random.sample(keys, NUM_QUERIES // 2)]

        structures = {
            "Array": build(ArrayDictionary(), shuffled),
            "Linked List": build(LinkedListDictionary(), shuffled),
            "BST (random order)": build(SearchTree(balanced=False), shuffled),
            "BST (sorted order)": build(SearchTree(balanced=False), ordered),
            "AVL": build(SearchTree(balanced=True), ordered),
        }

        row = []
        for name in names:
            t = search_time_us(structures[name], queries)
            results[name].append(t)
            row.append(f"{t:>16.2f}us")
        print(f"{n:>6} | " + " | ".join(row))

        if n == SIZES[-1]:
            for name in names[2:]:
                heights[name] = structures[name].height()

    print(f"\nTree height at n = {SIZES[-1]}:")
    for name, h in heights.items():
        print(f"  {name}: {h}")

    # วาดกราฟ
    plt.figure(figsize=(9, 5))
    for name in names:
        plt.plot(SIZES, results[name], marker="o", label=name)
    plt.yscale("log")
    plt.xlabel("Number of words (n)")
    plt.ylabel("Average search time per word (us, log scale)")
    plt.title("Search time comparison")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("benchmark.png", dpi=150)
    print("\nSaved chart to benchmark.png")
    plt.show()


if __name__ == "__main__":
    main()