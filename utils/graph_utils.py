"""
Graph Utils - Công cụ xử lý đồ thị
"""

import hashlib
import logging
import networkx as nx
from typing import Dict, List, Tuple, Set, Any, Optional

logger = logging.getLogger("GraphUtils")

def create_node_id(name: str, type_name: str = "entity") -> str:
    """
    Tạo ID duy nhất cho node dựa trên tên và loại
    
    Args:
        name: Tên của node
        type_name: Loại node (mặc định: entity)
    
    Returns:
        str: ID duy nhất cho node
    """
    if not name:
        return f"{type_name}_unknown"
    
    # Làm sạch tên
    name_clean = name.lower().strip()
    
    # Tạo chuỗi để hash
    text_to_hash = f"{type_name.lower()}:{name_clean}"
    
    # Tạo hash md5
    hash_obj = hashlib.md5(text_to_hash.encode('utf-8'))
    node_id = f"{type_name}_{hash_obj.hexdigest()[:10]}"
    
    return node_id

def get_subgraph(graph: nx.DiGraph, node_ids: List[str], max_depth: int = 1) -> nx.DiGraph:
    """
    Lấy đồ thị con bắt đầu từ các node cho trước
    
    Args:
        graph: Đồ thị gốc
        node_ids: Danh sách ID của các node gốc
        max_depth: Độ sâu tối đa tìm kiếm
    
    Returns:
        nx.DiGraph: Đồ thị con
    """
    if not graph or not node_ids:
        return nx.DiGraph()
    
    # Kiểm tra các node tồn tại trong đồ thị
    valid_nodes = [node_id for node_id in node_ids if node_id in graph.nodes]
    
    if not valid_nodes:
        logger.warning("Không có node nào hợp lệ trong danh sách")
        return nx.DiGraph()
    
    # Lấy tất cả các node trong phạm vi độ sâu cho trước
    nodes_to_include = set(valid_nodes)
    
    def explore_neighbors(node_id: str, depth: int = 0):
        """Tìm tất cả các node láng giềng theo độ sâu"""
        if depth >= max_depth:
            return
        
        # Lấy tất cả các node kết nối trực tiếp
        neighbors = set(graph.successors(node_id)).union(set(graph.predecessors(node_id)))
        
        # Thêm vào danh sách các node cần bao gồm
        new_neighbors = neighbors - nodes_to_include
        nodes_to_include.update(new_neighbors)
        
        # Tiếp tục tìm với độ sâu tiếp theo
        for neighbor in new_neighbors:
            explore_neighbors(neighbor, depth + 1)
    
    # Bắt đầu tìm từ các node gốc
    for node_id in valid_nodes:
        explore_neighbors(node_id)
    
    # Tạo đồ thị con với các node đã tìm được
    subgraph = graph.subgraph(nodes_to_include).copy()
    
    return subgraph

def find_paths(graph: nx.DiGraph, start_node: str, end_node: str, max_length: int = 3) -> List[List[str]]:
    """
    Tìm các đường đi từ node bắt đầu đến node kết thúc
    
    Args:
        graph: Đồ thị
        start_node: ID của node bắt đầu
        end_node: ID của node kết thúc
        max_length: Độ dài tối đa của đường đi
    
    Returns:
        list: Danh sách các đường đi (mỗi đường đi là một list các node ID)
    """
    if not graph or start_node not in graph.nodes or end_node not in graph.nodes:
        return []
    
    # Sử dụng all_simple_paths của NetworkX với giới hạn độ dài
    try:
        paths = list(nx.all_simple_paths(graph, start_node, end_node, cutoff=max_length))
        return paths
    except Exception as e:
        logger.error(f"Lỗi khi tìm đường đi: {e}")
        return []

def calculate_centrality(graph: nx.DiGraph, top_n: int = 10) -> Dict[str, float]:
    """
    Tính toán độ trung tâm của các node trong đồ thị
    
    Args:
        graph: Đồ thị
        top_n: Số lượng node trung tâm nhất cần trả về
    
    Returns:
        dict: Dictionary {node_id: centrality_score}
    """
    if not graph or not graph.nodes:
        return {}
    
    try:
        # Tính độ trung tâm PageRank
        centrality = nx.pagerank(graph)
        
        # Sắp xếp và lấy top N
        sorted_centrality = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
        top_centrality = dict(sorted_centrality[:top_n])
        
        return top_centrality
    except Exception as e:
        logger.error(f"Lỗi khi tính toán độ trung tâm: {e}")
        return {}

def find_communities(graph: nx.DiGraph) -> Dict[str, int]:
    """
    Tìm các cộng đồng trong đồ thị sử dụng thuật toán Louvain
    
    Args:
        graph: Đồ thị
    
    Returns:
        dict: Dictionary {node_id: community_id}
    """
    try:
        # Tạo phiên bản undirected của đồ thị
        undirected_graph = graph.to_undirected()
        
        # Sử dụng thuật toán Louvain
        from community import best_partition
        partition = best_partition(undirected_graph)
        
        return partition
    except ImportError:
        logger.warning("Thư viện python-louvain không có sẵn, sử dụng phân vùng đơn giản")
        
        # Phân vùng đơn giản dựa trên các thành phần liên thông
        communities = {}
        components = nx.connected_components(graph.to_undirected())
        
        for i, component in enumerate(components):
            for node in component:
                communities[node] = i
        
        return communities
    except Exception as e:
        logger.error(f"Lỗi khi tìm cộng đồng: {e}")
        return {}

def analyze_graph(graph: nx.DiGraph) -> Dict[str, Any]:
    """
    Phân tích đồ thị và trả về các chỉ số quan trọng
    
    Args:
        graph: Đồ thị cần phân tích
    
    Returns:
        dict: Các chỉ số phân tích
    """
    if not graph or not graph.nodes:
        return {
            "nodes": 0,
            "edges": 0,
            "density": 0,
            "connected": False
        }
    
    try:
        # Thông tin cơ bản
        node_count = graph.number_of_nodes()
        edge_count = graph.number_of_edges()
        density = nx.density(graph)
        
        # Kiểm tra liên thông
        undirected = graph.to_undirected()
        is_connected = nx.is_connected(undirected)
        
        # Số thành phần liên thông
        components = list(nx.connected_components(undirected))
        component_count = len(components)
        
        # Kích thước của thành phần liên thông lớn nhất
        largest_component_size = len(max(components, key=len)) if components else 0
        
        # Độ lệch của độ vào/ra
        in_degrees = [d for n, d in graph.in_degree()]
        out_degrees = [d for n, d in graph.out_degree()]
        
        avg_in_degree = sum(in_degrees) / node_count if node_count > 0 else 0
        avg_out_degree = sum(out_degrees) / node_count if node_count > 0 else 0
        
        # Đường kính (có thể mất nhiều thời gian với đồ thị lớn)
        diameter = -1
        if node_count < 1000 and is_connected:  # Chỉ tính với đồ thị nhỏ
            try:
                diameter = nx.diameter(undirected)
            except Exception:
                pass
        
        return {
            "nodes": node_count,
            "edges": edge_count,
            "density": density,
            "connected": is_connected,
            "component_count": component_count,
            "largest_component_size": largest_component_size,
            "avg_in_degree": avg_in_degree,
            "avg_out_degree": avg_out_degree,
            "diameter": diameter
        }
    except Exception as e:
        logger.error(f"Lỗi khi phân tích đồ thị: {e}")
        return {
            "nodes": graph.number_of_nodes(),
            "edges": graph.number_of_edges(),
            "error": str(e)
        }

def merge_graphs(graph1: nx.DiGraph, graph2: nx.DiGraph) -> nx.DiGraph:
    """
    Kết hợp hai đồ thị thành một
    
    Args:
        graph1: Đồ thị thứ nhất
        graph2: Đồ thị thứ hai
    
    Returns:
        nx.DiGraph: Đồ thị kết hợp
    """
    if not graph1 and not graph2:
        return nx.DiGraph()
    
    if not graph1:
        return graph2.copy()
    
    if not graph2:
        return graph1.copy()
    
    # Tạo đồ thị mới
    merged_graph = graph1.copy()
    
    # Thêm các node từ graph2
    for node, attrs in graph2.nodes(data=True):
        if node not in merged_graph:
            merged_graph.add_node(node, **attrs)
        else:
            # Cập nhật thuộc tính của node đã tồn tại
            for key, value in attrs.items():
                if key not in merged_graph.nodes[node]:
                    merged_graph.nodes[node][key] = value
    
    # Thêm các edge từ graph2
    for u, v, attrs in graph2.edges(data=True):
        if not merged_graph.has_edge(u, v):
            merged_graph.add_edge(u, v, **attrs)
        else:
            # Cập nhật thuộc tính của edge đã tồn tại
            for key, value in attrs.items():
                if key not in merged_graph[u][v]:
                    merged_graph[u][v][key] = value
    
    return merged_graph