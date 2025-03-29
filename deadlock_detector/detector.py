import networkx as nx
import psutil

def get_process_info():
    """Fetch system process information."""
    process_list = {}
    for proc in psutil.process_iter(attrs=['pid', 'name', 'status']):
        process_list[proc.info['pid']] = proc.info['name']
    return process_list

def detect_deadlock():
    """Builds a Resource Allocation Graph (RAG) and detects deadlocks."""
    G = nx.DiGraph()

    # Simulated process-resource dependencies
    edges = [(1, 'R1'), ('R1', 2), (2, 'R2'), ('R2', 3), (3, 'R3'), ('R3', 1)]
    
    G.add_edges_from(edges)
    
    try:
        cycle = nx.find_cycle(G, orientation="original")
        return f"Deadlock detected: {cycle}"
    except nx.NetworkXNoCycle:
        return "No deadlock detected."

if __name__ == "__main__":
    print(detect_deadlock())
