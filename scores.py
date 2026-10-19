import os
import time

from avl import SearchTree

SCORE_FILE = "scores.txt"


def calc_score(steps, optimal, hints):
    """คะแนนเต็ม 100 หักตามก้าวที่เกินและจำนวนคำใบ้"""
    return max(0, 100 - 10 * (steps - optimal) - 15 * hints)


def merge_sort(items, key):
    """Merge Sort: แบ่งครึ่งแบบ recursion แล้วรวมกลับ O(n log n)"""
    if len(items) <= 1:
        return items
    mid = len(items) // 2
    left = merge_sort(items[:mid], key)
    right = merge_sort(items[mid:], key)

    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


class Leaderboard:
    def __init__(self):
        self.tree = SearchTree(balanced=True)
        self.load()

    # entry = (-score, name, time, start, goal)
    def add(self, name, score, start, goal):
        name = name.replace("|", " ").strip() or "player"
        self.tree.insert((-score, name, time.time(), start, goal))
        self.save()

    def top(self, n=5):
        return self.tree.to_list()[:n]            # in-order = คะแนนสูงไปต่ำ

    def by_name(self):
        return merge_sort(self.tree.to_list(), key=lambda e: e[1].lower())

    def remove_name(self, name):
        targets = [e for e in self.tree.to_list() if e[1] == name]
        for e in targets:
            self.tree.delete(e)
        self.save()
        return len(targets)

    def save(self):
        with open(SCORE_FILE, "w", encoding="utf-8") as f:
            for neg, name, t, start, goal in self.tree.to_list():
                f.write(f"{-neg}|{name}|{t}|{start}|{goal}\n")

    def load(self):
        if not os.path.exists(SCORE_FILE):
            return
        with open(SCORE_FILE, encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) == 5:
                    score, name, t, start, goal = parts
                    self.tree.insert((-int(score), name, float(t), start, goal))


def show(entries):
    if not entries:
        print("  (ยังไม่มีคะแนน)")
        return
    for rank, (neg, name, _, start, goal) in enumerate(entries, 1):
        print(f"  {rank:>2}. {name:<12} {-neg:>3} คะแนน   ({start} -> {goal})")