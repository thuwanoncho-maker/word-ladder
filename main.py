import random
from graph import build_graph
from solver import bfs, dfs
from avl import SearchTree
from scores import Leaderboard, calc_score, show


def load_words(filename):
    with open(filename) as f:
        return [line.strip().lower() for line in f if line.strip()]


def pick_puzzle(words, graph, min_steps=3, max_steps=6):
    """สุ่มโจทย์: สองคำยาวเท่ากัน มีทางถึงกัน และความยาวทางอยู่ในช่วงที่กำหนด"""
    by_len = {}
    for w in words:
        by_len.setdefault(len(w), []).append(w)
    lengths = [n for n, group in by_len.items() if len(group) >= 2]

    for _ in range(5000):
        n = random.choice(lengths)
        a, b = random.sample(by_len[n], 2)
        path, _ = bfs(graph, a, b)
        if path and min_steps <= len(path) - 1 <= max_steps:
            return a, b
    return None


def play(start, goal, dictionary, graph):
    """เล่น 1 รอบ: ถ้าชนะคืนค่า (ก้าวที่ใช้, ก้าวที่สั้นสุด, จำนวน hint) ไม่งั้นคืน None"""
    current = start
    path = [start]
    hints = 0
    print(f"\nเปลี่ยนจาก {start} ไปเป็น {goal} ทีละ 1 ตัวอักษร")
    print("พิมพ์ hint = ขอคำใบ้, solve = ดูเฉลย, compare = เทียบ BFS/DFS, quit = ออก\n")

    while current != goal:
        guess = input(f"[{current}] -> ").strip().lower()

        if guess == "quit":
            return None
        elif guess == "hint":
            best, _ = bfs(graph, current, goal)
            print(f"คำใบ้: ลอง '{best[1]}'")
            hints += 1
        elif guess == "solve":
            best, explored = bfs(graph, current, goal)
            print("AI: " + " -> ".join(best))
            print(f"(BFS สำรวจไป {explored} คำ)")
            return None
        elif guess == "compare":
            b_path, b_explored = bfs(graph, current, goal)
            d_path, d_explored = dfs(graph, current, goal)
            print(f"BFS: {len(b_path) - 1} ก้าว, สำรวจ {b_explored} คำ")
            print(f"DFS: {len(d_path) - 1} ก้าว, สำรวจ {d_explored} คำ")
        elif not dictionary.search(guess):
            print("ไม่มีคำนี้ในพจนานุกรม")
        elif guess not in graph[current]:
            print("ต้องต่างจากคำเดิมแค่ 1 ตัวอักษร")
        else:
            current = guess
            path.append(guess)

    best, _ = bfs(graph, start, goal)
    steps, optimal = len(path) - 1, len(best) - 1
    print(f"\nชนะแล้ว! คุณใช้ {steps} ก้าว (ใช้คำใบ้ {hints} ครั้ง)")
    print("ทางของคุณ: " + " -> ".join(path))
    print(f"ทางสั้นสุด: {optimal} ก้าว: " + " -> ".join(best))
    if steps == optimal:
        print("สุดยอด! คุณหาทางสั้นสุดได้")
    return steps, optimal, hints


def main():
    words = load_words("words.txt")
    graph = build_graph(words)

    dictionary = SearchTree(balanced=True)   # พจนานุกรมเก็บใน AVL Tree
    for w in words:
        dictionary.insert(w)

    board = Leaderboard()                    # ตารางคะแนนเก็บใน AVL Tree

    while True:
        print("\n===== WORD LADDER =====")
        print("1) เล่นเกม")
        print("2) ตารางคะแนน (10 อันดับแรก)")
        print("3) รายชื่อผู้เล่น (เรียงตามชื่อ)")
        print("4) ลบคะแนนของผู้เล่น")
        print("5) ออก")
        choice = input("เลือก: ").strip()

        if choice == "1":
            puzzle = pick_puzzle(words, graph)
            if puzzle is None:
                print("ใน words.txt ยังมีคำไม่พอสำหรับสุ่มโจทย์")
                continue
            result = play(puzzle[0], puzzle[1], dictionary, graph)
            if result:
                steps, optimal, hints = result
                score = calc_score(steps, optimal, hints)
                print(f"คะแนนของคุณ: {score}")
                name = input("ชื่อผู้เล่น: ")
                board.add(name, score, puzzle[0], puzzle[1])
                print("\nอันดับปัจจุบัน:")
                show(board.top(5))
        elif choice == "2":
            print("\nตารางคะแนน:")
            show(board.top(10))
        elif choice == "3":
            print("\nเรียงตามชื่อ (Merge Sort):")
            show(board.by_name())
        elif choice == "4":
            name = input("ชื่อผู้เล่นที่จะลบ: ").strip()
            print(f"ลบแล้ว {board.remove_name(name)} รายการ")
        elif choice == "5":
            print("ลาก่อน!")
            break


if __name__ == "__main__":
    main()