"""
Reasoner - Module suy luận, tạo câu trả lời từ kiến thức, chuyên biệt cho toán lớp 1
"""

import logging
import time
import random
import re
from typing import List, Dict, Tuple, Any

import config
from utils.nlp_utils import extract_keywords, text_similarity

class Reasoner:
    """
    Module suy luận dựa trên cơ sở kiến thức để trả lời câu hỏi, tập trung vào toán lớp 1
    """
    
    def __init__(self, knowledge_base):
        """
        Khởi tạo reasoner module
        
        Args:
            knowledge_base (KnowledgeBase): Cơ sở kiến thức để suy luận
        """
        self.kb = knowledge_base
        self.logger = logging.getLogger("Reasoner")
    
    def reason(self, query: str, kb_results: List[Tuple[str, Dict, float]]) -> Dict:
        """
        Thực hiện suy luận để tạo câu trả lời từ kết quả KB
        
        Args:
            query: Câu hỏi của người dùng
            kb_results: Kết quả từ Knowledge Base, mỗi phần tử là (node_id, attributes, relevance)
        
        Returns:
            dict: Kết quả trả về gồm answer và metadata
        """
        self.logger.info(f"Suy luận dựa trên {len(kb_results)} kết quả từ KB")
        
        start_time = time.time()
        
        if not kb_results:
            return {
                "answer": "Tôi không có đủ thông tin để trả lời câu hỏi này.",
                "confidence": 0.0,
                "sources": [],
                "success": False
            }
        
        try:
            # Phân loại loại câu hỏi
            question_type = self._classify_question(query)
            self.logger.debug(f"Loại câu hỏi: {question_type}")
            
            # Lấy các thông tin cần thiết từ kb_results
            sources = set()
            node_contents = []
            for node, attrs, relevance in kb_results:
                if attrs.get("source") and attrs["source"] != "unknown":
                    sources.add(attrs["source"])
                
                node_contents.append({
                    "text": attrs.get("description", ""),
                    "name": attrs.get("name", str(node)),
                    "type": attrs.get("type", "entity"),
                    "relevance": relevance
                })
            
            # Tạo câu trả lời dựa trên loại câu hỏi
            answer, confidence = self._generate_answer(question_type, query, node_contents)
            
            # Tính thời gian suy luận
            reasoning_time = time.time() - start_time
            
            result = {
                "answer": answer,
                "confidence": confidence,
                "sources": list(sources),
                "reasoning_time": reasoning_time,
                "question_type": question_type,
                "success": True
            }
            
            return result
            
        except Exception as e:
            self.logger.error(f"Lỗi trong quá trình suy luận: {e}", exc_info=True)
            return {
                "answer": "Đã xảy ra lỗi khi xử lý câu hỏi của bạn.",
                "confidence": 0.0,
                "sources": [],
                "success": False,
                "error": str(e)
            }
    
    def evaluate_relevance(self, kb_results: List[Tuple[str, Dict, float]], query: str) -> float:
        """
        Đánh giá độ liên quan của kết quả KB với câu hỏi
        
        Args:
            kb_results: Kết quả từ KB
            query: Câu hỏi của người dùng
            
        Returns:
            float: Độ liên quan từ 0.0 đến 1.0
        """
        if not kb_results:
            return 0.0
            
        # Tính trung bình độ liên quan của các kết quả
        relevance_sum = sum(rel for _, _, rel in kb_results)
        avg_relevance = relevance_sum / len(kb_results)
        
        # Nếu có ít nhất một kết quả có độ liên quan cao
        max_relevance = max(rel for _, _, rel in kb_results)
        
        # Kết hợp trung bình và giá trị lớn nhất
        final_relevance = 0.7 * max_relevance + 0.3 * avg_relevance
        
        self.logger.debug(f"Độ liên quan: max={max_relevance:.2f}, avg={avg_relevance:.2f}, final={final_relevance:.2f}")
        return final_relevance
    
    def solve_math_problem(self, query: str, kb_results: List[Tuple[str, Dict, float]]) -> Dict:
        """
        Giải quyết bài toán lớp 1
        
        Args:
            query: Câu hỏi toán học
            kb_results: Kết quả từ Knowledge Base
        
        Returns:
            dict: Kết quả bao gồm câu trả lời và giải thích
        """
        # Nhận dạng loại bài toán
        problem_type = self._identify_math_problem_type(query)
        
        # Trích xuất số từ câu hỏi
        numbers = self._extract_numbers(query)
        
        # Giải quyết dựa vào loại bài toán
        if problem_type == "addition":
            return self._solve_addition(numbers, query)
        elif problem_type == "subtraction":
            return self._solve_subtraction(numbers, query)
        elif problem_type == "comparison":
            return self._solve_comparison(numbers, query)
        else:
            # Tìm kiếm trong KB nếu không nhận dạng được loại toán
            return self._find_answer_in_kb(query, kb_results)
    
    def _classify_question(self, query: str) -> str:
        """
        Phân loại loại câu hỏi
        
        Args:
            query: Câu hỏi cần phân loại
            
        Returns:
            str: Loại câu hỏi (definition, explanation, how_to, ...)
        """
        query = query.lower()
        
        # Phân loại câu hỏi dựa trên từ khóa
        if any(word in query for word in ["là gì", "định nghĩa", "khái niệm", "nghĩa là gì"]):
            return "definition"
        elif any(word in query for word in ["tại sao", "vì sao", "lý do", "nguyên nhân"]):
            return "explanation"
        elif any(word in query for word in ["làm thế nào", "làm sao", "cách", "phương pháp", "hướng dẫn"]):
            return "how_to"
        elif any(word in query for word in ["ví dụ", "minh họa", "ví dụ về"]):
            return "example"
        elif any(word in query for word in ["so sánh", "khác nhau", "giống nhau", "khác biệt"]):
            return "comparison"
        elif any(word in query for word in ["liệt kê", "danh sách", "các loại", "những loại"]):
            return "list"
        else:
            return "information"
    
    def _generate_answer(self, question_type: str, query: str, node_contents: List[Dict]) -> Tuple[str, float]:
        """
        Tạo câu trả lời dựa trên loại câu hỏi và nội dung từ KB
        
        Args:
            question_type: Loại câu hỏi
            query: Câu hỏi gốc
            node_contents: Nội dung từ các node liên quan
            
        Returns:
            tuple: (answer, confidence)
        """
        # Sắp xếp theo độ liên quan
        node_contents.sort(key=lambda x: x["relevance"], reverse=True)
        
        # Tính mức độ tin cậy dựa trên độ liên quan và số lượng thông tin
        confidence = min(0.9, node_contents[0]["relevance"]) if node_contents else 0.0
        
        if not node_contents:
            return "Tôi không có đủ thông tin để trả lời câu hỏi này.", confidence
        
        # Tạo câu trả lời dựa vào loại câu hỏi
        if question_type == "definition":
            return self._answer_definition(query, node_contents), confidence
        elif question_type == "explanation":
            return self._answer_explanation(query, node_contents), confidence
        elif question_type == "how_to":
            return self._answer_how_to(query, node_contents), confidence
        elif question_type == "example":
            return self._answer_example(query, node_contents), confidence
        elif question_type == "comparison":
            return self._answer_comparison(query, node_contents), confidence
        elif question_type == "list":
            return self._answer_list(query, node_contents), confidence
        else:
            return self._answer_information(query, node_contents), confidence
    
    def _identify_math_problem_type(self, query: str) -> str:
        """Xác định loại bài toán lớp 1"""
        query_lower = query.lower()
        
        # Từ khóa cho từng loại toán
        addition_keywords = ["cộng", "tổng", "thêm", "tất cả", "có bao nhiêu", "+"]
        subtraction_keywords = ["trừ", "hiệu", "bớt", "còn lại", "mất đi", "vẫn còn", "-"]
        comparison_keywords = ["hơn", "kém", "nhiều hơn", "ít hơn", "lớn hơn", "nhỏ hơn", "so sánh"]
        
        # Xác định loại toán
        if "+" in query or any(keyword in query_lower for keyword in addition_keywords):
            return "addition"
        elif "-" in query or any(keyword in query_lower for keyword in subtraction_keywords):
            return "subtraction"
        elif any(keyword in query_lower for keyword in comparison_keywords):
            return "comparison"
        else:
            return "unknown"
    
    def _extract_numbers(self, query: str) -> List[int]:
        """Trích xuất các số từ câu hỏi"""
        import re
        
        # Tìm tất cả các số trong câu hỏi
        numbers = re.findall(r'\d+', query)
        
        # Chuyển về số nguyên
        return [int(num) for num in numbers]
    
    def _solve_addition(self, numbers: List[int], query: str) -> Dict:
        """Giải bài toán cộng"""
        if len(numbers) < 2:
            return {
                "answer": "Tôi không tìm thấy đủ số để thực hiện phép cộng.",
                "confidence": 0.5
            }
        
        # Lấy 2 số đầu tiên để cộng
        operands = numbers[:2]
        result = sum(operands)
        explanation = f"{operands[0]} + {operands[1]} = {result}"
        
        answer = f"Kết quả phép tính {operands[0]} + {operands[1]} = {result}."
        
        if "tại sao" in query.lower() or "vì sao" in query.lower() or "giải thích" in query.lower():
            answer += f"\n\nGiải thích: Để tính {operands[0]} + {operands[1]}, chúng ta cộng {operands[0]} và {operands[1]} lại với nhau và được kết quả là {result}."
            
            # Thêm giải thích cụ thể cho học sinh lớp 1
            if operands[0] <= 10 and operands[1] <= 10:
                answer += f"\n\nChúng ta có thể hình dung bằng cách đếm: {' + '.join(['●' * operands[0], '●' * operands[1]])} = {'●' * result}."
        
        return {
            "answer": answer,
            "explanation": explanation,
            "operation": "addition",
            "numbers": operands,
            "result": result,
            "confidence": 0.9
        }
    
    def _solve_subtraction(self, numbers: List[int], query: str) -> Dict:
        """Giải bài toán trừ"""
        if len(numbers) < 2:
            return {
                "answer": "Tôi không tìm thấy đủ số để thực hiện phép trừ.",
                "confidence": 0.5
            }
        
        # Lấy 2 số đầu tiên để trừ
        operands = numbers[:2]
        result = operands[0] - operands[1]
        explanation = f"{operands[0]} - {operands[1]} = {result}"
        
        answer = f"Kết quả phép tính {operands[0]} - {operands[1]} = {result}."
        
        if "tại sao" in query.lower() or "vì sao" in query.lower() or "giải thích" in query.lower():
            answer += f"\n\nGiải thích: Để tính {operands[0]} - {operands[1]}, chúng ta lấy {operands[0]} trừ đi {operands[1]} và được kết quả là {result}."
            
            # Thêm giải thích cụ thể cho học sinh lớp 1
            if operands[0] <= 20:
                dots = '●' * operands[0]
                crossed = '●' * operands[1]
                remaining = '●' * result
                answer += f"\n\nChúng ta có thể hình dung: {dots} trừ đi {crossed} còn lại {remaining}."
        
        return {
            "answer": answer,
            "explanation": explanation,
            "operation": "subtraction",
            "numbers": operands,
            "result": result,
            "confidence": 0.9
        }
    
    def _solve_comparison(self, numbers: List[int], query: str) -> Dict:
        """Giải bài toán so sánh"""
        if len(numbers) < 2:
            return {
                "answer": "Tôi không tìm thấy đủ số để thực hiện phép so sánh.",
                "confidence": 0.5
            }
        
        # Lấy 2 số đầu tiên để so sánh
        num1, num2 = numbers[0], numbers[1]
        
        if num1 > num2:
            difference = num1 - num2
            explanation = f"{num1} > {num2}, {num1} lớn hơn {num2} là {difference}"
            answer = f"{num1} lớn hơn {num2} là {difference}."
        elif num1 < num2:
            difference = num2 - num1
            explanation = f"{num1} < {num2}, {num1} nhỏ hơn {num2} là {difference}"
            answer = f"{num1} nhỏ hơn {num2} là {difference}."
        else:
            explanation = f"{num1} = {num2}, hai số bằng nhau"
            answer = f"{num1} bằng {num2}."
        
        if "tại sao" in query.lower() or "vì sao" in query.lower() or "giải thích" in query.lower():
            answer += f"\n\nGiải thích: Chúng ta so sánh hai số {num1} và {num2}."
            if num1 != num2:
                larger = max(num1, num2)
                smaller = min(num1, num2)
                diff = larger - smaller
                answer += f" Vì {larger} - {smaller} = {diff}, nên {larger} lớn hơn {smaller} là {diff} đơn vị."
            else:
                answer += f" Vì hai số có giá trị giống nhau, nên chúng bằng nhau."
        
        return {
            "answer": answer,
            "explanation": explanation,
            "operation": "comparison",
            "numbers": [num1, num2],
            "result": difference if num1 != num2 else 0,
            "comparison": ">" if num1 > num2 else ("<" if num1 < num2 else "="),
            "confidence": 0.9
        }
    
    def _find_answer_in_kb(self, query: str, kb_results: List[Tuple[str, Dict, float]]) -> Dict:
        """Tìm câu trả lời trong KB nếu không nhận dạng được phép tính"""
        if not kb_results:
            return {
                "answer": "Tôi không tìm thấy thông tin để trả lời câu hỏi toán học này.",
                "confidence": 0.3
            }
        
        # Sắp xếp kb_results theo độ liên quan
        kb_results.sort(key=lambda x: x[2], reverse=True)
        
        # Lấy node liên quan nhất
        node_id, attrs, relevance = kb_results[0]
        
        if attrs.get("type") == "knowledge" and "description" in attrs:
            # Nếu đây là node kiến thức cụ thể
            answer = f"{attrs.get('description', '')}"
            
            # Nếu là phép cộng/trừ cụ thể
            if attrs.get("name", "").startswith("Phép cộng") or attrs.get("name", "").startswith("Phép trừ"):
                # Nếu mô tả dạng "a+b=c" hoặc "a-b=c"
                math_expression = attrs.get("description", "")
                
                if "+" in math_expression:
                    parts = math_expression.split("+")
                    if len(parts) == 2 and "=" in parts[1]:
                        num1 = parts[0].strip()
                        num2, result = parts[1].split("=")[0].strip(), parts[1].split("=")[1].strip()
                        answer = f"Kết quả của {num1} + {num2} = {result}"
                
                elif "-" in math_expression:
                    parts = math_expression.split("-")
                    if len(parts) == 2 and "=" in parts[1]:
                        num1 = parts[0].strip()
                        num2, result = parts[1].split("=")[0].strip(), parts[1].split("=")[1].strip()
                        answer = f"Kết quả của {num1} - {num2} = {result}"
            
            return {
                "answer": answer,
                "confidence": min(0.8, relevance),
                "source": attrs.get("source", "knowledge_base"),
                "success": True
            }
        
        # Không tìm thấy câu trả lời cụ thể
        # Kiểm tra các phép tính đơn giản
        numbers = self._extract_numbers(query)
        if len(numbers) >= 2:
            # Thử đoán phép tính
            if "+" in query or "cộng" in query.lower() or "tổng" in query.lower():
                return self._solve_addition(numbers, query)
            elif "-" in query or "trừ" in query.lower() or "hiệu" in query.lower() or "còn lại" in query.lower():
                return self._solve_subtraction(numbers, query)
        
        # Trả về thông tin chung
        answer = "Tôi không đủ thông tin để trả lời câu hỏi toán học này một cách chính xác. "
        
        if len(kb_results) > 0:
            answer += f"Có thể bạn đang hỏi về {kb_results[0][1].get('name', '')}? Vui lòng cung cấp thêm thông tin để tôi có thể giúp bạn."
        
        return {
            "answer": answer,
            "confidence": 0.3,
            "success": False
        }
    
    def _answer_definition(self, query: str, node_contents: List[Dict]) -> str:
        """Trả lời câu hỏi định nghĩa"""
        keywords = extract_keywords(query)
        
        # Tìm node phù hợp nhất để định nghĩa
        relevant_nodes = []
        for node in node_contents:
            name = node["name"].lower()
            if any(keyword in name for keyword in keywords):
                relevant_nodes.append(node)
        
        # Nếu không tìm thấy, sử dụng node có độ liên quan cao nhất
        if not relevant_nodes:
            relevant_nodes = [node_contents[0]]
        
        # Tạo câu trả lời
        definition = relevant_nodes[0]["text"]
        name = relevant_nodes[0]["name"]
        
        if not definition:
            return f"Tôi biết về {name} nhưng không có định nghĩa cụ thể."
        
        return f"{name} là {definition}"
    
    def _answer_explanation(self, query: str, node_contents: List[Dict]) -> str:
        """Trả lời câu hỏi giải thích"""
        # Kết hợp thông tin từ các node liên quan
        explanations = []
        for node in node_contents[:3]:  # Chỉ lấy 3 node liên quan nhất
            if node["text"]:
                explanations.append(node["text"])
        
        if not explanations:
            return "Tôi không có đủ thông tin để giải thích câu hỏi này."
        
        # Tạo câu trả lời
        return "\n\n".join(explanations)
    
    def _answer_how_to(self, query: str, node_contents: List[Dict]) -> str:
        """Trả lời câu hỏi hướng dẫn"""
        # Tìm các node có thông tin hướng dẫn
        how_to_nodes = [node for node in node_contents if len(node["text"]) > 50]
        
        if not how_to_nodes:
            return "Tôi không có hướng dẫn cụ thể cho câu hỏi này."
        
        # Tạo câu trả lời
        answer = "Đây là hướng dẫn:\n\n"
        for i, node in enumerate(how_to_nodes[:2], 1):  # Chỉ lấy 2 node liên quan nhất
            answer += f"{node['text']}\n\n"
        
        return answer
    
    def _answer_example(self, query: str, node_contents: List[Dict]) -> str:
        """Trả lời câu hỏi ví dụ"""
        # Tìm các node có ví dụ
        examples = []
        for node in node_contents:
            if "ví dụ" in node["text"].lower():
                examples.append(node["text"])
        
        if not examples:
            # Nếu không tìm thấy ví dụ cụ thể, lấy thông tin chung
            if node_contents:
                return f"Tôi không có ví dụ cụ thể, nhưng đây là thông tin về {node_contents[0]['name']}:\n\n{node_contents[0]['text']}"
            else:
                return "Tôi không có ví dụ cho câu hỏi này."
        
        # Tạo câu trả lời
        return "Ví dụ:\n\n" + "\n\n".join(examples)
    
    def _answer_comparison(self, query: str, node_contents: List[Dict]) -> str:
        """Trả lời câu hỏi so sánh"""
        # Tìm các thực thể cần so sánh
        keywords = extract_keywords(query)
        comparison_nodes = []
        
        for node in node_contents:
            if any(keyword in node["name"].lower() for keyword in keywords):
                comparison_nodes.append(node)
        
        if len(comparison_nodes) < 2:
            return "Tôi không có đủ thông tin để so sánh các đối tượng trong câu hỏi của bạn."
        
        # Tạo câu trả lời
        answer = f"So sánh giữa {comparison_nodes[0]['name']} và {comparison_nodes[1]['name']}:\n\n"
        answer += f"- {comparison_nodes[0]['name']}: {comparison_nodes[0]['text']}\n\n"
        answer += f"- {comparison_nodes[1]['name']}: {comparison_nodes[1]['text']}\n\n"
        
        return answer
    
    def _answer_list(self, query: str, node_contents: List[Dict]) -> str:
        """Trả lời câu hỏi liệt kê"""
        items = []
        
        for node in node_contents:
            items.append(f"- {node['name']}: {node['text']}")
        
        if not items:
            return "Tôi không có thông tin để liệt kê cho câu hỏi này."
        
        # Tạo câu trả lời
        return "Danh sách:\n\n" + "\n\n".join(items[:5])  # Giới hạn 5 mục
    
    def _answer_information(self, query: str, node_contents: List[Dict]) -> str:
        """Trả lời câu hỏi thông tin chung"""
        # Tìm node có thông tin phù hợp nhất
        relevant_info = []
        
        for node in node_contents[:3]:  # Chỉ lấy 3 node liên quan nhất
            if node["text"]:
                relevant_info.append(node["text"])
        
        if not relevant_info:
            return "Tôi không có thông tin cụ thể cho câu hỏi này."
        
        # Tạo câu trả lời
        return "\n\n".join(relevant_info)