import os

import streamlit as st

from avl import SearchTree
from graph import build_graph
from main import load_words, pick_puzzle
from scores import Leaderboard, calc_score
from solver import bfs, dfs

st.set_page_config(page_title="Word Ladder", page_icon="🪜")


@st.cache_resource
def load_resources():
    """โหลดคำ สร้างกราฟ AVL พจนานุกรม และตารางคะแนน ครั้งเดียวต่อเซิร์ฟเวอร์"""
    words = load_words("words.txt")
    graph = build_graph(words)
    dictionary = SearchTree(balanced=True)
    for w in words:
        dictionary.insert(w)
    board = Leaderboard()
    return words, graph, dictionary, board


words, graph, dictionary, board = load_resources()


# ---------- ตรรกะเกม (ใช้โค้ดเดิมทั้งหมด) ----------
def new_game():
    puzzle = pick_puzzle(words, graph)
    if puzzle is None:
        st.session_state.game = None
        return
    start, goal = puzzle
    st.session_state.game = {
        "start": start, "goal": goal, "current": start, "path": [start],
        "hints": 0, "status": "playing", "saved": False,
        "msg": None, "solution": None,
    }


def do_guess():
    g = st.session_state.game
    guess = st.session_state.guess_input.strip().lower()
    if not guess:
        return
    if not dictionary.search(guess):                 # ค้นใน AVL Tree
        g["msg"] = ("error", "ไม่มีคำนี้ในพจนานุกรม")
    elif guess not in graph[g["current"]]:
        g["msg"] = ("error", "ต้องต่างจากคำเดิมแค่ 1 ตัวอักษร")
    else:
        g["current"] = guess
        g["path"].append(guess)
        g["msg"] = None
        if guess == g["goal"]:
            g["status"] = "won"


def do_hint():
    g = st.session_state.game
    best, _ = bfs(graph, g["current"], g["goal"])
    g["hints"] += 1
    g["msg"] = ("info", f"คำใบ้: ลอง '{best[1]}'")


def do_compare():
    g = st.session_state.game
    b_path, b_exp = bfs(graph, g["current"], g["goal"])
    d_path, d_exp = dfs(graph, g["current"], g["goal"])
    g["msg"] = ("info",
                f"**BFS:** {len(b_path) - 1} ก้าว, สำรวจ {b_exp} คำ\n\n"
                f"**DFS:** {len(d_path) - 1} ก้าว, สำรวจ {d_exp} คำ")


def do_solve():
    g = st.session_state.game
    best, explored = bfs(graph, g["current"], g["goal"])
    g["solution"] = (best, explored)
    g["status"] = "gave_up"


def rows(entries):
    return [{"ลำดับ": i, "ผู้เล่น": e[1], "คะแนน": -e[0],
             "โจทย์": f"{e[3]} → {e[4]}"}
            for i, e in enumerate(entries, 1)]


if "game" not in st.session_state:
    new_game()

# ---------- หน้าเว็บ ----------
st.title("🪜 Word Ladder")
st.caption("เปลี่ยนคำทีละ 1 ตัวอักษร ให้ถึงคำเป้าหมายในก้าวน้อยที่สุด")

tab_play, tab_board, tab_info = st.tabs(["เล่นเกม", "ตารางคะแนน", "เบื้องหลังโปรแกรม"])

# ----- แท็บเล่นเกม -----
with tab_play:
    g = st.session_state.game
    if g is None:
        st.warning("ใน words.txt ยังมีคำไม่พอสำหรับสุ่มโจทย์")
    else:
        st.subheader(f"{g['start']}  →  {g['goal']}")
        st.write("ทางที่เดินมา: " + " → ".join(g["path"]))

        if g["status"] == "playing":
            st.markdown(f"คำปัจจุบัน: **{g['current']}**")
            with st.form("guess_form", clear_on_submit=True):
                st.text_input("พิมพ์คำถัดไป", key="guess_input")
                st.form_submit_button("ส่งคำ", on_click=do_guess)

            c1, c2, c3 = st.columns(3)
            c1.button("💡 ขอคำใบ้", on_click=do_hint, use_container_width=True)
            c2.button("⚖️ เทียบ BFS/DFS", on_click=do_compare, use_container_width=True)
            c3.button("🏳️ ดูเฉลย", on_click=do_solve, use_container_width=True)

            if g["msg"]:
                getattr(st, g["msg"][0])(g["msg"][1])

        elif g["status"] == "won":
            best, _ = bfs(graph, g["start"], g["goal"])
            steps, optimal = len(g["path"]) - 1, len(best) - 1
            score = calc_score(steps, optimal, g["hints"])
            st.success(f"ชนะแล้ว! ใช้ {steps} ก้าว (ทางสั้นสุด {optimal} ก้าว, "
                       f"ใช้คำใบ้ {g['hints']} ครั้ง) ได้ {score} คะแนน")
            st.write("ทางสั้นสุดของ AI: " + " → ".join(best))
            if not g["saved"]:
                with st.form("save_form"):
                    name = st.text_input("ชื่อผู้เล่น")
                    if st.form_submit_button("บันทึกคะแนน"):
                        board.add(name, score, g["start"], g["goal"])
                        g["saved"] = True
                        st.rerun()
            else:
                st.info("บันทึกคะแนนแล้ว ดูได้ที่แท็บตารางคะแนน")

        else:  # gave_up
            best, explored = g["solution"]
            st.info("AI: " + " → ".join(best) + f"\n\n(BFS สำรวจ {explored} คำ)")

        st.button("🔄 โจทย์ใหม่", on_click=new_game)

# ----- แท็บตารางคะแนน -----
with tab_board:
    if "flash" in st.session_state:
        st.success(st.session_state.pop("flash"))

    st.subheader("10 อันดับแรก")
    top = rows(board.top(10))
    if top:
        st.table(top)
    else:
        st.info("ยังไม่มีคะแนน ลองเล่นเกมดูก่อน")

    st.subheader("รายชื่อผู้เล่น (เรียงตามชื่อด้วย Merge Sort)")
    by_name = rows(board.by_name())
    if by_name:
        st.table(by_name)

    with st.form("delete_form"):
        del_name = st.text_input("ลบคะแนนของผู้เล่น (พิมพ์ชื่อ)")
        if st.form_submit_button("ลบ"):
            n = board.remove_name(del_name.strip())
            st.session_state.flash = f"ลบแล้ว {n} รายการ"
            st.rerun()

# ----- แท็บเบื้องหลังโปรแกรม -----
with tab_info:
    st.subheader("โครงสร้างข้อมูลและอัลกอริทึมที่ใช้")
    st.markdown("""
| เรื่องที่เรียน | ใช้ตรงไหน |
|---|---|
| Graph | แต่ละคำคือโหนด คำที่ต่างกัน 1 ตัวอักษรคือเส้นเชื่อม |
| BFS + Queue | ปุ่มคำใบ้ และการหาทางสั้นสุด |
| DFS + Stack | ปุ่มเทียบ BFS/DFS |
| AVL Tree | พจนานุกรมและตารางคะแนน |
| Merge Sort | รายชื่อผู้เล่นเรียงตามชื่อ |
| In-order traversal | อันดับคะแนนจากสูงไปต่ำ |
""")
    st.subheader("ผลเปรียบเทียบเวลาค้นหา")
    if os.path.exists("benchmark.png"):
        st.image("benchmark.png")
    else:
        st.info("ยังไม่มีกราฟ รัน python benchmark.py ก่อนเพื่อสร้าง benchmark.png")