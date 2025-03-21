"""
Command Line Interface - Giao diện dòng lệnh cho hệ thống AGI
"""

import os
import logging
import time
from typing import Dict, Any, List

class AGICLI:
    """
    Giao diện dòng lệnh cho hệ thống AGI
    """
    
    def __init__(self, engine, verbose=False):
        """
        Khởi tạo giao diện dòng lệnh
        
        Args:
            engine: Engine AGI chính
            verbose: Chế độ hiển thị thông tin chi tiết
        """
        self.engine = engine
        self.verbose = verbose
        self.logger = logging.getLogger("AGICLI")
        self.history = []  # Lịch sử tương tác
        
        self.commands = {
            "help": self._show_help,
            "exit": self._exit,
            "quit": self._exit,
            "history": self._show_history,
            "clear": self._clear_screen,
            "stats": self._show_stats
        }
        
        self.logger.info("AGICLI đã được khởi tạo")
    
    def start(self):
        """Bắt đầu giao diện dòng lệnh tương tác"""
        self._print_welcome()
        
        running = True
        while running:
            try:
                user_input = input("\n> ")
                
                # Xử lý lệnh đặc biệt
                if user_input.startswith("/"):
                    command = user_input[1:].strip().lower()
                    self._process_command(command)
                    continue
                
                # Kiểm tra lệnh thoát
                if user_input.lower() in ["exit", "quit", "thoát"]:
                    running = False
                    print("Cảm ơn bạn đã sử dụng. Tạm biệt!")
                    continue
                
                # Xử lý câu hỏi
                if not user_input.strip():
                    continue
                    
                self._process_input(user_input)
                
            except KeyboardInterrupt:
                print("\nThoát ứng dụng...")
                running = False
                break
            except Exception as e:
                self.logger.error(f"Lỗi xử lý: {e}", exc_info=True)
                print(f"Đã xảy ra lỗi: {e}")
    
    def _process_input(self, user_input):
        """
        Xử lý câu hỏi của người dùng
        
        Args:
            user_input: Câu hỏi của người dùng
        """
        print("\nĐang xử lý yêu cầu của bạn...")
        start_time = time.time()
        
        # Gửi yêu cầu đến engine
        response = self.engine.process_request(user_input)
        
        # Thêm vào lịch sử
        self.history.append({
            "input": user_input,
            "response": response,
            "timestamp": time.time()
        })
        
        # Hiển thị kết quả
        self._display_response(response, time.time() - start_time)
    
    def _display_response(self, response: Dict[str, Any], process_time: float):
        """
        Hiển thị kết quả từ engine
        
        Args:
            response: Kết quả từ engine
            process_time: Thời gian xử lý (giây)
        """
        print("\n" + "=" * 60)
        print("Trả lời:")
        print(response["answer"])
        
        # Hiển thị thông tin chi tiết nếu ở chế độ verbose
        if self.verbose:
            print("\nThông tin thêm:")
            print(f"- Độ tin cậy: {response.get('confidence', 0):.2f}")
            if response.get("sources"):
                print(f"- Nguồn: {', '.join(response.get('sources', []))}")
            print(f"- Thời gian xử lý: {process_time:.2f} giây")
            if "question_type" in response:
                print(f"- Loại câu hỏi: {response['question_type']}")
        
        print("=" * 60)
    
    def _process_command(self, command: str):
        """
        Xử lý lệnh đặc biệt
        
        Args:
            command: Lệnh cần xử lý
        """
        parts = command.split()
        cmd = parts[0]
        args = parts[1:] if len(parts) > 1 else []
        
        if cmd in self.commands:
            self.commands[cmd](args)
        else:
            print(f"Lệnh không được hỗ trợ: {cmd}")
            print("Gõ /help để xem danh sách lệnh")
    
    def _show_help(self, args=[]):
        """Hiển thị trợ giúp"""
        print("\n=== Trợ giúp ===")
        print("Các lệnh có sẵn:")
        print("  /help       - Hiển thị trợ giúp này")
        print("  /exit, /quit - Thoát ứng dụng")
        print("  /history    - Hiển thị lịch sử tương tác")
        print("  /clear      - Xóa màn hình")
        print("  /stats      - Hiển thị thống kê về hệ thống")
        print("\nCách sử dụng:")
        print("- Nhập câu hỏi hoặc yêu cầu trực tiếp để tương tác với AGI")
        print("- Sử dụng lệnh đặc biệt bắt đầu bằng dấu /")
    
    def _exit(self, args=[]):
        """Thoát ứng dụng"""
        print("Cảm ơn bạn đã sử dụng. Tạm biệt!")
        exit(0)
    
    def _show_history(self, args=[]):
        """Hiển thị lịch sử tương tác"""
        if not self.history:
            print("Chưa có lịch sử tương tác")
            return
            
        print("\n=== Lịch sử tương tác ===")
        limit = 5  # Mặc định hiển thị 5 mục gần nhất
        
        # Kiểm tra có tham số số lượng không
        if args and args[0].isdigit():
            limit = int(args[0])
        
        # Lấy các mục gần nhất
        recent = self.history[-limit:] if len(self.history) > limit else self.history
        
        for i, item in enumerate(recent, 1):
            timestamp = time.strftime("%H:%M:%S", time.localtime(item["timestamp"]))
            print(f"\n{i}. [{timestamp}]")
            print(f"Q: {item['input']}")
            print(f"A: {item['response']['answer'][:100]}..." if len(item['response']['answer']) > 100 else f"A: {item['response']['answer']}")
    
    def _clear_screen(self, args=[]):
        """Xóa màn hình"""
        os.system('cls' if os.name == 'nt' else 'clear')
        self._print_welcome()
    
    def _show_stats(self, args=[]):
        """Hiển thị thống kê về hệ thống"""
        kb_stats = self.engine.get_kb_stats()
        
        print("\n=== Thống kê hệ thống ===")
        print(f"Tổng số thực thể: {kb_stats['nodes']}")
        print(f"Tổng số mối quan hệ: {kb_stats['edges']}")
        
        print("\nLoại thực thể:")
        for type_name, count in kb_stats['types'].items():
            print(f"  - {type_name}: {count}")
        
        print(f"\nSố lần tương tác: {len(self.history)}")
        
        # Hiển thị thêm thống kê khác nếu ở chế độ verbose
        if self.verbose and self.history:
            total_time = sum(item['response'].get('process_time', 0) for item in self.history if 'process_time' in item['response'])
            avg_time = total_time / len(self.history) if self.history else 0
            print(f"Thời gian xử lý trung bình: {avg_time:.2f} giây")
    
    def _print_welcome(self):
        """Hiển thị thông điệp chào mừng"""
        print("\n" + "=" * 60)
        print("Simple AGI - Hệ thống AGI đơn giản với khả năng tự học")
        print("=" * 60)
        print("Nhập câu hỏi hoặc yêu cầu của bạn")
        print("Gõ /help để xem trợ giúp hoặc exit để thoát")
        print("=" * 60)