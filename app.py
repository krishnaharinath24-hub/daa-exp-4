from flask import Flask, request, render_template_string
import heapq

app = Flask(__name__)

# --- Dijkstra Implementation ---
def dijkstra(graph, source):
    n = len(graph)
    dist = [float('inf')] * n
    prev = [None] * n
    dist[source] = 0
    pq = [(0, source)]
    visited = set()

    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))
    return dist, prev

def reconstruct_path(prev, source, target):
    path = []
    node = target
    while node is not None:
        path.append(node)
        node = prev[node]
    path.reverse()
    if path and path[0] == source:
        return path
    return []

# --- HTML Template ---
TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>Dijkstra Shortest Path</title>
</head>
<body>
    <h2>Dijkstra's Algorithm (Shortest Paths)</h2>
    <form method="post">
        <label>Number of vertices:</label>
        <input type="number" name="vertices" required><br><br>
        
        <label>Edges (format: u v w, one per line):</label><br>
        <textarea name="edges" rows="6" cols="40" required></textarea><br><br>
        
        <label>Source vertex:</label>
        <input type="number" name="source" required><br><br>
        
        <button type="submit">Run Dijkstra</button>
    </form>
    {% if result %}
        <h3>Results (from source {{src}}):</h3>
        <table border="1" cellpadding="5">
            <tr><th>Vertex</th><th>Distance</th><th>Path</th></tr>
            {% for v, d, path in result %}
                <tr>
                    <td>{{v}}</td>
                    <td>{{d}}</td>
                    <td>{{path}}</td>
                </tr>
            {% endfor %}
        </table>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST", "HEAD"])
def index():
    result = None
    src = None

    if request.method == "POST":
        try:
            n = int(request.form["vertices"])
            edges_input = request.form["edges"].strip().splitlines()
            src = int(request.form["source"])

            # Build graph
            graph = {i: [] for i in range(n)}
            for line in edges_input:
                u, v, w = map(int, line.split())
                graph[u].append((v, w))

            dist, prev = dijkstra(graph, src)

            result = []
            for v in range(n):
                path = reconstruct_path(prev, src, v)
                path_str = " -> ".join(map(str, path)) if path else "No path"
                d = dist[v] if dist[v] != float("inf") else "INF"
                result.append((v, d, path_str))
        except Exception as e:
            result = [("Error", "Invalid input", str(e))]

    return render_template_string(TEMPLATE, result=result, src=src)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
