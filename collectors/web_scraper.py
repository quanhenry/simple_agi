"""
Web Scraper - Thu thập thông tin từ internet
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
    Thu thập thông tin từ internet
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
        # Trong thực tế, cần tích hợp với công cụ tìm kiếm như Google Search API
        # Hiện tại, chỉ mô phỏng việc tìm kiếm với một số URL cố định
        
        self.logger.info(f"Mô phỏng tìm kiếm cho: {query}")
        
        # Mô phỏng URL tìm kiếm
        urls = [
            "https://vi.wikipedia.org/wiki/Trí_tuệ_nhân_tạo",
            "https://www.python.org/doc/",
            "https://github.com/topics/artificial-intelligence",
            "https://stackoverflow.com/questions/tagged/machine-learning",
            "https://www.kaggle.com/competitions"
        ]
        
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
            # (Thực tế cần phức tạp hơn để trích xuất nội dung chính từ trang web)
            content = ""
            main_tags = soup.find_all(["article", "main", "div"], class_=re.compile(r"(content|main|article)"))
            
            if main_tags:
                # Lấy nội dung từ tag chứa nhiều văn bản nhất
                main_content = max(main_tags, key=lambda tag: len(tag.get_text()))
                content = main_content.get_text(separator="\n", strip=True)
            else:
                # Fallback: lấy tất cả đoạn văn
                paragraphs = soup.find_all("p")
                content = "\n".join(p.get_text(strip=True) for p in paragraphs)
            
            # Làm sạch và cắt ngắn nội dung
            content = clean_text(content)
            content = content[:5000]  # Giới hạn độ dài
            
            # Trích xuất thông tin
            # Trong thực tế, cần sử dụng NLP để trích xuất entities và relations
            domain = urlparse(url).netloc
            
            # Tạo thông tin trả về
            result = {
                "title": title,
                "content": content,
                "url": url,
                "source": domain,
                "timestamp": time.time(),
                "confidence": 0.7,  # Mức độ tin cậy mặc định cho dữ liệu web
                "entities": [
                    {
                        "name": title,
                        "type": "concept",
                        "description": content[:200]  # Trích 200 ký tự đầu làm mô tả
                    }
                ],
                "relations": []
            }
            
            return result
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Lỗi khi tải URL {url}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Lỗi khi xử lý nội dung từ {url}: {e}")
            return None