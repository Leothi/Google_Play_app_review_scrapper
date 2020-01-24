import os

SELENIUM_DRIVER = os.getenv("SELENIUM_DRIVER", "geckodriver")
DOWNLOADS_PATH = os.getenv("DOWNLOADS_PATH")

PROXY_HOST = os.getenv("PROXY_HOST", "localhost")
PROXY_PORT = os.getenv("PROXY_PORT", "40080")
PROXY_USER = os.getenv("PROXY_USER", "")
PROXY_PASS = os.getenv("PROXY_PASS", "")
