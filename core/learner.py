"""
Learner - Module học tập, tích hợp kiến thức mới vào Knowledge Base
"""

import logging
import hashlib
from datetime import datetime

import config
from utils.graph_utils import create_node_id
from utils.validators import validate_entity, validate_relation

class Learner:
    """
    Module học tập từ thông tin mới và tích hợp vào Knowledge Base
    """
    
    def __init__(self, knowledge_base):
        """
        Khởi tạo learner module
        
        Args:
            knowledge_base (KnowledgeBase): Cơ sở kiến thức để lưu trữ
        """
        self.kb = knowledge_base
        self.logger = logging.getLogger("Learner")
        
    def learn(self, information, context=None):
        """
        Học từ thông tin mới và tích hợp vào Knowledge Base
        
        Args:
            information: Thông tin mới, có thể là list hoặc dictionary
            context: Ngữ cảnh liên quan (như câu hỏi ban đầu)
        
        Returns:
            bool: True nếu việc học thành công, False nếu thất bại
        """
        if not information:
            self.logger.warning("Không có thông tin để học")
            return False
            
        self.logger.info(f"Bắt đầu quá trình học với {len(information) if isinstance(information, list) else 1} thông tin mới")
        
        try:
            # Xử lý danh sách thông tin
            if isinstance(information, list):
                for info in information:
                    self._process_info(info, context)
            else:
                # Xử lý một thông tin đơn lẻ
                self._process_info(information, context)
                
            # Lưu knowledge base
            self.kb.save()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Lỗi trong quá trình học: {e}", exc_info=True)
            return False
    
    def _process_info(self, info, context=None):
        """
        Xử lý và tích hợp một thông tin mới vào Knowledge Base
        
        Args:
            info: Thông tin đơn lẻ (dict)
            context: Ngữ cảnh liên quan
        """
        # Kiểm tra tính hợp lệ của thông tin
        if not self._validate_info(info):
            self.logger.warning(f"Thông tin không hợp lệ, bỏ qua: {info}")
            return
            
        # Kiểm tra tính mâu thuẫn với kiến thức hiện tại
        contradiction = self._check_contradiction(info)
        if contradiction:
            self._resolve_contradiction(info, contradiction)
            return
            
        # Trích xuất thực thể và mối quan hệ
        entities, relations = self._extract_entities_and_relations(info)
        
        # Thêm các thực thể vào KB
        entity_nodes = []
        for entity in entities:
            if not validate_entity(entity):
                self.logger.warning(f"Thực thể không hợp lệ, bỏ qua: {entity}")
                continue
                
            node_id = create_node_id(entity["name"], entity.get("type", "entity"))
            existing_node = self.kb.get_node(node_id)
            
            if existing_node:
                # Cập nhật node nếu đã tồn tại
                self._update_existing_node(node_id, entity)
                entity_nodes.append(node_id)
            else:
                # Tạo node mới nếu chưa tồn tại
                attributes = {
                    "name": entity["name"],
                    "type": entity.get("type", "entity"),
                    "description": entity.get("description", ""),
                    "source": info.get("source", "unknown"),
                    "confidence": entity.get("confidence", info.get("confidence", config.MIN_CONFIDENCE))
                }
                
                if "properties" in entity:
                    for prop_name, prop_value in entity["properties"].items():
                        attributes[f"prop_{prop_name}"] = prop_value
                
                self.kb.add_node(node_id, attributes)
                entity_nodes.append(node_id)
                self.logger.debug(f"Đã thêm thực thể mới: {entity['name']} ({node_id})")
        
        # Thêm các mối quan hệ vào KB
        for relation in relations:
            if not validate_relation(relation):
                self.logger.warning(f"Quan hệ không hợp lệ, bỏ qua: {relation}")
                continue
                
            source_id = create_node_id(relation["source"], relation.get("source_type", "entity"))
            target_id = create_node_id(relation["target"], relation.get("target_type", "entity"))
            relation_type = relation["relation_type"]
            
            # Chỉ thêm quan hệ nếu cả source và target đều tồn tại trong KB
            if source_id in self.kb.graph.nodes and target_id in self.kb.graph.nodes:
                relation_attrs = {
                    "description": relation.get("description", ""),
                    "source": info.get("source", "unknown"),
                    "confidence": relation.get("confidence", info.get("confidence", config.MIN_CONFIDENCE))
                }
                
                if "properties" in relation:
                    for prop_name, prop_value in relation["properties"].items():
                        relation_attrs[f"prop_{prop_name}"] = prop_value
                
                self.kb.add_edge(source_id, target_id, relation_type, relation_attrs)
                self.logger.debug(f"Đã thêm quan hệ: {relation['source']} -> {relation['target']} ({relation_type})")
            else:
                self.logger.warning(f"Không thể thêm quan hệ vì thiếu node: {source_id} hoặc {target_id}")
                
        # Thêm liên kết với ngữ cảnh nếu có
        if context and entity_nodes:
            context_id = create_node_id(context, "context")
            
            # Tạo node context nếu chưa tồn tại
            if context_id not in self.kb.graph.nodes:
                context_attrs = {
                    "name": context,
                    "type": "context",
                    "created_at": datetime.now().isoformat()
                }
                self.kb.add_node(context_id, context_attrs)
                self.logger.debug(f"Đã tạo node ngữ cảnh: {context} ({context_id})")
                
            # Liên kết context với các entity
            for entity_id in entity_nodes:
                self.kb.add_edge(context_id, entity_id, "related_to", {"confidence": 1.0})
                self.logger.debug(f"Đã liên kết ngữ cảnh với entity: {context_id} -> {entity_id}")
    
    def _validate_info(self, info):
        """
        Kiểm tra tính hợp lệ của thông tin
        
        Args:
            info (dict): Thông tin cần kiểm tra
            
        Returns:
            bool: True nếu thông tin hợp lệ, False nếu không
        """
        # Kiểm tra cấu trúc cơ bản
        if not isinstance(info, dict):
            self.logger.warning("Thông tin không phải là dictionary")
            return False
            
        # Kiểm tra độ tin cậy
        if "confidence" in info and info["confidence"] < config.MIN_CONFIDENCE:
            self.logger.warning(f"Độ tin cậy quá thấp: {info.get('confidence')}")
            return False
            
        # Kiểm tra có thông tin hữu ích không
        has_entities = "entities" in info and info["entities"]
        has_relations = "relations" in info and info["relations"]
        has_content = "content" in info and info["content"]
        
        if not (has_entities or has_relations or has_content):
            self.logger.warning("Thông tin không chứa entities, relations hoặc content")
            return False
            
        return True
    
    def _check_contradiction(self, info):
        """
        Kiểm tra tính mâu thuẫn với kiến thức hiện tại
        
        Args:
            info (dict): Thông tin cần kiểm tra
            
        Returns:
            dict/None: Thông tin về mâu thuẫn nếu có, None nếu không
        """
        # TODO: Thực hiện kiểm tra mâu thuẫn
        # Phiên bản đơn giản hiện tại không thực hiện kiểm tra mâu thuẫn
        return None
    
    def _resolve_contradiction(self, info, contradiction):
        """
        Giải quyết mâu thuẫn giữa thông tin mới và kiến thức hiện tại
        
        Args:
            info (dict): Thông tin mới
            contradiction (dict): Thông tin về mâu thuẫn
        """
        # TODO: Thực hiện giải quyết mâu thuẫn
        # Phiên bản đơn giản hiện tại không thực hiện giải quyết mâu thuẫn
        self.logger.info(f"Phát hiện mâu thuẫn: {contradiction}")
        
        # Giải quyết đơn giản: lấy thông tin có độ tin cậy cao hơn
        if info.get("confidence", 0) > contradiction.get("confidence", 0):
            self.logger.info("Sử dụng thông tin mới (độ tin cậy cao hơn)")
            return True
        else:
            self.logger.info("Giữ thông tin cũ (độ tin cậy cao hơn)")
            return False
    
    def _extract_entities_and_relations(self, info):
        """
        Trích xuất các thực thể và mối quan hệ từ thông tin
        
        Args:
            info (dict): Thông tin cần trích xuất
            
        Returns:
            tuple: (entities, relations)
        """
        entities = []
        relations = []
        
        # Thực thể đã được cung cấp
        if "entities" in info and info["entities"]:
            entities = info["entities"]
            
        # Quan hệ đã được cung cấp
        if "relations" in info and info["relations"]:
            relations = info["relations"]
            
        # Trong trường hợp chỉ có dữ liệu thô, cần trích xuất từ nội dung
        if not entities and not relations and "content" in info:
            # Tạo một thực thể từ tiêu đề nếu có
            if "title" in info:
                entities.append({
                    "name": info["title"],
                    "type": "concept",
                    "description": info.get("content", "")[:200]  # Trích 200 ký tự đầu làm mô tả
                })
                
            # TODO: Thực hiện NLP để trích xuất thêm thực thể và quan hệ từ nội dung
        
        return entities, relations
    
    def _update_existing_node(self, node_id, entity):
        """
        Cập nhật node đã tồn tại với thông tin mới
        
        Args:
            node_id (str): ID của node cần cập nhật
            entity (dict): Thông tin mới về thực thể
        """
        # Lấy thông tin hiện tại của node
        _, current_attrs = self.kb.get_node(node_id)
        
        # Cập nhật các thuộc tính
        new_attrs = {
            "updated_at": datetime.now().isoformat()
        }
        
        # Cập nhật mô tả nếu cần
        if "description" in entity and entity["description"] and (
            "description" not in current_attrs or 
            len(entity["description"]) > len(current_attrs.get("description", ""))
        ):
            new_attrs["description"] = entity["description"]
            
        # Cập nhật các thuộc tính bổ sung
        if "properties" in entity:
            for prop_name, prop_value in entity["properties"].items():
                new_attrs[f"prop_{prop_name}"] = prop_value
                
        # Cập nhật độ tin cậy
        if ("confidence" in entity and 
            entity["confidence"] > current_attrs.get("confidence", 0)):
            new_attrs["confidence"] = entity["confidence"]
            
        # Áp dụng các cập nhật
        if new_attrs:
            self.kb.add_node(node_id, new_attrs)
            self.logger.debug(f"Đã cập nhật node: {node_id} với {len(new_attrs)} thuộc tính")