def build_graph(words):
    """สร้างกราฟแบบ Adjacency List: {คำ: [คำเพื่อนบ้าน, ...]}"""
    words = set(words)
    buckets = {}
    for w in words:
        for i in range(len(w)):
            pattern = w[:i] + "_" + w[i + 1:]
            buckets.setdefault(pattern, []).append(w)

    graph = {w: [] for w in words}
    for group in buckets.values():
        for a in group:
            for b in group:
                if a != b:
                    graph[a].append(b)
    return graph