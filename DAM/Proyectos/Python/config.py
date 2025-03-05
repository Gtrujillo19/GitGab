
import logging
import time
import requests
from binance.client import Client
from utils import sync_time_with_binance

# Configuración básica
SYMBOL = "BTCUSDT"
API_KEY = "1m4KedCWE1cucFaEdDfBltplNTGf8PJx9Z9Nag450pS21F5xI7UtJc7fj3TWm2aG"
API_SECRET = "IMlZNSvLyMf7HkNYJq2tbrlnlp4m6lcdMbaaCL6lVLBhS0cqnPAs7GAMmJpvxlX0"

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot_logs.log"),
        logging.StreamHandler()
    ]
)

# Sincronización del tiempo con el servidor de Binance
time_difference = sync_time_with_binance()

# Cliente de Binance Testnet
try:
    client = Client(API_KEY, API_SECRET, testnet=True)
    client.API_URL = "https://testnet.binance.vision/api"
except Exception as e:
    logging.error(f"Error al inicializar el cliente de Binance: {str(e)}")
    raise