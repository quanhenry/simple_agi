"""
Information Collector - Thu thập thông tin từ nhiều nguồn
"""

import logging
import time
from typing import List, Dict, Any, Optional
import threading
import queue

import config
from collectors.web_scraper import WebScraper
from collectors.api_connector import ApiConnector

class InformationCollector:
    """
    Thu thập thông tin từ nhiều nguồn khác nhau
    """
    
    def __init__(self):
        """Khởi tạo Information Collector"""
        self.logger = logging.getLogger("InfoCollector")
        
        # Cấu hình
        self.config = config.INFO_COLLECTOR_CONFIG
        
        # Khởi tạo các nguồn thông tin
        self.web_scraper = WebScraper()
        self.api_connector = ApiConnector()
        
        self.logger.info("Information Collector đã được khởi tạo")
    
    def collect(self, query: str, min_results: int = None) -> List[Dict[str, Any]]:
        """
        Thu thập thông tin từ nhiều nguồn
        
        Args:
            query: Câu hỏi cần thu thập thông tin
            min_results: Số lượng kết quả tối thiểu cần thu thập
            
        Returns:
            list: Danh sách thông tin thu thập được
        """
        if min_results is None:
            min_results = self.config.get('min_sources', 2)
        
        # Thời điểm bắt đầu
        start_time = time.time()
        
        self.logger.info(f"Thu thập thông tin cho query: {query}")
        
        # Kết quả từ tất cả các nguồn
        all_results = []
        
        # Xác định nguồn thông tin cần thu thập
        sources = self.config.get('sources', ['web', 'api'])
        
        # Thu thập từ Web (nếu cần)
        web_results_count = 0
        if 'web' in sources:
            needed_from_web = max(1, min_results - len(all_results))
            self.logger.info(f"Bắt đầu thu thập từ Web (cần thêm {needed_from_web} nguồn)")
            
            web_results = self.web_scraper.collect(query, max_items=needed_from_web)
            web_results_count = len(web_results)
            
            if web_results:
                all_results.extend(web_results)
                self.logger.info(f"Đã thu thập được {len(web_results)} thông tin từ Web")
        
        # Thu thập từ API (nếu cần và web không đủ)
        api_results_count = 0
        if 'api' in sources and len(all_results) < min_results:
            needed_from_api = min_results - len(all_results)
            self.logger.info(f"Bắt đầu thu thập từ API (cần thêm {needed_from_api} nguồn)")
            
            api_results = self.api_connector.collect(query, max_items=needed_from_api)
            api_results_count = len(api_results)
            
            if api_results:
                all_results.extend(api_results)
                self.logger.info(f"Đã thu thập được {len(api_results)} thông tin từ API")
        
        # Tổng kết
        total_time = time.time() - start_time
        self.logger.info(f"Đã thu thập được tổng cộng {len(all_results)} thông tin mới trong {total_time:.2f} giây")
        
        # Báo cáo chi tiết về kết quả thu thập
        self.logger.info(f"Chi tiết: Web={web_results_count}, API={api_results_count}")
        
        # Trả về danh sách kết quả
        return all_results
    
    def collect_parallel(self, query: str, min_results: int = None) -> List[Dict[str, Any]]:
        """
        Thu thập thông tin từ nhiều nguồn song song
        
        Args:
            query: Câu hỏi cần thu thập thông tin
            min_results: Số lượng kết quả tối thiểu cần thu thập
            
        Returns:
            list: Danh sách thông tin thu thập được
        """
        if min_results is None:
            min_results = self.config.get('min_sources', 2)
        
        # Thời điểm bắt đầu
        start_time = time.time()
        
        self.logger.info(f"Thu thập thông tin song song cho query: {query}")
        
        # Kết quả từ tất cả các nguồn
        result_queue = queue.Queue()
        
        # Xác định nguồn thông tin cần thu thập
        sources = self.config.get('sources', ['web', 'api'])
        
        # Tạo thread cho mỗi nguồn
        threads = []
        
        # Hàm thu thập từ Web
        def collect_from_web():
            try:
                web_results = self.web_scraper.collect(query, max_items=min_results)
                for result in web_results:
                    result_queue.put(result)
                self.logger.info(f"Web thread: Đã thu thập được {len(web_results)} kết quả")
            except Exception as e:
                self.logger.error(f"Lỗi khi thu thập từ Web: {e}", exc_info=True)
        
        # Hàm thu thập từ API
        def collect_from_api():
            try:
                api_results = self.api_connector.collect(query, max_items=min_results)
                for result in api_results:
                    result_queue.put(result)
                self.logger.info(f"API thread: Đã thu thập được {len(api_results)} kết quả")
            except Exception as e:
                self.logger.error(f"Lỗi khi thu thập từ API: {e}", exc_info=True)
        
        # Tạo và khởi động các thread
        if 'web' in sources:
            web_thread = threading.Thread(target=collect_from_web)
            web_thread.daemon = True
            threads.append(web_thread)
            web_thread.start()
        
        if 'api' in sources:
            api_thread = threading.Thread(target=collect_from_api)
            api_thread.daemon = True
            threads.append(api_thread)
            api_thread.start()
        
        # Đợi timeout hoặc đủ kết quả
        timeout = self.config.get('timeout', 30)
        end_time = start_time + timeout
        
        # Đợi các thread hoàn thành hoặc timeout
        for thread in threads:
            remaining_time = max(0, end_time - time.time())
            thread.join(timeout=remaining_time)
        
        # Lấy kết quả từ queue
        all_results = []
        while not result_queue.empty() and len(all_results) < min_results * 2:  # Giới hạn số lượng kết quả
            all_results.append(result_queue.get())
        
        # Tổng kết
        total_time = time.time() - start_time
        self.logger.info(f"Đã thu thập được tổng cộng {len(all_results)} thông tin mới trong {total_time:.2f} giây")
        
        return all_results