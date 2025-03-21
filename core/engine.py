"""
AGI Engine - Thành phần chính điều phối hoạt động của hệ thống
"""

import logging
import time
from core.knowledge_base import KnowledgeBase
from core.learner import Learner
from core.reasoner import Reasoner
from collectors.collector import InformationCollector
import config

class AGIEngine:
    """AGI Engine là thành phần điều phối chính của hệ thống"""
    
    def __init__(self):
        """Khởi tạo AGI Engine với các thành phần con"""
        self.logger = logging.getLogger("AGIEngine")
        
        # Khởi tạo Knowledge Base
        self.kb = KnowledgeBase()
        
        # Khởi tạo Learner
        self.learner = Learner(self.kb)
        
        # Khởi tạo Reasoner
        self.reasoner = Reasoner(self.kb)
        
        # Khởi tạo Information Collector
        self.collector = InformationCollector()
        
        self.logger.info("AGI Engine đã được khởi tạo")
    
    def process_request(self, request):
        """
        Xử lý yêu cầu từ người dùng
        
        Luồng xử lý:
        1. Kiểm tra KB để tìm thông tin liên quan
        2. Nếu không có đủ thông tin, thu thập thêm dữ liệu
        3. Tích hợp thông tin mới vào KB
        4. Suy luận để tạo câu trả lời
        
        Args:
            request (str): Câu hỏi hoặc yêu cầu của người dùng
            
        Returns:
            dict: Kết quả trả về gồm answer và metadata
        """
        start_time = time.time()
        self.logger.info(f"Xử lý yêu cầu: {request}")
        
        try:
            # 1. Kiểm tra knowledge base
            kb_results = self.kb.query(request)
            self.logger.debug(f"Tìm được {len(kb_results)} kết quả từ KB")
            
            # 2. Nếu không đủ thông tin, thu thập thêm
            if not self._has_sufficient_info(kb_results, request):
                self.logger.info("Không đủ thông tin, bắt đầu thu thập")
                new_info = self.collector.collect(request, kb_results)
                
                # 3. Tích hợp thông tin mới vào KB
                if new_info:
                    self.logger.info(f"Học {len(new_info) if isinstance(new_info, list) else 1} thông tin mới")
                    self.learner.learn(new_info, request)
                    # Truy vấn lại KB sau khi học
                    kb_results = self.kb.query(request)
                    self.logger.debug(f"Sau khi học, tìm được {len(kb_results)} kết quả từ KB")
            
            # 4. Suy luận để tạo câu trả lời
            response = self.reasoner.reason(request, kb_results)
            
            # Thêm thông tin thời gian xử lý
            process_time = time.time() - start_time
            response["process_time"] = process_time
            self.logger.info(f"Đã xử lý yêu cầu trong {process_time:.2f} giây")
            
            return response
            
        except Exception as e:
            self.logger.error(f"Lỗi khi xử lý yêu cầu: {str(e)}", exc_info=True)
            return {
                "answer": f"Xảy ra lỗi khi xử lý: {str(e)}",
                "error": str(e),
                "success": False
            }
    
    def _has_sufficient_info(self, kb_results, request):
        """
        Kiểm tra xem thông tin hiện tại có đủ để trả lời không
        
        Args:
            kb_results (list): Kết quả từ KB
            request (str): Yêu cầu của người dùng
            
        Returns:
            bool: True nếu có đủ thông tin, False nếu cần thu thập thêm
        """
        # Nếu không có kết quả, chắc chắn không đủ thông tin
        if not kb_results:
            return False
            
        # Đánh giá mức độ liên quan của kết quả
        relevance = self.reasoner.evaluate_relevance(kb_results, request)
        self.logger.debug(f"Độ liên quan của kết quả: {relevance:.2f}")
        
        # So sánh với ngưỡng cấu hình
        return relevance >= config.MIN_CONFIDENCE
    
    def get_kb_stats(self):
        """
        Lấy thống kê về Knowledge Base
        
        Returns:
            dict: Thông tin thống kê
        """
        return {
            "nodes": len(self.kb.graph.nodes),
            "edges": len(self.kb.graph.edges),
            "types": self._count_node_types()
        }
    
    def _count_node_types(self):
        """Đếm số lượng node theo từng loại"""
        type_count = {}
        for _, attrs in self.kb.graph.nodes(data=True):
            node_type = attrs.get("type", "unknown")
            if node_type in type_count:
                type_count[node_type] += 1
            else:
                type_count[node_type] = 1
        return type_count