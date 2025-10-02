
# import modin.pandas as pd
import pandas as pd
import re
from pathlib import Path
from worker import create_task

import logging

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
    # excel_file_path = '../data/2025 - Copy.xlsx'
    # excel_file_path = '../data/2024.xlsx'
    excel_file_path = '../data/2024 - Copy.xlsx'
    res = create_task(excel_file_path)
    # print(res)

if __name__ == "__main__":
    main()