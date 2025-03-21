"""
Knowledge Base - Lưu trữ và quản lý kiến thức dưới dạng đồ thị
"""

import os
import json
import logging
import networkx as nx
from datetime import datetime

import config
from utils.nlp_utils import extract_keywords

class KnowledgeBase:
    """
    Cơ sở dữ liệu kiến thức dạng đồ thị
    """
    
    def __init__(self):
        """Khởi tạo knowledge base"""
        self.logger = logging.getLogger("KnowledgeBase")
        
        # Tạo thư mục lưu trữ nếu chưa tồn tại
        os.makedirs(config.KNOWLEDGE_GRAPH_DIR, exist_ok=True)
        
        # Khởi tạo đồ thị kiến thức
        self.graph = self._load_or_create_graph()
        
        self.logger.info(f"Knowledge Base đã khởi tạo với {len(self.graph.nodes)} nodes và {len(self.graph.edges)} edges")
    
    def _load_or_create_graph(self):
        """
        Tải đồ thị kiến thức hiện có hoặc tạo mới nếu chưa có
        
        Returns:
            networkx.DiGraph: Đồ thị kiến thức
        """
        graph_path = os.path.join(config.KNOWLEDGE_GRAPH_DIR, "knowledge_graph.json")
        
        if os.path.exists(graph_path):
            try:
                # Tải đồ thị từ file
                with open(graph_path, 'r', encoding='utf-8') as f:
                    graph_data = json.load(f)
                graph = nx.node_link_graph(graph_data)
                self.logger.info(f"Đã tải đồ thị kiến thức với {len(graph.nodes)} nodes và {len(graph.edges)} edges")
                return graph
            except Exception as e:
                self.logger.error(f"Lỗi khi tải đồ thị kiến thức: {e}")
        
        # Tạo đồ thị mới nếu không tải được
        self.logger.info("Tạo đồ thị kiến thức mới")
        return nx.DiGraph()
    
    def save(self):
        """Lưu đồ thị kiến thức xuống file"""
        graph_path = os.path.join(config.KNOWLEDGE_GRAPH_DIR, "knowledge_graph.json")
        backup_path = os.path.join(config.KNOWLEDGE_GRAPH_DIR, 
                                  f"knowledge_graph_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        # Tạo backup nếu file đã tồn tại
        if os.path.exists(graph_path):
            try:
                os.rename(graph_path, backup_path)
                self.logger.debug(f"Đã tạo backup tại {backup_path}")
            except Exception as e:
                self.logger.error(f"Không thể tạo backup: {e}")
        
        # Lưu đồ thị xuống file
        try:
            graph_data = nx.node_link_data(self.graph)
            with open(graph_path, 'w', encoding='utf-8') as f:
                json.dump(graph_data, f, ensure_ascii=False, indent=2)
            self.logger.info(f"Đã lưu đồ thị kiến thức với {len(self.graph.nodes)} nodes và {len(self.graph.edges)} edges")
        except Exception as e:
            self.logger.error(f"Lỗi khi lưu đồ thị kiến thức: {e}")
    
    def add_node(self, node_id, attributes=None):
        """
        Thêm node vào đồ thị
        
        Args:
            node_id (str): ID của node
            attributes (dict, optional): Thuộc tính của node
            
        Returns:
            str: ID của node đã thêm
        """
        if attributes is None:
            attributes = {}
            
        # Thêm thông tin thời gian nếu là node mới
        is_new = node_id not in self.graph.nodes
        if is_new:
            attributes.update({
                "created_at": datetime.now().isoformat(),
            })
        
        # Luôn cập nhật thời gian sửa đổi
        attributes.update({
            "updated_at": datetime.now().isoformat()
        })
        
        # Thêm hoặc cập nhật node
        self.graph.add_node(node_id, **attributes)
        
        # Log tùy theo node mới hay cập nhật
        if is_new:
            self.logger.debug(f"Đã thêm node mới: {node_id}")
        else:
            self.logger.debug(f"Đã cập nhật node: {node_id}")
            
        return node_id
    
    def add_edge(self, source, target, relation_type, attributes=None):
        """
        Thêm edge (mối quan hệ) vào đồ thị
        
        Args:
            source (str): ID của node nguồn
            target (str): ID của node đích
            relation_type (str): Loại quan hệ
            attributes (dict, optional): Thuộc tính của edge
        """
        if attributes is None:
            attributes = {}
            
        # Đảm bảo cả source và target đều tồn tại
        if source not in self.graph.nodes:
            self.logger.warning(f"Node nguồn không tồn tại: {source}")
            return False
            
        if target not in self.graph.nodes:
            self.logger.warning(f"Node đích không tồn tại: {target}")
            return False
            
        # Thêm thông tin thời gian và loại quan hệ
        attributes.update({
            "relation_type": relation_type,
            "created_at": datetime.now().isoformat()
        })
        
        # Kiểm tra xem edge đã tồn tại chưa
        if self.graph.has_edge(source, target):
            # Cập nhật thuộc tính của edge
            for key, value in attributes.items():
                self.graph[source][target][key] = value
            self.logger.debug(f"Đã cập nhật edge: {source} -> {target} ({relation_type})")
        else:
            # Thêm edge mới
            self.graph.add_edge(source, target, **attributes)
            self.logger.debug(f"Đã thêm edge mới: {source} -> {target} ({relation_type})")
        
        return True
    
    def query(self, query_text):
        """
        Truy vấn đồ thị kiến thức với câu hỏi của người dùng
        Trả về các node và edge liên quan đến câu hỏi
        
        Args:
            query_text (str): Câu hỏi cần truy vấn
            
        Returns:
            list: Danh sách các node liên quan và độ liên quan
        """
        self.logger.info(f"Truy vấn KB với: {query_text}")
        
        # Trích xuất từ khóa từ câu hỏi
        keywords = extract_keywords(query_text)
        self.logger.debug(f"Từ khóa: {keywords}")
        
        # Nếu không có từ khóa, trả về rỗng
        if not keywords:
            self.logger.warning("Không tìm thấy từ khóa trong câu hỏi")
            return []
        
        relevant_nodes = []
        
        # Duyệt qua tất cả node trong đồ thị
        for node, attrs in self.graph.nodes(data=True):
            # Chuyển node_id thành chuỗi để tìm kiếm
            node_str = str(node).lower()
            
            # Kiểm tra nếu có từ khóa trong node_id
            if any(keyword in node_str for keyword in keywords):
                relevant_nodes.append((node, attrs, 1.0))  # Độ liên quan 100%
                continue
                
            # Kiểm tra trong các thuộc tính
            node_text = " ".join(str(v) for v in attrs.values() if isinstance(v, (str, int, float)))
            node_text = node_text.lower()
            
            # Tính độ liên quan dựa trên số từ khóa xuất hiện
            matches = sum(1 for keyword in keywords if keyword in node_text)
            if matches > 0:
                relevance = matches / len(keywords)
                if relevance > 0.3:  # Ngưỡng tối thiểu 30% liên quan
                    relevant_nodes.append((node, attrs, relevance))
        
        # Sắp xếp theo độ liên quan
        relevant_nodes.sort(key=lambda x: x[2], reverse=True)
        
        self.logger.info(f"Tìm thấy {len(relevant_nodes)} nodes liên quan")
        return relevant_nodes
    
    def get_node(self, node_id):
        """
        Lấy thông tin của một node
        
        Args:
            node_id (str): ID của node cần lấy
            
        Returns:
            tuple: (node_id, attributes) nếu tồn tại, None nếu không
        """
        if node_id in self.graph.nodes:
            return node_id, self.graph.nodes[node_id]
        return None
        
    def get_related_nodes(self, node_id, relation_type=None, max_depth=1):
        """
        Lấy các node liên quan đến node hiện tại
        
        Args:
            node_id (str): ID của node gốc
            relation_type (str, optional): Loại quan hệ cần lọc
            max_depth (int, optional): Độ sâu tối đa tìm kiếm
            
        Returns:
            list: Danh sách các node liên quan
        """
        if node_id not in self.graph.nodes:
            self.logger.warning(f"Node không tồn tại: {node_id}")
            return []
            
        related = []
        visited = set()
        
        def explore(current_id, depth=0):
            if depth >= max_depth or current_id in visited:
                return
                
            visited.add(current_id)
            
            # Tìm các node kết nối trực tiếp
            for src, dst, data in self.graph.out_edges(current_id, data=True):
                if relation_type is None or data.get("relation_type") == relation_type:
                    if dst not in visited:
                        related.append((dst, self.graph.nodes[dst], data))
                        
                        # Tiếp tục tìm ở độ sâu tiếp theo
                        if depth + 1 < max_depth:
                            explore(dst, depth + 1)
        
        # Bắt đầu tìm từ node gốc
        explore(node_id)
                
        return related
    
    def remove_node(self, node_id):
        """
        Xóa một node khỏi đồ thị
        
        Args:
            node_id (str): ID của node cần xóa
            
        Returns:
            bool: True nếu xóa thành công, False nếu không
        """
        if node_id in self.graph.nodes:
            self.graph.remove_node(node_id)
            self.logger.info(f"Đã xóa node: {node_id}")
            return True
        else:
            self.logger.warning(f"Không thể xóa node không tồn tại: {node_id}")
            return False
    
    def remove_edge(self, source, target):
        """
        Xóa một edge khỏi đồ thị
        
        Args:
            source (str): ID của node nguồn
            target (str): ID của node đích
            
        Returns:
            bool: True nếu xóa thành công, False nếu không
        """
        if self.graph.has_edge(source, target):
            self.graph.remove_edge(source, target)
            self.logger.info(f"Đã xóa edge: {source} -> {target}")
            return True
        else:
            self.logger.warning(f"Không thể xóa edge không tồn tại: {source} -> {target}")
            return False