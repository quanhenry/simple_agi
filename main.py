#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple AGI - Hệ thống AGI đơn giản với khả năng tự học
"""

import sys
import argparse
import logging
from core.engine import AGIEngine
from ui.cli import AGICLI
from ui.web import AGIWeb
import config

def parse_arguments():
    """Phân tích tham số dòng lệnh"""
    parser = argparse.ArgumentParser(description='Simple AGI - Hệ thống AGI đơn giản với khả năng tự học')
    parser.add_argument('--ui', default='cli', choices=['cli', 'web'], help='Loại giao diện (mặc định: cli)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Hiển thị thông tin chi tiết')
    return parser.parse_args()

def setup_logging():
    """Cấu hình logging"""
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("simple_agi.log")
        ]
    )
    logger = logging.getLogger("SimpleAGI")
    logger.info("Khởi động Simple AGI")
    return logger

def main():
    """Hàm chính khởi chạy ứng dụng"""
    args = parse_arguments()
    logger = setup_logging()
    
    try:
        # Khởi tạo engine
        logger.info("Khởi tạo AGI Engine")
        engine = AGIEngine()
        
        # Khởi tạo giao diện
        if args.ui == 'cli':
            logger.info("Khởi động giao diện dòng lệnh")
            ui = AGICLI(engine, verbose=args.verbose)
            ui.start()
        elif args.ui == 'web':
            logger.info("Khởi động giao diện web")
            ui = AGIWeb(engine, verbose=args.verbose)
            ui.start()
    except Exception as e:
        logger.error(f"Lỗi khởi động: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nThoát ứng dụng...")
        sys.exit(0)