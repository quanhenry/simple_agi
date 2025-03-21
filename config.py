"""
Cấu hình dự án SimpleAGI cho dạy Toán lớp 1
"""

import os
import logging

# Thiết lập cấu hình logging
LOG_LEVEL = "INFO"  # Thêm cấu hình LOG_LEVEL

logging_config = {
    'level': logging.INFO,
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'datefmt': '%Y-%m-%d %H:%M:%S'
}

# Thiết lập đường dẫn dữ liệu
DATA_DIR = "data"
KNOWLEDGE_GRAPH_DIR = os.path.join(DATA_DIR, "knowledge_graph")
CACHE_DIR = os.path.join(DATA_DIR, "cache")

# Thiết lập Knowledge Base
KB_CONFIG = {
    'graph_file': os.path.join(KNOWLEDGE_GRAPH_DIR, "knowledge_graph.json"),
    'initial_knowledge': os.path.join(KNOWLEDGE_GRAPH_DIR, "initial_knowledge.json"),
    'max_results': 10,
    'similarity_threshold': 0.5
}

# Thiết lập Web Scraper
USER_AGENT = "SimpleAGI-Math/1.0 (educational purposes)"
TRUSTED_DOMAINS = ["khanacademy.org", "mathisfun.com", "education.com", "mathplayground.com", "vi.wikipedia.org"]
REQUEST_TIMEOUT = 10  # seconds

WEB_SCRAPER_CONFIG = {
    'max_pages': 3,
    'timeout': REQUEST_TIMEOUT,
    'user_agent': USER_AGENT,
    'search_engine': 'mock',  # 'mock' hoặc 'google'
    'trusted_domains': TRUSTED_DOMAINS
}

# API Keys
API_KEYS = {
    'openai': os.environ.get('OPENAI_API_KEY', ''),
    'google': os.environ.get('GOOGLE_API_KEY', 'AIzaSyDvYUe2IgWpsjrOZeN699CgzqeVMcDof2U'),
    'anthropic': os.environ.get('ANTHROPIC_API_KEY', '')
}

# API mặc định
DEFAULT_API_MODEL = "google-gemini"

# Thiết lập Learner
LEARNER_CONFIG = {
    'max_facts_per_session': 100,
    'similarity_threshold': 0.8
}

# Độ tin cậy tối thiểu
MIN_CONFIDENCE = 0.6

# Thiết lập UI
UI_CONFIG = {
    'web': {
        'host': '0.0.0.0',
        'port': 8000,
        'debug': False
    }
}

# Thiết lập Information Collector
INFO_COLLECTOR_CONFIG = {
    'sources': ['web', 'api'], 
    'min_sources': 2,
    'timeout': 30
}

# Cấu trúc tri thức toán học lớp 1
MATH_CATEGORIES = {
    "counting": ["count_objects", "number_sequence", "before_after"],
    "operations": ["addition", "subtraction", "simple_word_problems"],
    "comparison": ["greater_than", "less_than", "equal_to"],
    "place_value": ["ones", "tens", "hundreds"],
    "measurement": ["length", "weight", "time", "money"],
    "geometry": ["shapes", "patterns"]
}

# Định nghĩa các mối quan hệ đặc thù cho toán học
MATH_RELATIONS = [
    "prerequisite_for",  # Kiến thức A là điều kiện tiên quyết cho B
    "example_of",        # A là ví dụ của B
    "solution_for",      # A là giải pháp cho B
    "visualization_of",  # A là hình ảnh minh họa của B
    "formula_for"        # A là công thức cho B
]