"""
Web Interface - Giao diện web đơn giản cho hệ thống AGI
"""

import logging
import time
import json
import threading
from typing import Dict, Any, List

from flask import Flask, render_template, request, jsonify, Response

class AGIWeb:
    """
    Giao diện web đơn giản cho hệ thống AGI
    """
    
    def __init__(self, engine, host="0.0.0.0", port=8000, verbose=False):
        """
        Khởi tạo giao diện web
        
        Args:
            engine: Engine AGI chính
            host: Host để lắng nghe (mặc định: 0.0.0.0)
            port: Port để lắng nghe (mặc định: 5000)
            verbose: Chế độ hiển thị thông tin chi tiết
        """
        self.engine = engine
        self.host = host
        self.port = port
        self.verbose = verbose
        self.logger = logging.getLogger("AGIWeb")
        self.history = []  # Lịch sử tương tác
        
        # Khởi tạo Flask app
        self.app = Flask(__name__)
        self._setup_routes()
        
        self.logger.info("AGIWeb đã được khởi tạo")
    
    def start(self):
        """Khởi động giao diện web"""
        self.logger.info(f"Khởi động giao diện web tại http://{self.host}:{self.port}")
        print(f"Khởi động giao diện web tại http://{self.host}:{self.port}")
        
        # Khởi động Flask trong một thread riêng
        threading.Thread(target=self._run_flask, daemon=True).start()
        
        # Giữ tiến trình chính chạy
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("Đã nhận tín hiệu thoát")
            print("\nThoát ứng dụng...")
    
    def _run_flask(self):
        """Chạy Flask app"""
        self.app.run(host=self.host, port=self.port, debug=False, use_reloader=False)
    
    def _setup_routes(self):
        """Thiết lập các route cho Flask app"""
        
        # @self.app.route('/')
        # def index():
        #     """Trang chủ"""
        #     return render_template('/Users/quannguyen/Downloads/AI-AGI/simple_agi/templates/index.html')
        @self.app.route('/')
        def index():
            """Trang chủ"""
            html = """
            <!DOCTYPE html>
            <html lang="vi">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Simple AGI - Hệ thống AGI đơn giản</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        line-height: 1.6;
                        margin: 0;
                        padding: 20px;
                        color: #333;
                    }
                    .container {
                        max-width: 800px;
                        margin: 0 auto;
                    }
                    header {
                        text-align: center;
                        margin-bottom: 20px;
                        padding-bottom: 10px;
                        border-bottom: 1px solid #eee;
                    }
                    .chat-container {
                        display: flex;
                        flex-direction: column;
                        height: 500px;
                        border: 1px solid #ddd;
                        border-radius: 5px;
                    }
                    .chat-messages {
                        flex: 1;
                        overflow-y: auto;
                        padding: 15px;
                        background-color: #f9f9f9;
                    }
                    .message {
                        margin-bottom: 15px;
                        padding: 10px;
                        border-radius: 5px;
                    }
                    .user-message {
                        background-color: #dcf8c6;
                        align-self: flex-end;
                        margin-left: 40px;
                    }
                    .agi-message {
                        background-color: #fff;
                        align-self: flex-start;
                        margin-right: 40px;
                        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
                    }
                    .chat-input {
                        display: flex;
                        padding: 10px;
                        border-top: 1px solid #ddd;
                        background-color: #fff;
                    }
                    .chat-input input {
                        flex: 1;
                        padding: 10px;
                        border: 1px solid #ddd;
                        border-radius: 4px;
                    }
                    .chat-input button {
                        padding: 10px 15px;
                        margin-left: 10px;
                        background-color: #4CAF50;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        cursor: pointer;
                    }
                    .stats {
                        margin-top: 20px;
                        padding: 15px;
                        background-color: #f5f5f5;
                        border-radius: 5px;
                    }
                    footer {
                        margin-top: 30px;
                        text-align: center;
                        color: #666;
                    }
                    .loading {
                        text-align: center;
                        padding: 20px;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <header>
                        <h1>Simple AGI</h1>
                        <p>Hệ thống AGI đơn giản với khả năng tự học</p>
                    </header>
                    
                    <div class="chat-container">
                        <div id="chatMessages" class="chat-messages">
                            <div class="message agi-message">
                                Xin chào! Tôi là Simple AGI. Bạn có thể hỏi tôi bất cứ điều gì.
                            </div>
                        </div>
                        <div class="chat-input">
                            <input type="text" id="queryInput" placeholder="Nhập câu hỏi của bạn..." />
                            <button id="sendButton">Gửi</button>
                        </div>
                    </div>
                    
                    <div class="stats" id="statsContainer">
                        <h3>Thống kê hệ thống</h3>
                        <div id="statsContent">Đang tải...</div>
                    </div>
                    
                    <footer>
                        <p>© 2025 Simple AGI - Dự án AGI Tự học</p>
                    </footer>
                </div>
                
                <script>
                    document.addEventListener('DOMContentLoaded', function() {
                        const chatMessages = document.getElementById('chatMessages');
                        const queryInput = document.getElementById('queryInput');
                        const sendButton = document.getElementById('sendButton');
                        const statsContent = document.getElementById('statsContent');
                        
                        // Tải thống kê ban đầu
                        loadStats();
                        
                        // Tải lịch sử
                        loadHistory();
                        
                        // Xử lý gửi câu hỏi
                        sendButton.addEventListener('click', sendQuery);
                        queryInput.addEventListener('keypress', function(e) {
                            if (e.key === 'Enter') {
                                sendQuery();
                            }
                        });
                        
                        function sendQuery() {
                            const query = queryInput.value.trim();
                            if (!query) return;
                            
                            // Hiển thị tin nhắn người dùng
                            addMessage(query, 'user');
                            queryInput.value = '';
                            
                            // Hiển thị thông báo đang xử lý
                            const loadingId = 'loading-' + Date.now();
                            chatMessages.innerHTML += `
                                <div id="${loadingId}" class="loading">
                                    <p>Đang xử lý...</p>
                                </div>
                            `;
                            chatMessages.scrollTop = chatMessages.scrollHeight;
                            
                            // Gửi yêu cầu
                            fetch('/api/query', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json'
                                },
                                body: JSON.stringify({ query: query })
                            })
                            .then(response => response.json())
                            .then(data => {
                                // Xóa thông báo đang xử lý
                                const loadingElement = document.getElementById(loadingId);
                                if (loadingElement) {
                                    loadingElement.remove();
                                }
                                
                                // Hiển thị câu trả lời
                                addMessage(data.answer, 'agi');
                                
                                // Cập nhật thống kê
                                loadStats();
                            })
                            .catch(error => {
                                console.error('Error:', error);
                                // Xóa thông báo đang xử lý
                                const loadingElement = document.getElementById(loadingId);
                                if (loadingElement) {
                                    loadingElement.remove();
                                }
                                
                                // Hiển thị thông báo lỗi
                                addMessage('Đã xảy ra lỗi khi xử lý yêu cầu của bạn. Vui lòng thử lại.', 'agi');
                            });
                        }
                        
                        function addMessage(message, type) {
                            const messageClass = type === 'user' ? 'user-message' : 'agi-message';
                            const messageHtml = `
                                <div class="message ${messageClass}">
                                    ${message.replace(/\\n/g, '<br>')}
                                </div>
                            `;
                            chatMessages.innerHTML += messageHtml;
                            chatMessages.scrollTop = chatMessages.scrollHeight;
                        }
                        
                        function loadHistory() {
                            fetch('/api/history?limit=5')
                                .then(response => response.json())
                                .then(data => {
                                    if (data.length > 0) {
                                        // Xóa tin nhắn chào mừng
                                        chatMessages.innerHTML = '';
                                        
                                        // Hiển thị lịch sử
                                        data.forEach(item => {
                                            addMessage(item.query, 'user');
                                            addMessage(item.answer, 'agi');
                                        });
                                    }
                                })
                                .catch(error => console.error('Error loading history:', error));
                        }
                        
                        function loadStats() {
                            fetch('/api/stats')
                                .then(response => response.json())
                                .then(data => {
                                    const statsHtml = `
                                        <p>Số thực thể: ${data.kb.nodes}</p>
                                        <p>Số mối quan hệ: ${data.kb.edges}</p>
                                        <p>Số lần tương tác: ${data.history.total_interactions}</p>
                                        ${data.history.avg_process_time ? 
                                            `<p>Thời gian xử lý trung bình: ${data.history.avg_process_time.toFixed(2)} giây</p>` : ''}
                                    `;
                                    statsContent.innerHTML = statsHtml;
                                })
                                .catch(error => console.error('Error loading stats:', error));
                        }
                    });
                </script>
            </body>
            </html>
            """
            return html
        @self.app.route('/api/query', methods=['POST'])
        def query():
            """API endpoint để xử lý câu hỏi"""
            try:
                data = request.get_json()
                user_input = data.get('query', '')
                
                if not user_input:
                    return jsonify({"error": "Không có câu hỏi"}), 400
                
                self.logger.info(f"Nhận câu hỏi từ web: {user_input}")
                
                # Xử lý yêu cầu
                start_time = time.time()
                response = self.engine.process_request(user_input)
                process_time = time.time() - start_time
                
                # Thêm thông tin thời gian xử lý
                response['process_time'] = process_time
                
                # Thêm vào lịch sử
                self.history.append({
                    "input": user_input,
                    "response": response,
                    "timestamp": time.time()
                })
                
                return jsonify(response)
                
            except Exception as e:
                self.logger.error(f"Lỗi xử lý API query: {e}", exc_info=True)
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/history')
        def history():
            """API endpoint để lấy lịch sử tương tác"""
            limit = request.args.get('limit', default=10, type=int)
            
            # Lấy các mục gần nhất
            recent = self.history[-limit:] if len(self.history) > limit else self.history
            
            # Chuyển đổi thành dạng đơn giản
            simple_history = []
            for item in recent:
                simple_item = {
                    "query": item["input"],
                    "answer": item["response"]["answer"],
                    "timestamp": item["timestamp"],
                    "confidence": item["response"].get("confidence", 0)
                }
                if self.verbose:
                    simple_item["details"] = {
                        "sources": item["response"].get("sources", []),
                        "process_time": item["response"].get("process_time", 0),
                        "question_type": item["response"].get("question_type", "unknown")
                    }
                simple_history.append(simple_item)
            
            return jsonify(simple_history)
        
        @self.app.route('/api/stats')
        def stats():
            """API endpoint để lấy thông kê hệ thống"""
            kb_stats = self.engine.get_kb_stats()
            
            # Tính thêm thống kê từ history
            history_stats = {
                "total_interactions": len(self.history)
            }
            
            if self.history:
                total_time = sum(item['response'].get('process_time', 0) for item in self.history if 'process_time' in item['response'])
                avg_time = total_time / len(self.history) if self.history else 0
                history_stats["avg_process_time"] = avg_time
            
            stats = {
                "kb": kb_stats,
                "history": history_stats,
                "timestamp": time.time()
            }
            
            return jsonify(stats)
    
    def _html_templates(self):
        """
        Tạo các template HTML cơ bản
        
        Chú ý: Trong ứng dụng thực tế, bạn nên tạo các file template riêng
        trong thư mục templates của Flask.
        """
        return {
            "index.html": """
            <!DOCTYPE html>
            <html lang="vi">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Simple AGI - Hệ thống AGI đơn giản</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        line-height: 1.6;
                        margin: 0;
                        padding: 20px;
                        color: #333;
                    }
                    .container {
                        max-width: 800px;
                        margin: 0 auto;
                    }
                    header {
                        text-align: center;
                        margin-bottom: 20px;
                        padding-bottom: 10px;
                        border-bottom: 1px solid #eee;
                    }
                    .chat-container {
                        display: flex;
                        flex-direction: column;
                        height: 500px;
                        border: 1px solid #ddd;
                        border-radius: 5px;
                    }
                    .chat-messages {
                        flex: 1;
                        overflow-y: auto;
                        padding: 15px;
                        background-color: #f9f9f9;
                    }
                    .message {
                        margin-bottom: 15px;
                        padding: 10px;
                        border-radius: 5px;
                    }
                    .user-message {
                        background-color: #dcf8c6;
                        align-self: flex-end;
                        margin-left: 40px;
                    }
                    .agi-message {
                        background-color: #fff;
                        align-self: flex-start;
                        margin-right: 40px;
                        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
                    }
                    .chat-input {
                        display: flex;
                        padding: 10px;
                        border-top: 1px solid #ddd;
                        background-color: #fff;
                    }
                    .chat-input input {
                        flex: 1;
                        padding: 10px;
                        border: 1px solid #ddd;
                        border-radius: 4px;
                    }
                    .chat-input button {
                        padding: 10px 15px;
                        margin-left: 10px;
                        background-color: #4CAF50;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        cursor: pointer;
                    }
                    .stats {
                        margin-top: 20px;
                        padding: 15px;
                        background-color: #f5f5f5;
                        border-radius: 5px;
                    }
                    footer {
                        margin-top: 30px;
                        text-align: center;
                        color: #666;
                    }
                    .loading {
                        text-align: center;
                        padding: 20px;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <header>
                        <h1>Simple AGI</h1>
                        <p>Hệ thống AGI đơn giản với khả năng tự học</p>
                    </header>
                    
                    <div class="chat-container">
                        <div id="chatMessages" class="chat-messages">
                            <div class="message agi-message">
                                Xin chào! Tôi là Simple AGI. Bạn có thể hỏi tôi bất cứ điều gì.
                            </div>
                        </div>
                        <div class="chat-input">
                            <input type="text" id="queryInput" placeholder="Nhập câu hỏi của bạn..." />
                            <button id="sendButton">Gửi</button>
                        </div>
                    </div>
                    
                    <div class="stats" id="statsContainer">
                        <h3>Thống kê hệ thống</h3>
                        <div id="statsContent">Đang tải...</div>
                    </div>
                    
                    <footer>
                        <p>© 2025 Simple AGI - Dự án AGI Tự học</p>
                    </footer>
                </div>
                
                <script>
                    document.addEventListener('DOMContentLoaded', function() {
                        const chatMessages = document.getElementById('chatMessages');
                        const queryInput = document.getElementById('queryInput');
                        const sendButton = document.getElementById('sendButton');
                        const statsContent = document.getElementById('statsContent');
                        
                        // Tải thống kê ban đầu
                        loadStats();
                        
                        // Tải lịch sử
                        loadHistory();
                        
                        // Xử lý gửi câu hỏi
                        sendButton.addEventListener('click', sendQuery);
                        queryInput.addEventListener('keypress', function(e) {
                            if (e.key === 'Enter') {
                                sendQuery();
                            }
                        });
                        
                        function sendQuery() {
                            const query = queryInput.value.trim();
                            if (!query) return;
                            
                            // Hiển thị tin nhắn người dùng
                            addMessage(query, 'user');
                            queryInput.value = '';
                            
                            // Hiển thị thông báo đang xử lý
                            const loadingId = 'loading-' + Date.now();
                            chatMessages.innerHTML += `
                                <div id="${loadingId}" class="loading">
                                    <p>Đang xử lý...</p>
                                </div>
                            `;
                            chatMessages.scrollTop = chatMessages.scrollHeight;
                            
                            // Gửi yêu cầu
                            fetch('/api/query', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json'
                                },
                                body: JSON.stringify({ query: query })
                            })
                            .then(response => response.json())
                            .then(data => {
                                // Xóa thông báo đang xử lý
                                const loadingElement = document.getElementById(loadingId);
                                if (loadingElement) {
                                    loadingElement.remove();
                                }
                                
                                // Hiển thị câu trả lời
                                addMessage(data.answer, 'agi');
                                
                                // Cập nhật thống kê
                                loadStats();
                            })
                            .catch(error => {
                                console.error('Error:', error);
                                // Xóa thông báo đang xử lý
                                const loadingElement = document.getElementById(loadingId);
                                if (loadingElement) {
                                    loadingElement.remove();
                                }
                                
                                // Hiển thị thông báo lỗi
                                addMessage('Đã xảy ra lỗi khi xử lý yêu cầu của bạn. Vui lòng thử lại.', 'agi');
                            });
                        }
                        
                        function addMessage(message, type) {
                            const messageClass = type === 'user' ? 'user-message' : 'agi-message';
                            const messageHtml = `
                                <div class="message ${messageClass}">
                                    ${message.replace(/\\n/g, '<br>')}
                                </div>
                            `;
                            chatMessages.innerHTML += messageHtml;
                            chatMessages.scrollTop = chatMessages.scrollHeight;
                        }
                        
                        function loadHistory() {
                            fetch('/api/history?limit=5')
                                .then(response => response.json())
                                .then(data => {
                                    if (data.length > 0) {
                                        // Xóa tin nhắn chào mừng
                                        chatMessages.innerHTML = '';
                                        
                                        // Hiển thị lịch sử
                                        data.forEach(item => {
                                            addMessage(item.query, 'user');
                                            addMessage(item.answer, 'agi');
                                        });
                                    }
                                })
                                .catch(error => console.error('Error loading history:', error));
                        }
                        
                        function loadStats() {
                            fetch('/api/stats')
                                .then(response => response.json())
                                .then(data => {
                                    const statsHtml = `
                                        <p>Số thực thể: ${data.kb.nodes}</p>
                                        <p>Số mối quan hệ: ${data.kb.edges}</p>
                                        <p>Số lần tương tác: ${data.history.total_interactions}</p>
                                        ${data.history.avg_process_time ? 
                                            `<p>Thời gian xử lý trung bình: ${data.history.avg_process_time.toFixed(2)} giây</p>` : ''}
                                    `;
                                    statsContent.innerHTML = statsHtml;
                                })
                                .catch(error => console.error('Error loading stats:', error));
                        }
                    });
                </script>
            </body>
            </html>
            """
        }