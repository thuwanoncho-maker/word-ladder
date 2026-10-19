import sys


class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


def height(node):
    return node.height if node else 0


def update(node):
    node.height = 1 + max(height(node.left), height(node.right))


def balance_factor(node):
    return height(node.left) - height(node.right) if node else 0


def rotate_right(y):
    x = y.left
    y.left = x.right
    x.right = y
    update(y)
    update(x)
    return x


def rotate_left(x):
    y = x.right
    x.right = y.left
    y.left = x
    update(x)
    update(y)
    return y


def finish(node, balanced):
    """อัปเดตความสูง และถ้าเป็น AVL ให้หมุนต้นไม้เมื่อเอียงเกินไป"""
    update(node)
    if not balanced:
        return node
    bf = balance_factor(node)
    if bf > 1:                                   # เอียงซ้าย
        if balance_factor(node.left) < 0:        # กรณี Left-Right
            node.left = rotate_left(node.left)
        return rotate_right(node)
    if bf < -1:                                  # เอียงขวา
        if balance_factor(node.right) > 0:       # กรณี Right-Left
            node.right = rotate_right(node.right)
        return rotate_left(node)
    return node


def insert(node, key, balanced):
    if node is None:
        return Node(key)
    if key < node.key:
        node.left = insert(node.left, key, balanced)
    elif key > node.key:
        node.right = insert(node.right, key, balanced)
    else:
        return node                              # มีคำนี้แล้ว ไม่เพิ่มซ้ำ
    return finish(node, balanced)


def min_node(node):
    while node.left:
        node = node.left
    return node


def delete(node, key, balanced):
    if node is None:
        return None
    if key < node.key:
        node.left = delete(node.left, key, balanced)
    elif key > node.key:
        node.right = delete(node.right, key, balanced)
    else:
        if node.left is None:                    # ไม่มีลูก หรือมีลูกขวาอย่างเดียว
            return node.right
        if node.right is None:                   # มีลูกซ้ายอย่างเดียว
            return node.left
        successor = min_node(node.right)         # มีลูกสองข้าง: ใช้ค่าถัดไปแทนที่
        node.key = successor.key
        node.right = delete(node.right, successor.key, balanced)
    return finish(node, balanced)


def inorder(node, out):
    if node:
        inorder(node.left, out)
        out.append(node.key)
        inorder(node.right, out)


class SearchTree:
    """balanced=True คือ AVL, balanced=False คือ BST ธรรมดา"""

    def __init__(self, balanced=True):
        self.root = None
        self.balanced = balanced
        self.size = 0

    def insert(self, key):
        if not self.search(key):
            self.size += 1
        self.root = insert(self.root, key, self.balanced)

    def delete(self, key):
        if self.search(key):
            self.size -= 1
        self.root = delete(self.root, key, self.balanced)

    def search(self, key):
        node = self.root
        while node:
            if key == node.key:
                return True
            node = node.left if key < node.key else node.right
        return False

    def height(self):
        return height(self.root)

    def to_list(self):
        out = []
        inorder(self.root, out)
        return out


if __name__ == "__main__":
    # ทดสอบ: ใส่คำเรียงตามตัวอักษร (กรณีแย่สุดของ BST)
    sys.setrecursionlimit(20000)
    with open("words.txt") as f:
        words = sorted(line.strip() for line in f if line.strip())

    bst = SearchTree(balanced=False)
    avl = SearchTree(balanced=True)
    for w in words:
        bst.insert(w)
        avl.insert(w)

    print(f"จำนวนคำ: {len(words)}")
    print(f"ความสูง BST: {bst.height()}")
    print(f"ความสูง AVL: {avl.height()}")
    print("in-order เรียงถูกต้อง:", avl.to_list() == words)

    avl.delete(words[0])
    print("หลังลบคำแรก:", avl.size, "คำ, ค้นเจอไหม:", avl.search(words[0]))