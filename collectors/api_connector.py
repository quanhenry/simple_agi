"""
API Connector - Kết nối với các API của các mô hình lớn để thu thập thông tin, tập trung vào toán lớp 1
"""

import logging
import time
import json
import os
from typing import List, Dict, Any, Optional, Tuple

import config

# Thư viện tùy chọn, sẽ được import khi cần
openai_available = False
google_available = False
anthropic_available = False

try:
    import openai
    openai_available = True
except ImportError:
    pass

try:
    import google.generativeai as genai
    google_available = True
except ImportError:
    pass

try:
    import anthropic
    anthropic_available = True
except ImportError:
    pass

class ApiConnector:
    """
    Kết nối với các API của các mô hình lớn để thu thập thông tin về toán lớp 1
    """
    
    def __init__(self):
        """Khởi tạo API connector"""
        self.logger = logging.getLogger("ApiConnector")
        
        # Thiết lập API keys từ biến môi trường nếu không có trong config
        self._setup_api_keys()
        
        # Kiểm tra các API có sẵn
        self.apis_available = self._check_available_apis()
        
        # Khởi tạo các client nếu có thể
        self.clients = self._initialize_clients()
        
        # Ghi log thông tin
        if self.apis_available:
            api_names = ", ".join(self.apis_available)
            self.logger.info(f"API Connector đã được khởi tạo với các API: {api_names}")
        else:
            self.logger.warning("Không có API nào được cấu hình hoặc có sẵn")
    
    def _setup_api_keys(self):
        """
        Thiết lập API keys từ biến môi trường nếu chưa có trong config
        """
        # Đảm bảo config.API_KEYS tồn tại
        if not hasattr(config, 'API_KEYS'):
            config.API_KEYS = {}
        
        # Thiết lập Google API Key
        if not config.API_KEYS.get("google"):
            google_api_key = os.environ.get("GOOGLE_API_KEY") or "AIzaSyDvYUe2IgWpsjrOZeN699CgzqeVMcDof2U"
            config.API_KEYS["google"] = google_api_key
            self.logger.info(f"Đã thiết lập Google API Key từ biến môi trường hoặc giá trị mặc định")
        
        # Thiết lập các API keys khác tương tự nếu cần
        
        # Thiết lập API mặc định
        if not hasattr(config, 'DEFAULT_API_MODEL'):
            config.DEFAULT_API_MODEL = "google-gemini"
    
    def _check_available_apis(self) -> List[str]:
        """
        Kiểm tra các API có sẵn và được cấu hình
        
        Returns:
            list: Danh sách các API có sẵn
        """
        available = []
        
        # Kiểm tra OpenAI
        if openai_available and config.API_KEYS.get("openai"):
            available.append("openai")
            
        # Kiểm tra Google
        if google_available and config.API_KEYS.get("google"):
            available.append("google")
            self.logger.info(f"Google API được kích hoạt với key: {config.API_KEYS['google'][:5]}...")
            
        # Kiểm tra Anthropic
        if anthropic_available and config.API_KEYS.get("anthropic"):
            available.append("anthropic")
            
        return available
    
    def _initialize_clients(self) -> Dict[str, Any]:
        """
        Khởi tạo các client cho các API
        
        Returns:
            dict: Dictionary chứa các client
        """
        clients = {}
        
        try:
            # Khởi tạo client OpenAI
            if "openai" in self.apis_available:
                openai.api_key = config.API_KEYS["openai"]
                clients["openai"] = openai
                self.logger.info("Đã khởi tạo OpenAI client")
                
            # Khởi tạo client Google
            if "google" in self.apis_available:
                genai.configure(api_key=config.API_KEYS["google"])
                clients["google"] = genai
                self.logger.info("Đã khởi tạo Google Gemini client")
                
            # Khởi tạo client Anthropic
            if "anthropic" in self.apis_available:
                clients["anthropic"] = anthropic.Anthropic(api_key=config.API_KEYS["anthropic"])
                self.logger.info("Đã khởi tạo Anthropic client")
                
        except Exception as e:
            self.logger.error(f"Lỗi khi khởi tạo clients: {e}", exc_info=True)
            
        return clients
    
    def collect(self, query: str, max_items: int = 2) -> List[Dict[str, Any]]:
        """
        Thu thập thông tin từ các API về toán lớp 1
        
        Args:
            query: Câu hỏi cần thu thập thông tin
            max_items: Số lượng kết quả tối đa cần thu thập
        
        Returns:
            list: Danh sách thông tin thu thập được
        """
        self.logger.info(f"Thu thập từ API cho query: {query}")
        
        if not self.apis_available:
            self.logger.warning("Không có API nào được cấu hình, bỏ qua thu thập")
            return []
        
        results = []
        apis_to_try = self.apis_available.copy()
        
        # Ưu tiên API được cấu hình mặc định
        default_api = config.DEFAULT_API_MODEL.split("-")[0].lower()
        if default_api in apis_to_try:
            apis_to_try.remove(default_api)
            apis_to_try.insert(0, default_api)
        
        # Thử lần lượt các API cho đến khi đủ kết quả
        for api_name in apis_to_try:
            if len(results) >= max_items:
                break
                
            try:
                self.logger.info(f"Đang truy vấn API: {api_name}")
                api_results = self._query_api(api_name, query)
                
                if api_results:
                    results.extend(api_results)
                    self.logger.info(f"Đã thu thập được {len(api_results)} kết quả từ {api_name}")
                
            except Exception as e:
                self.logger.error(f"Lỗi khi truy vấn API {api_name}: {e}", exc_info=True)
        
        # Giới hạn số lượng kết quả
        results = results[:max_items]
        
        self.logger.info(f"Tổng cộng thu thập được {len(results)} kết quả từ API")
        return results
    
    def _query_api(self, api_name: str, query: str) -> List[Dict[str, Any]]:
        """
        Truy vấn một API cụ thể
        
        Args:
            api_name: Tên API cần truy vấn
            query: Câu hỏi cần truy vấn
        
        Returns:
            list: Danh sách kết quả từ API
        """
        if api_name == "openai":
            return self._query_openai(query)
        elif api_name == "google":
            return self._query_google(query)
        elif api_name == "anthropic":
            return self._query_anthropic(query)
        else:
            self.logger.warning(f"API không được hỗ trợ: {api_name}")
            return []
    
    def _query_openai(self, query: str) -> List[Dict[str, Any]]:
        """Truy vấn API OpenAI cho thông tin toán lớp 1"""
        if "openai" not in self.clients:
            return []
            
        # Chuẩn bị prompt tập trung vào toán lớp 1
        system_message = """
        Bạn là trợ lý toán học cho học sinh lớp 1. 
        Hãy cung cấp thông tin chi tiết và chính xác về chủ đề toán học được hỏi, 
        phù hợp với trình độ lớp 1 (6-7 tuổi).
        
        Trả lời bằng JSON với các trường:
        - title: tiêu đề ngắn gọn
        - content: nội dung chi tiết phù hợp với trình độ lớp 1
        - entities: danh sách các khái niệm toán học liên quan (tên, loại, mô tả)
        - relations: danh sách các ví dụ tính toán cụ thể (nếu phù hợp)
        
        Các chủ đề toán lớp 1 bao gồm: đếm đến 100, phép cộng/trừ trong phạm vi 100, 
        so sánh số, hình học cơ bản (hình vuông, tam giác, tròn), đo lường đơn giản.
        """
        
        prompt = f"Cung cấp thông tin về toán lớp 1: {query}"
        
        try:
            response = self.clients["openai"].chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            # Xử lý phản hồi
            content = response.choices[0].message.content
            
            # Cố gắng phân tích JSON
            try:
                data = json.loads(content)
                
                # Tạo kết quả đúng định dạng
                result = {
                    "title": data.get("title", f"Thông tin về {query}"),
                    "content": data.get("content", ""),
                    "source": "openai",
                    "timestamp": time.time(),
                    "confidence": 0.85,
                    "entities": data.get("entities", []),
                    "relations": data.get("relations", [])
                }
                
                return [result]
                
            except json.JSONDecodeError:
                # Nếu không phải JSON, tạo kết quả thủ công
                result = {
                    "title": f"Thông tin về {query}",
                    "content": content,
                    "source": "openai",
                    "timestamp": time.time(),
                    "confidence": 0.7,
                    "entities": [
                        {
                            "name": query,
                            "type": "concept",
                            "description": content[:200]
                        }
                    ],
                    "relations": []
                }
                
                return [result]
                
        except Exception as e:
            self.logger.error(f"Lỗi khi truy vấn OpenAI: {e}")
            return []
    
    def _query_google(self, query: str) -> List[Dict[str, Any]]:
        """Truy vấn API Google (Gemini) cho thông tin toán lớp 1"""
        if "google" not in self.clients:
            self.logger.error("Google client không khả dụng")
            return []
            
        try:
            # Sử dụng API key từ config
            genai.configure(api_key=config.API_KEYS["google"])
            self.logger.info("Đã cấu hình lại Google Gemini với API key")
            
            # Tạo mô hình Gemini Pro
            model = self.clients["google"].GenerativeModel('gemini-2.0-flash')
            self.logger.info("Đã tạo mô hình Gemini Pro")
            
            # Chuẩn bị prompt chi tiết về toán lớp 1
            prompt = f"""
            Cung cấp thông tin đầy đủ và chính xác về chủ đề toán học lớp 1 sau: {query}
            
            Hãy trả lời chi tiết, đầy đủ và chính xác, phù hợp với trình độ của học sinh lớp 1 (6-7 tuổi).
            
            Tập trung vào các khía cạnh:
            - Giải thích đơn giản các khái niệm liên quan
            - Cung cấp các ví dụ cụ thể (chẳng hạn: 5+3=8, 10-4=6)
            - Liên hệ với các tình huống thực tế mà học sinh lớp 1 có thể hiểu được
            - Nếu là phép tính, hãy cung cấp các mẹo tính toán đơn giản
            
            Hãy sử dụng ngôn ngữ đơn giản, dễ hiểu cho học sinh lớp 1.
            """
            
            # Gọi API
            self.logger.info(f"Đang gửi yêu cầu đến Gemini: {query}")
            response = model.generate_content(prompt)
            self.logger.info("Đã nhận phản hồi từ Gemini")
            
            # Xử lý kết quả
            if hasattr(response, 'text'):
                content = response.text
                self.logger.info(f"Nhận được phản hồi dài {len(content)} ký tự")
                
                # Trích xuất tên khái niệm toán học từ nội dung
                math_concepts = [
                    "phép cộng", "phép trừ", "số tự nhiên", "hình học", 
                    "hình vuông", "hình tròn", "tam giác", "đo lường"
                ]
                
                entities = []
                for concept in math_concepts:
                    if concept.lower() in content.lower():
                        # Tìm câu chứa khái niệm này
                        sentences = content.split('.')
                        description = ""
                        for sentence in sentences:
                            if concept.lower() in sentence.lower():
                                description = sentence.strip()
                                break
                        
                        entities.append({
                            "name": concept,
                            "type": "concept",
                            "description": description or f"Liên quan đến {concept}"
                        })
                
                # Trích xuất các phép tính toán học từ nội dung
                relations = []
                # Tìm các dạng phép tính như a+b=c hoặc a-b=c
                import re
                add_pattern = r'(\d+)\s*\+\s*(\d+)\s*=\s*(\d+)'
                sub_pattern = r'(\d+)\s*-\s*(\d+)\s*=\s*(\d+)'
                
                for match in re.finditer(add_pattern, content):
                    a, b, c = match.groups()
                    relations.append({
                        "source": a,
                        "target": c,
                        "relation_type": "addition",
                        "description": f"{a} + {b} = {c}"
                    })
                
                for match in re.finditer(sub_pattern, content):
                    a, b, c = match.groups()
                    relations.append({
                        "source": a,
                        "target": c,
                        "relation_type": "subtraction",
                        "description": f"{a} - {b} = {c}"
                    })
                
                # Tạo tiêu đề dựa trên nội dung
                lines = content.split('\n')
                title_candidates = [line for line in lines[:2] if len(line) > 10 and len(line) < 100]
                title = title_candidates[0] if title_candidates else f"Thông tin về {query}"
                
                # Tạo kết quả
                result = {
                    "title": title,
                    "content": content,
                    "source": "google_gemini",
                    "timestamp": time.time(),
                    "confidence": 0.9,  # Gemini thường cho kết quả tốt
                    "entities": entities,
                    "relations": relations
                }
                
                self.logger.info(f"Đã xử lý phản hồi thành công với {len(entities)} entities")
                return [result]
            else:
                self.logger.warning("Phản hồi từ Gemini không có thuộc tính text")
                return []
            
        except Exception as e:
            self.logger.error(f"Lỗi khi truy vấn Google Gemini: {e}", exc_info=True)
            
            # Tạo kết quả lỗi để hệ thống có thông tin
            error_result = {
                "title": f"Lỗi khi truy vấn về {query}",
                "content": f"Đã xảy ra lỗi khi truy vấn Google Gemini: {str(e)}",
                "source": "google_gemini_error",
                "timestamp": time.time(),
                "confidence": 0.1,
                "entities": [],
                "relations": []
            }
            
            return [error_result]
    
    def _query_anthropic(self, query: str) -> List[Dict[str, Any]]:
        """Truy vấn API Anthropic (Claude) cho thông tin toán lớp 1"""
        if "anthropic" not in self.clients:
            return []
            
        try:
            response = self.clients["anthropic"].messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1000,
                temperature=0.3,
                system="Bạn là trợ lý toán học cho học sinh lớp 1. Hãy giải thích các khái niệm toán học đơn giản phù hợp với trình độ lớp 1 (6-7 tuổi).",
                messages=[
                    {"role": "user", "content": f"Giải thích về toán lớp 1: {query}. Hãy đưa ra các ví dụ cụ thể phù hợp với lứa tuổi."}
                ]
            )
            
            # Tạo kết quả
            result = {
                "title": f"Thông tin về {query}",
                "content": response.content[0].text,
                "source": "anthropic_claude",
                "timestamp": time.time(),
                "confidence": 0.85,
                "entities": [
                    {
                        "name": query,
                        "type": "concept",
                        "description": response.content[0].text[:200]
                    }
                ],
                "relations": []
            }
            
            return [result]
            
        except Exception as e:
            self.logger.error(f"Lỗi khi truy vấn Anthropic Claude: {e}")
            return []