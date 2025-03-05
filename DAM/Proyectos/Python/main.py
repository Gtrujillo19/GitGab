from tkinter import scrolledtext, ttk, messagebox, font, colorchooser
import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox, font, colorchooser
from bot import BinanceBot
from gui import create_gui
from config import client, time_difference

if __name__ == "__main__":
    try:
        print("Iniciando el programa...")
        use_gui = True
        if use_gui:
            log_widget = scrolledtext.ScrolledText()
            balance_label = ttk.Label()
            status_label = ttk.Label()
            history_widget = scrolledtext.ScrolledText()
            stats_label = ttk.Label()
            bot = BinanceBot(log_widget=log_widget, balance_label=balance_label, status_label=status_label, history_widget=history_widget, stats_label=stats_label, use_gui=True, strategy_type="moving_average", timeframe="1m", time_difference=time_difference)
            log_widget = scrolledtext.ScrolledText()
            balance_label = ttk.Label()
            status_label = ttk.Label()
            history_widget = scrolledtext.ScrolledText()
            stats_label = ttk.Label()
            bot = BinanceBot(log_widget=log_widget, balance_label=balance_label, status_label=status_label, history_widget=history_widget, stats_label=stats_label, use_gui=True, strategy_type="moving_average", timeframe="1m", time_difference=time_difference)
            create_gui(bot)
        else:
            bot = BinanceBot(use_gui=False, strategy_type="moving_average", timeframe="1m", time_difference=time_difference)
            bot.start()
    except Exception as e:
        print(f"Error al ejecutar el programa: {str(e)}")
        import logging
        logging.error(f"Error al ejecutar el programa: {str(e)}")