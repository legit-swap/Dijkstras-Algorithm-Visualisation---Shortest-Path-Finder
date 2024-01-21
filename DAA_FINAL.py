import sys
import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk

def find_min_vertex(distance, visited, n):
    min_vertex = -1
    for i in range(n):
        if not visited[i] and (min_vertex == -1 or distance[i] < distance[min_vertex]):
            min_vertex = i
    return min_vertex

def print_path(parent, vertex):
    if parent[vertex] == -1:
        return [vertex]
    path = print_path(parent, parent[vertex])
    path.append(vertex)
    return path

def dijkstra(edges, n):
    distance = [sys.maxsize] * n
    visited = [False] * n
    parent = [-1] * n
    distance[0] = 0

    G = nx.Graph()

    for i in range(n):
        G.add_node(i)

    for i in range(n - 1):
        min_vertex = find_min_vertex(distance, visited, n)
        visited[min_vertex] = True
        for j in range(n):
            if edges[min_vertex][j] != 0 and not visited[j]:
                dist = distance[min_vertex] + edges[min_vertex][j]
                if dist < distance[j]:
                    distance[j] = dist
                    parent[j] = min_vertex
                    G.add_edge(min_vertex, j, weight=edges[min_vertex][j])

    for i in range(n):
        print(f"{i} , {distance[i]} KM, Path:", end=" ")
        path = print_path(parent, i)
        print(" -> ".join(map(str, path)))

    return G, parent, distance

def highlight_path(G, parent, start, end):
    path_edges = [(parent[end], end)]
    while parent[end] != start:
        end = parent[end]
        path_edges.append((parent[end], end))
    
    edge_colors = ['b' if edge not in path_edges else 'r' for edge in G.edges()]
    return edge_colors

def visualize_dijkstra():
    n = int(vertices_entry.get())
    e = int(edges_entry.get())
    edge_weights = edge_weights_text.get("1.0", "end-1c").split("\n")
    
    edges = [[0] * n for _ in range(n) ]  # Initialize an n x n matrix with all values set to 0.
    
    for edge_weight in edge_weights:
        if edge_weight:
            f, s, weight = map(int, edge_weight.split())
            edges[f][s] = weight  # Update the matrix at the specified indices.
            edges[s][f] = weight  # Since it's an undirected graph, update both directions.
    
    G_initial = nx.Graph()
    for i in range(n):
        G_initial.add_node(i)
        for j in range(n):
            if edges[i][j] != 0:
                G_initial.add_edge(i, j, weight=edges[i][j])

    G_final, parent, distances = dijkstra(edges, n)
    edge_colors = highlight_path(G_final, parent, start=0, end=n-1)

    pos_initial = nx.spring_layout(G_initial)
    edge_labels_initial = nx.get_edge_attributes(G_initial, 'weight')
    labels_initial = {i: f'{i}' for i in range(n)}

    pos_final = pos_initial
    edge_labels_final = nx.get_edge_attributes(G_final, 'weight')
    
    # Create labels with node number and distance below the nodes
    labels_final = {i: f'\n\n({distances[i]} KM)' for i in range(n)}

    plt.figure(figsize=(12, 5))
    plt.subplot(121)
    nx.draw(G_initial, pos=pos_initial, with_labels=True, node_size=500, node_color='lightblue', font_size=10, font_weight='bold', font_color='black', edge_color='gray', width=1)
    nx.draw_networkx_edge_labels(G_initial, pos_initial, edge_labels=edge_labels_initial)
    nx.draw_networkx_labels(G_initial, pos_initial, labels_initial, font_size=10, font_weight='bold', font_color='black')
    plt.title("Initial State")

    plt.subplot(122)
    nx.draw(G_final, pos=pos_final, with_labels=True, node_size=500, node_color='lightblue', font_size=10, font_weight='bold', font_color='black', edge_color=edge_colors, width=2)
    nx.draw_networkx_edge_labels(G_final, pos_final, edge_labels=edge_labels_final)
    nx.draw_networkx_labels(G_final, pos_final, labels_final, font_size=10, font_weight='bold', font_color='black')
    plt.title("Final State")

    plt.tight_layout()
    plt.show()

app = tk.Tk()
app.title("Dijkstra's Algorithm Visualization")

# Create and layout GUI components
frame = ttk.Frame(app)
frame.grid(row=0, column=0)

vertices_label = ttk.Label(frame, text="Total Vertices:")
vertices_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
vertices_entry = ttk.Entry(frame)
vertices_entry.grid(row=0, column=1, padx=5, pady=5)

edges_label = ttk.Label(frame, text="Total Edges:")
edges_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
edges_entry = ttk.Entry(frame)
edges_entry.grid(row=1, column=1, padx=5, pady=5)

edge_weights_label = ttk.Label(frame, text="Edge Weights (Vertex1 Vertex2 Weight):")
edge_weights_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')
edge_weights_text = tk.Text(frame, height=10, width=30)
edge_weights_text.grid(row=2, column=1, padx=5, pady=5)

instructions_label = ttk.Label(frame, text="Enter edge weights in the format: 'Vertex1 Vertex2 Weight' (one per line)")
instructions_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

visualize_button = ttk.Button(frame, text="Visualize Dijkstra", command=visualize_dijkstra)
visualize_button.grid(row=4, column=0, columnspan=2, padx=5, pady=10)

app.mainloop()
