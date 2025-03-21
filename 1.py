# # #!/usr/bin/env python
# # # -*- coding: utf-8 -*-

# # """
# # Script tạo cấu trúc thư mục và file trống cho dự án AGI Tự học
# # """

# # import os

# # def create_directory(path):
# #     """Tạo thư mục nếu chưa tồn tại"""
# #     if not os.path.exists(path):
# #         os.makedirs(path)
# #         print(f"Đã tạo thư mục: {path}")

# # def create_empty_file(path):
# #     """Tạo file trống"""
# #     open(path, 'w').close()
# #     print(f"Đã tạo file trống: {path}")

# # def main():
# #     # Thư mục gốc
# #     root_dir = "simple_agi"
    
# #     # Danh sách thư mục cần tạo
# #     directories = [
# #         root_dir,
# #         os.path.join(root_dir, "core"),
# #         os.path.join(root_dir, "collectors"),
# #         os.path.join(root_dir, "ui"),
# #         os.path.join(root_dir, "utils"),
# #         os.path.join(root_dir, "data", "knowledge_graph"),
# #         os.path.join(root_dir, "data", "cache")
# #     ]
    
# #     # Tạo các thư mục
# #     for directory in directories:
# #         create_directory(directory)
    
# #     # Danh sách file cần tạo
# #     files = [
# #         # File trong thư mục gốc
# #         os.path.join(root_dir, "main.py"),
# #         os.path.join(root_dir, "config.py"),
# #         os.path.join(root_dir, "requirements.txt"),
        
# #         # File trong core
# #         os.path.join(root_dir, "core", "__init__.py"),
# #         os.path.join(root_dir, "core", "engine.py"),
# #         os.path.join(root_dir, "core", "learner.py"),
# #         os.path.join(root_dir, "core", "reasoner.py"),
# #         os.path.join(root_dir, "core", "knowledge_base.py"),
        
# #         # File trong collectors
# #         os.path.join(root_dir, "collectors", "__init__.py"),
# #         os.path.join(root_dir, "collectors", "collector.py"),
# #         os.path.join(root_dir, "collectors", "web_scraper.py"),
# #         os.path.join(root_dir, "collectors", "api_connector.py"),
        
# #         # File trong ui
# #         os.path.join(root_dir, "ui", "__init__.py"),
# #         os.path.join(root_dir, "ui", "cli.py"),
# #         os.path.join(root_dir, "ui", "web.py"),
        
# #         # File trong utils
# #         os.path.join(root_dir, "utils", "__init__.py"),
# #         os.path.join(root_dir, "utils", "nlp_utils.py"),
# #         os.path.join(root_dir, "utils", "graph_utils.py"),
# #         os.path.join(root_dir, "utils", "validators.py")
# #     ]
    
# #     # Tạo các file trống
# #     for file in files:
# #         create_empty_file(file)
    
# #     print("\nĐã tạo xong cấu trúc dự án AGI!")

# # if __name__ == "__main__":
# #     main()
# import nltk
# import ssl

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

# nltk.download('punkt')
# nltk.download('stopwords')
# {
#   "directed": true,
#   "multigraph": false,
#   "graph": {},
#   "nodes": [
#     {
#       "name": "Toán cấp 1",
#       "type": "subject",
#       "description": "Môn Toán dành cho học sinh tiểu học bao gồm các kiến thức cơ bản về số học, hình học và giải toán có lời văn.",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "updated_at": "2025-03-21T10:00:00",
#       "id": "subject_math_primary"
#     },
#     {
#       "name": "Tiếng Việt cấp 1",
#       "type": "subject",
#       "description": "Môn Tiếng Việt dành cho học sinh tiểu học bao gồm các kiến thức về đọc, viết, ngữ pháp và văn học.",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "updated_at": "2025-03-21T10:00:00",
#       "id": "subject_vietnamese_primary"
#     },
#     {
#       "name": "Số tự nhiên",
#       "type": "concept",
#       "description": "Số tự nhiên là các số nguyên không âm bắt đầu từ 0 (hoặc 1, tùy theo định nghĩa) và tiếp tục với 1, 2, 3,...",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "updated_at": "2025-03-21T10:00:00",
#       "id": "concept_natural_numbers"
#     },
#     {
#       "name": "Phép cộng",
#       "type": "concept",
#       "description": "Phép cộng là phép toán cơ bản nhằm tìm tổng của hai hay nhiều số.",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "updated_at": "2025-03-21T10:00:00",
#       "id": "concept_addition"
#     },
#     {
#       "name": "Phép trừ",
#       "type": "concept",
#       "description": "Phép trừ là phép toán cơ bản nhằm tìm hiệu của hai số.",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "updated_at": "2025-03-21T10:00:00",
#       "id": "concept_subtraction"
#     },
#     {
#       "name": "Phép nhân",
#       "type": "concept",
#       "description": "Phép nhân là phép toán cơ bản nhằm tìm tích của hai hay nhiều số.",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "updated_at": "2025-03-21T10:00:00",
#       "id": "concept_multiplication"
#     },
#     {
#       "name": "Phép chia",
#       "type": "concept",
#       "description": "Phép chia là phép toán cơ bản nhằm tìm thương của hai số.",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "updated_at": "2025-03-21T10:00:00",
#       "id": "concept_division"
#     },
#     {
#       "name": "Hình học",
#       "type": "concept",
#       "description": "Hình học là nhánh của toán học nghiên cứu về các hình dạng, kích thước, vị trí tương đối của các đối tượng và tính chất của không gian.",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "updated_at": "2025-03-21T10:00:00",
#       "id": "concept_geometry"
#     },
#     {
#       "name": "Đo lường",
#       "type": "concept",
#       "description": "Đo lường là quá trình xác định độ lớn, số lượng hoặc mức độ của một đối tượng.",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "updated_at": "2025-03-21T10:00:00",
#       "id": "concept_measurement"
#     },
#     {
#       "name": "Chữ cái và âm",
#       "type": "concept",
#       "description": "Chữ cái là các ký hiệu trong bảng chữ cái, mỗi chữ cái tương ứng với một hoặc một số âm nhất định.",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "updated_at": "2025-03-21T10:00:00",
#       "id": "concept_letters_sounds"
#     },
#     {
#       "name": "Từ và câu",
#       "type": "concept",
#       "description": "Từ là đơn vị ngôn ngữ có nghĩa, câu là tập hợp các từ được sắp xếp theo quy tắc để diễn đạt một ý tưởng hoàn chỉnh.",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "updated_at": "2025-03-21T10:00:00",
#       "id": "concept_words_sentences"
#     },
#     {
#       "name": "Ngữ pháp",
#       "type": "concept",
#       "description": "Ngữ pháp là tập hợp các quy tắc về cách sử dụng từ và cấu trúc câu trong một ngôn ngữ.",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "updated_at": "2025-03-21T10:00:00",
#       "id": "concept_grammar"
#     },
#     {
#       "name": "Văn học",
#       "type": "concept",
#       "description": "Văn học là tập hợp các tác phẩm viết hoặc nói có giá trị nghệ thuật, bao gồm thơ, truyện, tiểu thuyết, v.v.",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "updated_at": "2025-03-21T10:00:00",
#       "id": "concept_literature"
#     },
#     {
#       "name": "Đọc hiểu",
#       "type": "concept",
#       "description": "Đọc hiểu là khả năng đọc và hiểu ý nghĩa của văn bản.",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "updated_at": "2025-03-21T10:00:00",
#       "id": "concept_reading_comprehension"
#     },
#     {
#       "name": "Viết",
#       "type": "concept",
#       "description": "Viết là khả năng diễn đạt ý tưởng, suy nghĩ bằng ngôn từ trong văn bản.",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "updated_at": "2025-03-21T10:00:00",
#       "id": "concept_writing"
#     },
#     {
#       "name": "Hình vuông",
#       "type": "concept",
#       "description": "Hình vuông là tứ giác có bốn cạnh bằng nhau và bốn góc đều là góc vuông (90 độ).",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "updated_at": "2025-03-21T10:00:00",
#       "id": "concept_square"
#     },
#     {
#       "name": "Hình tam giác",
#       "type": "concept",
#       "description": "Hình tam giác là đa giác có ba cạnh và ba góc.",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "updated_at": "2025-03-21T10:00:00",
#       "id": "concept_triangle"
#     },
#     {
#       "name": "Hình tròn",
#       "type": "concept",
#       "description": "Hình tròn là hình phẳng gồm tất cả các điểm có cùng khoảng cách từ một điểm cho trước gọi là tâm.",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "updated_at": "2025-03-21T10:00:00",
#       "id": "concept_circle"
#     },
#     {
#       "name": "Chu vi",
#       "type": "concept",
#       "description": "Chu vi là tổng độ dài các cạnh của một hình phẳng.",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "updated_at": "2025-03-21T10:00:00",
#       "id": "concept_perimeter"
#     },
#     {
#       "name": "Diện tích",
#       "type": "concept",
#       "description": "Diện tích là số đo kích thước mặt phẳng của một hình.",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "updated_at": "2025-03-21T10:00:00",
#       "id": "concept_area"
#     },
#     {
#       "name": "Thơ",
#       "type": "concept",
#       "description": "Thơ là một thể loại văn học sử dụng các yếu tố như vần điệu, nhịp điệu và ngôn ngữ để truyền tải ý nghĩa và cảm xúc.",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "updated_at": "2025-03-21T10:00:00",
#       "id": "concept_poetry"
#     },
#     {
#       "name": "Truyện",
#       "type": "concept",
#       "description": "Truyện là một thể loại văn học kể về các sự kiện, nhân vật và hành động, có thể là thực hoặc hư cấu.",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "updated_at": "2025-03-21T10:00:00",
#       "id": "concept_story"
#     },
#     {
#       "name": "Bảng cửu chương",
#       "type": "concept",
#       "description": "Bảng cửu chương là bảng tổng hợp kết quả của phép nhân các số từ 1 đến 10 (hoặc từ 1 đến 9), thường được học thuộc để tính toán nhanh.",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "updated_at": "2025-03-21T10:00:00",
#       "id": "concept_multiplication_table"
#     },
#     {
#       "name": "Hình chữ nhật",
#       "type": "concept",
#       "description": "Hình chữ nhật là tứ giác có bốn góc vuông và các cạnh đối song song và bằng nhau.",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "updated_at": "2025-03-21T10:00:00",
#       "id": "concept_rectangle"
#     },
#     {
#       "name": "Trí tuệ nhân tạo Wikipedia tiếng Việt",
#       "type": "concept",
#       "description": "Đóng mở mục lục Trí tuệ nhân tạo 164 ngôn ngữ Afrikaans Alemannisch አማርኛ العربية Aragonés Արեւմտահայերէն অসম য Asturianu Avañe'ẽ Azərbaycanca تۆرکجه Bahasa Indonesia Bahasa Melayu ব ল 閩南語 Bân-lâm-gú Б",
#       "source": "vi.wikipedia.org",
#       "confidence": 0.7,
#       "created_at": "2025-03-21T10:44:03.838515",
#       "updated_at": "2025-03-21T10:47:03.100722",
#       "id": "concept_eedcf93a76"
#     },
#     {
#       "name": "3+2",
#       "type": "context",
#       "created_at": "2025-03-21T10:44:03.838616",
#       "updated_at": "2025-03-21T10:44:03.838620",
#       "id": "context_91aeddc2d2"
#     },
#     {
#       "name": "Our Documentation Python.org",
#       "type": "concept",
#       "description": "Beginner Beginner s Guide Python FAQs Moderate Python Periodicals Python Books Advanced Python Packaging User Guide In-development Docs Guido s Essays General PEP Index Python Videos Developer s Guide",
#       "source": "www.python.org",
#       "confidence": 0.7,
#       "created_at": "2025-03-21T10:44:03.838675",
#       "updated_at": "2025-03-21T10:47:03.100961",
#       "id": "concept_cbcba7207e"
#     },
#     {
#       "name": "artificial-intelligence GitHub Topics GitHub",
#       "type": "concept",
#       "description": "Explore Topics Trending Collections Events GitHub Sponsors artificial-intelligence Star The branch of computer science dealing with the reproduction, or mimicking of human-level intelligence, self-awa",
#       "source": "github.com",
#       "confidence": 0.7,
#       "created_at": "2025-03-21T10:44:03.838719",
#       "updated_at": "2025-03-21T10:47:03.101052",
#       "id": "concept_f72dcd487a"
#     }
#   ],
#   "links": [
#     {
#       "relation_type": "contains",
#       "description": "Toán cấp 1 bao gồm kiến thức về số tự nhiên",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "source": "subject_math_primary",
#       "target": "concept_natural_numbers"
#     },
#     {
#       "relation_type": "contains",
#       "description": "Toán cấp 1 bao gồm kiến thức về phép cộng",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "source": "subject_math_primary",
#       "target": "concept_addition"
#     },
#     {
#       "relation_type": "contains",
#       "description": "Toán cấp 1 bao gồm kiến thức về phép trừ",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "source": "subject_math_primary",
#       "target": "concept_subtraction"
#     },
#     {
#       "relation_type": "contains",
#       "description": "Toán cấp 1 bao gồm kiến thức về phép nhân",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "source": "subject_math_primary",
#       "target": "concept_multiplication"
#     },
#     {
#       "relation_type": "contains",
#       "description": "Toán cấp 1 bao gồm kiến thức về phép chia",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "source": "subject_math_primary",
#       "target": "concept_division"
#     },
#     {
#       "relation_type": "contains",
#       "description": "Toán cấp 1 bao gồm kiến thức về hình học",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "source": "subject_math_primary",
#       "target": "concept_geometry"
#     },
#     {
#       "relation_type": "contains",
#       "description": "Toán cấp 1 bao gồm kiến thức về đo lường",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "source": "subject_math_primary",
#       "target": "concept_measurement"
#     },
#     {
#       "relation_type": "contains",
#       "description": "Tiếng Việt cấp 1 bao gồm kiến thức về chữ cái và âm",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "source": "subject_vietnamese_primary",
#       "target": "concept_letters_sounds"
#     },
#     {
#       "relation_type": "contains",
#       "description": "Tiếng Việt cấp 1 bao gồm kiến thức về từ và câu",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "source": "subject_vietnamese_primary",
#       "target": "concept_words_sentences"
#     },
#     {
#       "relation_type": "contains",
#       "description": "Tiếng Việt cấp 1 bao gồm kiến thức về ngữ pháp",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "source": "subject_vietnamese_primary",
#       "target": "concept_grammar"
#     },
#     {
#       "relation_type": "contains",
#       "description": "Tiếng Việt cấp 1 bao gồm kiến thức về văn học",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "source": "subject_vietnamese_primary",
#       "target": "concept_literature"
#     },
#     {
#       "relation_type": "contains",
#       "description": "Tiếng Việt cấp 1 bao gồm kỹ năng đọc hiểu",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "source": "subject_vietnamese_primary",
#       "target": "concept_reading_comprehension"
#     },
#     {
#       "relation_type": "contains",
#       "description": "Tiếng Việt cấp 1 bao gồm kỹ năng viết",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "source": "subject_vietnamese_primary",
#       "target": "concept_writing"
#     },
#     {
#       "relation_type": "relates_to",
#       "description": "Phép cộng và phép trừ là hai phép toán ngược nhau",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "source": "concept_addition",
#       "target": "concept_subtraction"
#     },
#     {
#       "relation_type": "relates_to",
#       "description": "Phép nhân và phép chia là hai phép toán ngược nhau",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "source": "concept_multiplication",
#       "target": "concept_division"
#     },
#     {
#       "relation_type": "relates_to",
#       "description": "Phép nhân có thể được coi là phép cộng lặp lại nhiều lần",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "source": "concept_multiplication",
#       "target": "concept_addition"
#     },
#     {
#       "relation_type": "contains",
#       "description": "Hình học bao gồm kiến thức về hình vuông",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "source": "concept_geometry",
#       "target": "concept_square"
#     },
#     {
#       "relation_type": "contains",
#       "description": "Hình học bao gồm kiến thức về hình tam giác",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "source": "concept_geometry",
#       "target": "concept_triangle"
#     },
#     {
#       "relation_type": "contains",
#       "description": "Hình học bao gồm kiến thức về hình tròn",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "source": "concept_geometry",
#       "target": "concept_circle"
#     },
#     {
#       "relation_type": "contains",
#       "description": "Hình học bao gồm kiến thức về hình chữ nhật",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "source": "concept_geometry",
#       "target": "concept_rectangle"
#     },
#     {
#       "relation_type": "relates_to",
#       "description": "Hình học liên quan đến khái niệm chu vi",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "source": "concept_geometry",
#       "target": "concept_perimeter"
#     },
#     {
#       "relation_type": "relates_to",
#       "description": "Hình học liên quan đến khái niệm diện tích",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "source": "concept_geometry",
#       "target": "concept_area"
#     },
#     {
#       "relation_type": "contains",
#       "description": "Văn học bao gồm thể loại thơ",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "source": "concept_literature",
#       "target": "concept_poetry"
#     },
#     {
#       "relation_type": "contains",
#       "description": "Văn học bao gồm thể loại truyện",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "source": "concept_literature",
#       "target": "concept_story"
#     },
#     {
#       "relation_type": "relates_to",
#       "description": "Đọc hiểu và viết là hai kỹ năng bổ trợ cho nhau",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "source": "concept_reading_comprehension",
#       "target": "concept_writing"
#     },
#     {
#       "relation_type": "relates_to",
#       "description": "Bảng cửu chương là công cụ để ghi nhớ kết quả của phép nhân",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "source": "concept_multiplication_table",
#       "target": "concept_multiplication"
#     },
#     {
#       "relation_type": "generalizes",
#       "description": "Hình vuông là trường hợp đặc biệt của hình chữ nhật khi cả bốn cạnh bằng nhau",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "source": "concept_rectangle",
#       "target": "concept_square"
#     },
#     {
#       "relation_type": "has_property",
#       "description": "Hình chữ nhật có thuộc tính chu vi bằng tổng độ dài bốn cạnh",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "source": "concept_rectangle",
#       "target": "concept_perimeter"
#     },
#     {
#       "relation_type": "has_property",
#       "description": "Hình chữ nhật có thuộc tính diện tích bằng tích chiều dài và chiều rộng",
#       "origin": "initialization",
#       "confidence": 1.0,
#       "created_at": "2025-03-21T10:00:00",
#       "source": "concept_rectangle",
#       "target": "concept_area"
#     },
#     {
#       "confidence": 1.0,
#       "relation_type": "related_to",
#       "created_at": "2025-03-21T10:47:03.100811",
#       "source": "context_91aeddc2d2",
#       "target": "concept_eedcf93a76"
#     },
#     {
#       "confidence": 1.0,
#       "relation_type": "related_to",
#       "created_at": "2025-03-21T10:47:03.100994",
#       "source": "context_91aeddc2d2",
#       "target": "concept_cbcba7207e"
#     },
#     {
#       "confidence": 1.0,
#       "relation_type": "related_to",
#       "created_at": "2025-03-21T10:47:03.101079",
#       "source": "context_91aeddc2d2",
#       "target": "concept_f72dcd487a"
#     }
#   ]
# }