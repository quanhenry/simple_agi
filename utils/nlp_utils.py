"""
NLP Utils - Công cụ xử lý ngôn ngữ tự nhiên
"""

import re
import logging
from typing import List, Dict, Set, Tuple

# Thư viện tùy chọn, sẽ được import khi cần
spacy_available = False
nltk_available = False

try:
    import nltk
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    nltk_available = True
    # Tải dữ liệu cần thiết
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)
except ImportError:
    pass

try:
    import spacy
    spacy_available = True
except ImportError:
    pass

logger = logging.getLogger("NLPUtils")

# Danh sách stopwords tiếng Việt đơn giản
VIETNAMESE_STOPWORDS = {
    "là", "và", "của", "có", "trong", "cho", "với", "được", "không",
    "những", "các", "để", "một", "về", "từ", "khi", "đến", "tôi", "bạn",
    "chúng", "họ", "ở", "như", "đã", "sẽ", "cũng", "nhưng", "mà", "hay",
    "vì", "nếu", "này", "đó", "thì", "tại", "còn", "bởi", "theo", "rằng",
    "lại", "vậy", "nên", "dù", "tuy", "ai", "bằng", "vào", "ra", "nhiều",
    "ít", "rất", "đang", "nào", "làm", "biết", "phải", "hơn", "được", "trên",
    "dưới", "chỉ", "rồi", "sau", "trước", "đầu", "cuối", "thôi", "lúc"
}

# Từ đồng nghĩa đơn giản cho tiếng Việt
VIETNAMESE_SYNONYMS = {
    "lớn": ["to", "khổng lồ", "rộng", "đồ sộ"],
    "nhỏ": ["bé", "nhỏ bé", "li ti", "tí hon"],
    "tốt": ["hay", "tuyệt", "xuất sắc", "giỏi", "được"],
    "xấu": ["dở", "kém", "tệ", "không tốt"],
    "nhanh": ["mau", "lẹ", "vội", "gấp"],
    "chậm": ["từ từ", "thủng thẳng", "chầm chậm"],
    "đẹp": ["xinh", "đáng yêu", "ưa nhìn"],
    "học": ["nghiên cứu", "tìm hiểu", "đọc", "tìm tòi"]
}

def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
    """
    Trích xuất từ khóa quan trọng từ văn bản
    
    Args:
        text: Văn bản cần trích xuất
        max_keywords: Số lượng từ khóa tối đa trả về
    
    Returns:
        list: Danh sách từ khóa
    """
    if not text:
        return []
    
    # Chuyển text về chữ thường
    text = text.lower()
    
    # Sử dụng SpaCy nếu có sẵn
    if spacy_available:
        try:
            # Tải mô hình
            try:
                nlp = spacy.load("vi_core_news_sm")
            except:
                nlp = spacy.load("en_core_web_sm")
            
            # Xử lý văn bản
            doc = nlp(text)
            
            # Lấy các từ quan trọng (không phải stopword và là danh từ, động từ hoặc tính từ)
            keywords = []
            for token in doc:
                if (not token.is_stop and token.pos_ in ["NOUN", "VERB", "ADJ"] and 
                    len(token.text) > 1 and token.text not in VIETNAMESE_STOPWORDS):
                    keywords.append(token.text)
            
            # Lấy các cụm danh từ
            chunks = [chunk.text for chunk in doc.noun_chunks if len(chunk.text) > 3]
            
            # Kết hợp các từ khóa và cụm, loại bỏ trùng lặp
            all_keywords = list(set(keywords + chunks))
            
            # Trả về số lượng từ khóa tối đa
            return all_keywords[:max_keywords]
            
        except Exception as e:
            logger.warning(f"Lỗi khi sử dụng SpaCy: {e}, chuyển sang phương pháp đơn giản")
    
    # Sử dụng NLTK nếu có sẵn
    if nltk_available:
        try:
            # Tokenize
            words = word_tokenize(text)
            
            # Lọc stopwords
            stop_words = set(stopwords.words('english')).union(VIETNAMESE_STOPWORDS)
            keywords = [word for word in words if word.isalnum() and word not in stop_words and len(word) > 1]
            
            # Lấy các từ xuất hiện nhiều nhất
            word_freq = {}
            for word in keywords:
                word_freq[word] = word_freq.get(word, 0) + 1
            
            # Sắp xếp theo tần suất
            sorted_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
            
            return [word for word, freq in sorted_keywords[:max_keywords]]
            
        except Exception as e:
            logger.warning(f"Lỗi khi sử dụng NLTK: {e}, chuyển sang phương pháp đơn giản")
    
    # Phương pháp đơn giản nếu không có thư viện NLP
    # Tokenize đơn giản bằng dấu cách và dấu câu
    words = re.findall(r'\b\w+\b', text)
    
    # Lọc stopwords
    keywords = [word for word in words if word not in VIETNAMESE_STOPWORDS and len(word) > 1]
    
    # Đếm tần suất
    word_freq = {}
    for word in keywords:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    # Sắp xếp theo tần suất
    sorted_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    
    return [word for word, freq in sorted_keywords[:max_keywords]]

def clean_text(text: str) -> str:
    """
    Làm sạch văn bản, loại bỏ ký tự đặc biệt và khoảng trắng thừa
    
    Args:
        text: Văn bản cần làm sạch
    
    Returns:
        str: Văn bản đã làm sạch
    """
    if not text:
        return ""
    
    # Loại bỏ các ký tự đặc biệt nhưng giữ lại dấu câu cơ bản
    text = re.sub(r'[^\w\s.,;:!?()"\'-]', ' ', text)
    
    # Thay thế nhiều khoảng trắng thành một khoảng trắng
    text = re.sub(r'\s+', ' ', text)
    
    # Loại bỏ khoảng trắng ở đầu và cuối
    text = text.strip()
    
    return text

def text_similarity(text1: str, text2: str) -> float:
    """
    Tính độ tương đồng giữa hai văn bản
    
    Args:
        text1: Văn bản thứ nhất
        text2: Văn bản thứ hai
    
    Returns:
        float: Độ tương đồng từ 0.0 đến 1.0
    """
    if not text1 or not text2:
        return 0.0
    
    # Chuyển về chữ thường
    text1 = text1.lower()
    text2 = text2.lower()
    
    # Trích xuất từ khóa
    keywords1 = set(extract_keywords(text1, max_keywords=20))
    keywords2 = set(extract_keywords(text2, max_keywords=20))
    
    # Tính độ tương đồng Jaccard
    if not keywords1 or not keywords2:
        return 0.0
    
    intersection = len(keywords1.intersection(keywords2))
    union = len(keywords1.union(keywords2))
    
    return intersection / union if union > 0 else 0.0

def find_entities(text: str) -> List[Dict]:
    """
    Tìm các thực thể trong văn bản
    
    Args:
        text: Văn bản cần tìm thực thể
    
    Returns:
        list: Danh sách các thực thể tìm được
    """
    entities = []
    
    # Sử dụng SpaCy nếu có sẵn
    if spacy_available:
        try:
            # Tải mô hình
            try:
                nlp = spacy.load("vi_core_news_sm")
            except:
                nlp = spacy.load("en_core_web_sm")
            
            # Xử lý văn bản
            doc = nlp(text)
            
            # Lấy các thực thể được nhận dạng
            for ent in doc.ents:
                entity = {
                    "name": ent.text,
                    "type": ent.label_,
                    "start": ent.start_char,
                    "end": ent.end_char
                }
                entities.append(entity)
            
            return entities
            
        except Exception as e:
            logger.warning(f"Lỗi khi tìm thực thể với SpaCy: {e}")
    
    # Phương pháp đơn giản nếu không có SpaCy
    # Giả định các cụm danh từ là thực thể tiềm năng
    # (Phương pháp này không chính xác nhưng có thể dùng tạm)
    
    # Tìm các từ viết hoa (tiếng Anh) và các từ dài (tiếng Việt)
    capitalized_words = re.findall(r'\b[A-Z][a-z]+\b', text)
    long_words = [word for word in re.findall(r'\b\w{4,}\b', text) if word not in VIETNAMESE_STOPWORDS]
    
    # Tạo các thực thể
    for word in set(capitalized_words + long_words):
        entity = {
            "name": word,
            "type": "MISC",  # Loại chung
            "start": text.find(word),
            "end": text.find(word) + len(word)
        }
        entities.append(entity)
    
    return entities

def expand_query(query: str) -> str:
    """
    Mở rộng câu truy vấn với các từ đồng nghĩa để tăng khả năng tìm kiếm
    
    Args:
        query: Câu truy vấn gốc
    
    Returns:
        str: Câu truy vấn đã mở rộng
    """
    if not query:
        return query
    
    # Trích xuất từ khóa
    keywords = extract_keywords(query)
    
    # Tìm từ đồng nghĩa cho mỗi từ khóa
    expanded_keywords = set(keywords)
    
    for keyword in keywords:
        if keyword in VIETNAMESE_SYNONYMS:
            expanded_keywords.update(VIETNAMESE_SYNONYMS[keyword])
    
    # Kết hợp câu truy vấn gốc và các từ khóa mở rộng
    expanded_query = query
    for keyword in expanded_keywords:
        if keyword not in query:
            expanded_query += f" {keyword}"
    
    return expanded_query