"""
AGI Engine - Thành phần chính điều phối hoạt động của hệ thống, tập trung vào toán lớp 1
"""

import logging
import time
import re
from typing import Dict, Any, List, Tuple

from core.knowledge_base import KnowledgeBase
from core.learner import Learner
from core.reasoner import Reasoner
from collectors.collector import InformationCollector
import config

class AGIEngine:
    """AGI Engine là thành phần điều phối chính của hệ thống, tập trung vào toán lớp 1"""
    
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
        1. Kiểm tra xem có phải yêu cầu toán học không
        2. Nếu là toán học, sử dụng process_math_request
        3. Nếu không, xử lý như câu hỏi thông thường
        
        Args:
            request (str): Câu hỏi hoặc yêu cầu của người dùng
            
        Returns:
            dict: Kết quả trả về gồm answer và metadata
        """
        start_time = time.time()
        self.logger.info(f"Xử lý yêu cầu: {request}")
        
        # Xác định xem yêu cầu có phải là bài toán không
        if self._is_math_problem(request):
            return self.process_math_request(request)
        
        try:
            # 1. Kiểm tra knowledge base
            kb_results = self.kb.query(request)
            self.logger.debug(f"Tìm được {len(kb_results)} kết quả từ KB")
            
            # 2. Nếu không đủ thông tin, thu thập thêm
            if not self._has_sufficient_info(kb_results, request):
                self.logger.info("Không đủ thông tin, bắt đầu thu thập")
                new_info = self.collector.collect(request)
                
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
    
    def process_math_request(self, request):
        """
        Xử lý yêu cầu toán học
        
        Args:
            request (str): Câu hỏi toán học
            
        Returns:
            dict: Kết quả trả về gồm answer và metadata
        """
        start_time = time.time()
        self.logger.info(f"Xử lý bài toán: {request}")
        
        try:
            # Kiểm tra knowledge base cho kiến thức toán học sẵn có
            kb_results = self.kb.query(request)
            
            # Sử dụng reasoner chuyên biệt cho toán học
            response = self.reasoner.solve_math_problem(request, kb_results)
            
            # Thêm thông tin thời gian xử lý
            process_time = time.time() - start_time
            response["process_time"] = process_time
            
            # Thêm hình ảnh minh họa
            if "numbers" in response and len(response.get("numbers", [])) > 0:
                response["visualization"] = self._generate_math_visualization(
                    response.get("operation", ""),
                    response.get("numbers", []),
                    response.get("result", 0)
                )
            
            self.logger.info(f"Đã xử lý bài toán trong {process_time:.2f} giây")
            
            return response
            
        except Exception as e:
            self.logger.error(f"Lỗi khi xử lý bài toán: {str(e)}", exc_info=True)
            return {
                "answer": f"Xảy ra lỗi khi xử lý: {str(e)}",
                "error": str(e),
                "success": False
            }
    
    def _is_math_problem(self, request: str) -> bool:
        """
        Kiểm tra xem yêu cầu có phải là bài toán lớp 1 không
        
        Args:
            request: Yêu cầu cần kiểm tra
            
        Returns:
            bool: True nếu là bài toán lớp 1
        """
        # Tách các ký tự và tìm kiếm các phép toán 
        request_lower = request.lower()
        
        # Kiểm tra có dấu + hoặc -
        has_math_symbol = "+" in request or "-" in request
        
        # Kiểm tra có các từ khóa liên quan đến toán
        math_keywords = ["cộng", "trừ", "tổng", "hiệu", "bằng", "kết quả", 
                       "tính", "bài toán", "số", "phép tính"]
        has_math_keyword = any(keyword in request_lower for keyword in math_keywords)
        
        # Kiểm tra có ít nhất 2 số trong câu hỏi
        numbers = re.findall(r'\d+', request)
        has_numbers = len(numbers) >= 2
        
        # Xác định là bài toán nếu có ít nhất 2 trong 3 điều kiện
        conditions_met = sum([has_math_symbol, has_math_keyword, has_numbers])
        return conditions_met >= 2
    
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
    
    def _generate_math_visualization(self, operation, numbers, result):
        """
        Tạo mô tả trực quan cho phép tính
        
        Args:
            operation: Loại phép tính (addition, subtraction)
            numbers: Các số trong phép tính
            result: Kết quả phép tính
            
        Returns:
            str: Mô tả trực quan dạng HTML
        """
        if not numbers or len(numbers) < 2:
            return ""
            
        if operation == "addition":
            # Tạo minh họa cho phép cộng
            return f"""
            <div class="visualization addition">
                <div class="objects-container">
                    <div class="first-number">
                        {'●' * numbers[0]}
                    </div>
                    <div class="plus">+</div>
                    <div class="second-number">
                        {'●' * numbers[1]}
                    </div>
                    <div class="equals">=</div>
                    <div class="result">
                        {'●' * result}
                    </div>
                </div>
                <div class="number-line">
                    <div class="line"></div>
                    <div class="markers">
                        {'<div class="marker"></div>' * (result + 5)}
                    </div>
                    <div class="operation">
                        <div class="hop" style="left: 0px;">|</div>
                        <div class="hop" style="left: {numbers[0]*20}px;">+{numbers[1]}</div>
                    </div>
                </div>
            </div>
            """
        elif operation == "subtraction":
            # Tạo minh họa cho phép trừ
            return f"""
            <div class="visualization subtraction">
                <div class="objects-container">
                    <div class="first-number">
                        {'●' * numbers[0]}
                    </div>
                    <div class="minus">-</div>
                    <div class="second-number crossed">
                        {'<span class="crossed-item">●</span>' * numbers[1]}
                    </div>
                    <div class="equals">=</div>
                    <div class="result">
                        {'●' * result}
                    </div>
                </div>
                <div class="number-line">
                    <div class="line"></div>
                    <div class="markers">
                        {'<div class="marker"></div>' * (numbers[0] + 5)}
                    </div>
                    <div class="operation">
                        <div class="hop" style="left: {numbers[0]*20}px;">|</div>
                        <div class="hop" style="left: {result*20}px;">-{numbers[1]}</div>
                    </div>
                </div>
            </div>
            """
        else:
            return ""