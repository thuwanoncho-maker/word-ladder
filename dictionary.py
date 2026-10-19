class ArrayDictionary:
    """พจนานุกรมแบบ Array (list): ค้นทีละตัว O(n)"""

    def __init__(self):
        self.items = []

    def insert(self, key):
        self.items.append(key)

    def search(self, key):
        for x in self.items:
            if x == key:
                return True
        return False


class _Node:
    def __init__(self, key):
        self.key = key
        self.next = None


class LinkedListDictionary:
    """พจนานุกรมแบบ Linked List: ค้นทีละโหนด O(n)"""

    def __init__(self):
        self.head = None
        self.tail = None

    def insert(self, key):
        node = _Node(key)
        if self.tail is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node

    def search(self, key):
        node = self.head
        while node:
            if node.key == key:
                return True
            node = node.next
        return False