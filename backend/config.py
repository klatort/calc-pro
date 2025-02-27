import os

class Config:
    ROOT = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_FOLDER = os.path.join(ROOT, 'uploads')
    WINDOWS_PRICES_DIR = os.path.join(ROOT, './data/windows_prices.xlsx')
    LINUX_PRICES_DIR = os.path.join(ROOT, './data/RI_linux_prices.xlsx')
    UPLOAD_FOLDER = os.path.join(ROOT, 'uploads')