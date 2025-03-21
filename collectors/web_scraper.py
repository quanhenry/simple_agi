"""
Web Scraper - Thu thập thông tin từ internet, tập trung vào toán lớp 1
"""

import logging
import time
import random
import re
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

import config
from utils.validators import is_valid_url
from utils.nlp_utils import extract_keywords, clean_text

class WebScraper:
    """
    Thu thập thông tin từ internet, tập trung vào toán lớp 1
    """
    
    def __init__(self):
        """Khởi tạo web scraper"""
        self.logger = logging.getLogger("WebScraper")
        self.headers = {
            "User-Agent": config.USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "vi-VN,vi;q=0.8,en-US;q=0.5,en;q=0.3",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0"
        }
        self.session = requests.Session()
        self.logger.info("Web Scraper đã được khởi tạo")
    
    def collect(self, query: str, max_items: int = 3) -> List[Dict[str, Any]]:
        """
        Thu thập thông tin từ web
        
        Args:
            query: Câu hỏi cần thu thập thông tin
            max_items: Số lượng mục tối đa cần thu thập
        
        Returns:
            list: Danh sách thông tin thu thập được
        """
        self.logger.info(f"Thu thập từ web cho query: {query}")
        search_urls = self._search(query, max_results=max_items * 2)  # Tìm nhiều URL hơn để dự phòng
        
        if not search_urls:
            self.logger.warning("Không tìm được URL nào từ kết quả tìm kiếm")
            return []
        
        # Thu thập thông tin từ các URL tìm được
        results = []
        for url in search_urls:
            if len(results) >= max_items:
                break
                
            try:
                self.logger.debug(f"Đang thu thập từ URL: {url}")
                content = self._scrape_url(url)
                
                if content:
                    self.logger.debug(f"Đã thu thập được nội dung từ URL: {url}")
                    results.append(content)
                    
                    # Tạm dừng để tránh bị chặn
                    time.sleep(random.uniform(1.0, 2.0))
                
            except Exception as e:
                self.logger.error(f"Lỗi khi thu thập từ URL {url}: {e}")
        
        self.logger.info(f"Đã thu thập được {len(results)} thông tin từ web")
        return results
    
    def _search(self, query: str, max_results: int = 5) -> List[str]:
        """
        Tìm kiếm các URL phù hợp
        
        Args:
            query: Câu hỏi cần tìm kiếm
            max_results: Số lượng URL tối đa cần tìm
        
        Returns:
            list: Danh sách URL
        """
        self.logger.info(f"Tìm kiếm cho: {query}")
        
        # Xác định chủ đề toán học từ câu truy vấn
        topics = self._identify_math_topics(query)
        
        # Lấy URL liên quan đến các chủ đề
        math_resources = {
            "addition": [
                "https://www.mathplayground.com/grade_1_games.html",
                "https://www.khanacademy.org/math/arithmetic/arith-review-add-subtract",
                "https://www.education.com/resources/first-grade/addition/",
                "https://www.ixl.com/math/grade-1/addition"
            ],
            "subtraction": [
                "https://www.mathisfun.com/numbers/subtraction.html",
                "https://www.education.com/resources/first-grade/subtraction/",
                "https://www.ixl.com/math/grade-1/subtraction",
                "https://www.mathplayground.com/math_games.html"
            ],
            "counting": [
                "https://www.education.com/resources/first-grade/counting-numbers/",
                "https://www.ixl.com/math/grade-1/counting",
                "https://www.mathgames.com/counting"
            ],
            "shapes": [
                "https://www.mathisfun.com/geometry/shapes.html",
                "https://www.education.com/resources/first-grade/geometry/",
                "https://www.ixl.com/math/grade-1/shapes"
            ],
            "comparison": [
                "https://www.ixl.com/math/grade-1/comparing",
                "https://www.mathisfun.com/comparing-numbers.html",
                "https://www.education.com/resources/comparing-numbers/"
            ],
            "word_problems": [
                "https://www.mathplayground.com/wpdatabase/wpindex.html",
                "https://www.ixl.com/math/grade-1/word-problems",
                "https://www.education.com/resources/first-grade/word-problems/"
            ]
        }
        
        # Lấy URL liên quan đến các chủ đề
        urls = []
        for topic in topics:
            if topic in math_resources:
                urls.extend(math_resources[topic])
        
        # Nếu không tìm thấy URL nào, sử dụng các URL mặc định
        if not urls:
            default_urls = [
                "https://www.mathisfun.com/numbers/index.html",
                "https://www.ixl.com/math/grade-1",
                "https://www.education.com/resources/first-grade/math/",
                "https://www.khanacademy.org/math/early-math"
            ]
            urls.extend(default_urls)
        
        # Lọc URL theo tên miền được tin cậy
        filtered_urls = []
        for url in urls:
            domain = urlparse(url).netloc
            if any(trusted in domain for trusted in config.TRUSTED_DOMAINS):
                filtered_urls.append(url)
                
                if len(filtered_urls) >= max_results:
                    break
        
        self.logger.debug(f"Tìm thấy {len(filtered_urls)} URL tin cậy")
        return filtered_urls
    
    def _identify_math_topics(self, query: str) -> List[str]:
        """Xác định chủ đề toán học từ câu truy vấn"""
        topics = []
        
        # Từ khóa cho từng chủ đề
        topic_keywords = {
            "addition": ["cộng", "tổng", "thêm", "cộng vào", "+"],
            "subtraction": ["trừ", "hiệu", "bớt", "còn lại", "-"],
            "counting": ["đếm", "số", "bao nhiêu"],
            "shapes": ["hình", "vuông", "tròn", "tam giác"],
            "comparison": ["lớn hơn", "nhỏ hơn", "so sánh", ">", "<"],
            "word_problems": ["bài toán", "có lời văn", "tình huống"]
        }
        
        # Tìm các chủ đề phù hợp
        query_lower = query.lower()
        for topic, keywords in topic_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                topics.append(topic)
        
        # Nếu không tìm thấy chủ đề nào, trả về mặc định
        if not topics:
            topics = ["addition"]  # Mặc định là phép cộng
        
        return topics
    
    def _scrape_url(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Thu thập nội dung từ một URL
        
        Args:
            url: URL cần thu thập
            
        Returns:
            dict/None: Thông tin thu thập được hoặc None nếu thất bại
        """
        if not is_valid_url(url):
            self.logger.warning(f"URL không hợp lệ: {url}")
            return None
        
        try:
            response = self.session.get(
                url,
                headers=self.headers,
                timeout=config.REQUEST_TIMEOUT
            )
            
            if response.status_code != 200:
                self.logger.warning(f"Không thể truy cập URL {url}, mã trạng thái: {response.status_code}")
                return None
            
            # Parse HTML
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Lấy tiêu đề
            title = soup.title.string if soup.title else ""
            title = clean_text(title)
            
            # Lấy nội dung chính
            content = self._extract_math_content(soup, url)
            
            # Tạo thông tin trả về
            result = {
                "title": title,
                "content": content,
                "url": url,
                "source": urlparse(url).netloc,
                "timestamp": time.time(),
                "confidence": 0.7,  # Mức độ tin cậy mặc định cho dữ liệu web
                "entities": self._extract_math_entities(title, content),
                "relations": self._extract_math_relations(title, content)
            }
            
            return result
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Lỗi khi tải URL {url}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Lỗi khi xử lý nội dung từ {url}: {e}")
            return None
    
    def _extract_math_content(self, soup: BeautifulSoup, url: str) -> str:
        """Trích xuất nội dung liên quan đến toán học từ trang web"""
        content = ""
        
        # Các class hoặc id thường chứa nội dung chính
        main_content_selectors = [
            "main", "content", "article", 
            ".main-content", ".article-content", ".entry-content",
            "#main-content", "#content", "#article"
        ]
        
        # Các class hoặc id thường chứa nội dung toán học
        math_content_selectors = [
            ".math", ".mathematics", ".arithmetic", 
            "#math-content", "#lesson-content",
            ".lesson", ".exercise", ".examples"
        ]
        
        # Tìm nội dung toán học trước
        for selector in math_content_selectors:
            elements = soup.select(selector)
            if elements:
                for element in elements:
                    # Lấy nội dung text của phần tử
                    math_content = element.get_text(separator="\n", strip=True)
                    if math_content:
                        content += math_content + "\n\n"
        
        # Nếu không tìm thấy nội dung toán học cụ thể, dùng nội dung chính
        if not content:
            for selector in main_content_selectors:
                elements = soup.select(selector)
                if elements:
                    for element in elements:
                        main_content = element.get_text(separator="\n", strip=True)
                        if main_content:
                            content += main_content + "\n\n"
                            break
                    if content:
                        break
        
        # Nếu vẫn không tìm thấy, lấy tất cả các đoạn văn
        if not content:
            paragraphs = soup.find_all("p")
            content = "\n\n".join(p.get_text(strip=True) for p in paragraphs)
        
        # Làm sạch và cắt ngắn nội dung
        content = clean_text(content)
        content = content[:5000]  # Giới hạn độ dài
        
        return content
    
    def _extract_math_entities(self, title: str, content: str) -> List[Dict[str, Any]]:
        """Trích xuất các thực thể liên quan đến toán học từ nội dung"""
        entities = []
        
        # Trích xuất cụm từ khóa
        keywords = extract_keywords(title + " " + content, max_keywords=20)
        
        # Các từ khóa toán học lớp 1
        math_terms = [
            "số", "đếm", "cộng", "trừ", "tổng", "hiệu", "so sánh",
            "lớn hơn", "nhỏ hơn", "bằng", "hình", "đo lường",
            "dài", "rộng", "tiền", "giờ", "phút"
        ]
        
        # Thêm các thực thể từ từ khóa trích xuất được
        for keyword in keywords:
            # Kiểm tra nếu từ khóa liên quan đến toán
            is_math_related = any(term in keyword.lower() for term in math_terms)
            
            entity_type = "concept" if is_math_related else "general"
            
            # Tìm mô tả ngắn từ nội dung
            description = self._find_description_for_keyword(keyword, content)
            
            entity = {
                "name": keyword,
                "type": entity_type,
                "description": description
            }
            
            entities.append(entity)
        
        # Thêm các thực thể phép tính cụ thể
        math_expressions = self._extract_math_expressions(content)
        for expr in math_expressions:
            if "=" in expr:
                entity = {
                    "name": expr,
                    "type": "knowledge",
                    "description": expr
                }
                entities.append(entity)
        
        return entities
    
    def _extract_math_relations(self, title: str, content: str) -> List[Dict[str, Any]]:
        """Trích xuất các mối quan hệ toán học từ nội dung"""
        relations = []
        
        # Trích xuất các thực thể
        entities = self._extract_math_entities(title, content)
        
        # Tìm các mối quan hệ giữa các thực thể
        for i, entity1 in enumerate(entities):
            if entity1["type"] == "concept":
                for j, entity2 in enumerate(entities):
                    if i != j and entity2["type"] == "concept":
                        # Kiểm tra mối quan hệ
                        relation_type = self._determine_relation_type(entity1["name"], entity2["name"], content)
                        
                        if relation_type:
                            relation = {
                                "source": entity1["name"],
                                "target": entity2["name"],
                                "relation_type": relation_type,
                                "description": f"{entity1['name']} {relation_type} {entity2['name']}"
                            }
                            relations.append(relation)
        
        return relations
    
    def _extract_math_expressions(self, content: str) -> List[str]:
        """Trích xuất các biểu thức toán học từ nội dung"""
        expressions = []
        
        # Tìm các biểu thức dạng x+y=z hoặc x-y=z
        addition_pattern = r'\d+\s*\+\s*\d+\s*=\s*\d+'
        subtraction_pattern = r'\d+\s*-\s*\d+\s*=\s*\d+'
        
        # Tìm tất cả các biểu thức phép cộng
        for match in re.finditer(addition_pattern, content):
            expressions.append(match.group())
        
        # Tìm tất cả các biểu thức phép trừ
        for match in re.finditer(subtraction_pattern, content):
            expressions.append(match.group())
        
        return expressions
    
    def _determine_relation_type(self, entity1: str, entity2: str, content: str) -> Optional[str]:
        """Xác định loại mối quan hệ giữa hai thực thể"""
        # Mối quan hệ đơn giản dựa trên khoảng cách trong văn bản
        entity1_pos = content.lower().find(entity1.lower())
        entity2_pos = content.lower().find(entity2.lower())
        
        if entity1_pos == -1 or entity2_pos == -1:
            return None
        
        # Khoảng cách giữa hai thực thể trong văn bản
        distance = abs(entity1_pos - entity2_pos)
        
        # Nếu khoảng cách đủ gần, có thể có mối quan hệ
        if distance < 200:
            text_between = content[min(entity1_pos, entity2_pos):max(entity1_pos, entity2_pos)]
            
            if "là một phần của" in text_between or "thuộc về" in text_between:
                return "is_part_of"
            elif "bao gồm" in text_between or "có" in text_between:
                return "contains"
            elif "liên quan" in text_between:
                return "relates_to"
            else:
                return "related_to"  # Mối quan hệ chung
        
        return None
    
    def _find_description_for_keyword(self, keyword: str, content: str) -> str:
        """Tìm mô tả cho một từ khóa trong nội dung"""
        keyword_lower = keyword.lower()
        content_lower = content.lower()
        
        # Tìm vị trí của từ khóa trong nội dung
        keyword_pos = content_lower.find(keyword_lower)
        if keyword_pos == -1:
            return ""
        
        # Lấy một đoạn văn có chứa từ khóa
        sentence_start = content.rfind(".", 0, keyword_pos)
        if sentence_start == -1:
            sentence_start = 0
        else:
            sentence_start += 1  # Bỏ qua dấu chấm
        
        sentence_end = content.find(".", keyword_pos)
        if sentence_end == -1:
            sentence_end = len(content)
        
        # Lấy câu chứa từ khóa và câu tiếp theo nếu có
        description = content[sentence_start:sentence_end].strip()
        
        # Nếu mô tả quá ngắn, thử lấy thêm câu tiếp theo
        if len(description) < 50 and sentence_end < len(content) - 1:
            next_sentence_end = content.find(".", sentence_end + 1)
            if next_sentence_end != -1:
                description += content[sentence_end:next_sentence_end + 1]
        
        # Giới hạn độ dài mô tả
        if len(description) > 200:
            description = description[:197] + "..."
        
        return description.strip()