"""
Cấu hình dự án SimpleAGI
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
WEB_SCRAPER_CONFIG = {
    'max_pages': 3,
    'timeout': 10,
    'user_agent': 'SimpleAGI/0.1 (educational purposes)',
    'search_engine': 'mock'  # 'mock' hoặc 'google'
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