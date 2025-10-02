from worker import create_task
import logging
import argparse

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s]: %(message)s',
    handlers=[
        logging.FileHandler('test_worker.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Command line test parser for worker diagnostic')
    parser.add_argument('-f', '--file', type=str, help='The name of the xlsx file')
    args = parser.parse_args()
    # excel_file_path = '../data/2025 - Copy.xlsx'
    # excel_file_path = '../data/2024.xlsx'
    # excel_file_path = '../data/2024 - Copy.xlsx'
    excel_file_path = args.file
    res = create_task(excel_file_path)
    # print(res)

if __name__ == "__main__":
    main()