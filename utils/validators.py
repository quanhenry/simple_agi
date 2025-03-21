"""
Validators - Kiểm tra tính hợp lệ của dữ liệu
"""

import re
import logging
from typing import Dict, Any, List, Union, Optional
from urllib.parse import urlparse

logger = logging.getLogger("Validators")

def validate_entity(entity: Dict[str, Any]) -> bool:
    """
    Kiểm tra tính hợp lệ của thực thể
    
    Args:
        entity: Dictionary chứa thông tin thực thể
    
    Returns:
        bool: True nếu thực thể hợp lệ, False nếu không
    """
    if not isinstance(entity, dict):
        logger.warning("Thực thể không phải là dictionary")
        return False
    
    # Kiểm tra các trường bắt buộc
    if "name" not in entity or not entity["name"]:
        logger.warning("Thực thể thiếu trường name hoặc name rỗng")
        return False
    
    # Kiểm tra kiểu dữ liệu
    if not isinstance(entity["name"], str):
        logger.warning("Trường name không phải là chuỗi")
        return False
    
    # Kiểm tra các trường tùy chọn
    if "type" in entity and not isinstance(entity["type"], str):
        logger.warning("Trường type không phải là chuỗi")
        return False
    
    if "description" in entity and not isinstance(entity["description"], str):
        logger.warning("Trường description không phải là chuỗi")
        return False
    
    if "confidence" in entity:
        if not isinstance(entity["confidence"], (float, int)):
            logger.warning("Trường confidence không phải là số")
            return False
        
        if entity["confidence"] < 0 or entity["confidence"] > 1:
            logger.warning("Trường confidence phải nằm trong khoảng [0, 1]")
            return False
    
    if "properties" in entity and not isinstance(entity["properties"], dict):
        logger.warning("Trường properties không phải là dictionary")
        return False
    
    return True

def validate_relation(relation: Dict[str, Any]) -> bool:
    """
    Kiểm tra tính hợp lệ của mối quan hệ
    
    Args:
        relation: Dictionary chứa thông tin mối quan hệ
    
    Returns:
        bool: True nếu mối quan hệ hợp lệ, False nếu không
    """
    if not isinstance(relation, dict):
        logger.warning("Mối quan hệ không phải là dictionary")
        return False
    
    # Kiểm tra các trường bắt buộc
    required_fields = ["source", "target", "relation_type"]
    for field in required_fields:
        if field not in relation or not relation[field]:
            logger.warning(f"Mối quan hệ thiếu trường {field} hoặc {field} rỗng")
            return False
    
    # Kiểm tra kiểu dữ liệu
    if not all(isinstance(relation[field], str) for field in required_fields):
        logger.warning("Các trường source, target, relation_type phải là chuỗi")
        return False
    
    # Kiểm tra các trường tùy chọn
    if "description" in relation and not isinstance(relation["description"], str):
        logger.warning("Trường description không phải là chuỗi")
        return False
    
    if "confidence" in relation:
        if not isinstance(relation["confidence"], (float, int)):
            logger.warning("Trường confidence không phải là số")
            return False
        
        if relation["confidence"] < 0 or relation["confidence"] > 1:
            logger.warning("Trường confidence phải nằm trong khoảng [0, 1]")
            return False
    
    if "properties" in relation and not isinstance(relation["properties"], dict):
        logger.warning("Trường properties không phải là dictionary")
        return False
    
    return True

def is_valid_url(url: str) -> bool:
    """
    Kiểm tra URL có hợp lệ không
    
    Args:
        url: URL cần kiểm tra
    
    Returns:
        bool: True nếu URL hợp lệ, False nếu không
    """
    if not url or not isinstance(url, str):
        return False
    
    try:
        result = urlparse(url)
        # Kiểm tra có scheme và netloc không
        valid = all([result.scheme, result.netloc])
        # Kiểm tra scheme có phải là http hoặc https không
        valid = valid and result.scheme in ['http', 'https']
        return valid
    except:
        return False

def validate_information(info: Dict[str, Any]) -> bool:
    """
    Kiểm tra tính hợp lệ của thông tin
    
    Args:
        info: Dictionary chứa thông tin
    
    Returns:
        bool: True nếu thông tin hợp lệ, False nếu không
    """
    if not isinstance(info, dict):
        logger.warning("Thông tin không phải là dictionary")
        return False
    
    # Kiểm tra các trường quan trọng
    has_title = "title" in info and isinstance(info["title"], str) and info["title"]
    has_content = "content" in info and isinstance(info["content"], str) and info["content"]
    
    if not (has_title or has_content):
        logger.warning("Thông tin thiếu cả title và content")
        return False
    
    # Kiểm tra các trường tùy chọn
    if "source" in info and not isinstance(info["source"], str):
        logger.warning("Trường source không phải là chuỗi")
        return False
    
    if "url" in info and not is_valid_url(info["url"]):
        logger.warning(f"URL không hợp lệ: {info.get('url')}")
        return False
    
    if "confidence" in info:
        if not isinstance(info["confidence"], (float, int)):
            logger.warning("Trường confidence không phải là số")
            return False
        
        if info["confidence"] < 0 or info["confidence"] > 1:
            logger.warning("Trường confidence phải nằm trong khoảng [0, 1]")
            return False
    
    # Kiểm tra các trường entities và relations nếu có
    if "entities" in info:
        if not isinstance(info["entities"], list):
            logger.warning("Trường entities không phải là list")
            return False
        
        for entity in info["entities"]:
            if not validate_entity(entity):
                logger.warning(f"Entity không hợp lệ: {entity}")
                return False
    
    if "relations" in info:
        if not isinstance(info["relations"], list):
            logger.warning("Trường relations không phải là list")
            return False
        
        for relation in info["relations"]:
            if not validate_relation(relation):
                logger.warning(f"Relation không hợp lệ: {relation}")
                return False
    
    return True

def validate_query(query: str) -> bool:
    """
    Kiểm tra tính hợp lệ của câu truy vấn
    
    Args:
        query: Câu truy vấn cần kiểm tra
    
    Returns:
        bool: True nếu câu truy vấn hợp lệ, False nếu không
    """
    if not query or not isinstance(query, str):
        logger.warning("Câu truy vấn không hợp lệ")
        return False
    
    # Kiểm tra độ dài
    if len(query.strip()) < 2:
        logger.warning("Câu truy vấn quá ngắn")
        return False
    
    # Kiểm tra các ký tự không hợp lệ
    if re.search(r'[^\w\s.,;:!?()"\'-]', query):
        logger.warning("Câu truy vấn chứa ký tự không hợp lệ")
        # Không return False vì vẫn có thể xử lý được
    
    return True

def validate_api_response(response: Dict[str, Any]) -> bool:
    """
    Kiểm tra tính hợp lệ của phản hồi từ API
    
    Args:
        response: Dictionary chứa phản hồi từ API
    
    Returns:
        bool: True nếu phản hồi hợp lệ, False nếu không
    """
    if not isinstance(response, dict):
        logger.warning("Phản hồi API không phải là dictionary")
        return False
    
    # Kiểm tra status code hoặc error (nếu có)
    if "error" in response:
        logger.warning(f"Phản hồi API chứa lỗi: {response['error']}")
        return False
    
    # Kiểm tra dữ liệu trả về
    if "data" in response and not response["data"]:
        logger.warning("Phản hồi API không chứa dữ liệu")
        return False
    
    return True

def sanitize_input(text: str) -> str:
    """
    Làm sạch đầu vào từ người dùng, loại bỏ mã độc tiềm ẩn
    
    Args:
        text: Văn bản cần làm sạch
    
    Returns:
        str: Văn bản đã làm sạch
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Loại bỏ các ký tự điều khiển và không in được
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
    
    # Loại bỏ các thẻ HTML/XML có thể gây nguy hiểm
    text = re.sub(r'<[^>]*>', '', text)
    
    # Loại bỏ các ký tự đặc biệt nguy hiểm
    text = re.sub(r'[\\\'";`]', '', text)
    
    return text.strip()