from theme_editor import edit_ui_elements
import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox, font, colorchooser
import threading
import logging
import time
import json
import os
import re
from config import SYMBOL, client
from utils import calculate_ema, calculate_moving_averages, calculate_rsi, calculate_macd
# Importamos trading_strategy desde strategy.py
from strategy import trading_strategy


class BinanceBot:
    def __init__(
        self,
        log_widget=None,
        balance_label=None,
        status_label=None,
        history_widget=None,
        stats_label=None,
        use_gui=True,
        strategy_type="moving_average",
        timeframe="1m",
        time_difference=0):
        # Inicializa los atributos primero
        self.SYMBOL = "BTCUSDT"  # Par de trading por defecto
        print("Inicializando BinanceBot...")
        self.position = None
        self.btc_balance = 0.0
        self.usdt_balance = 0.0
        self.log_widget = log_widget
        self.balance_label = balance_label
        self.status_label = status_label
        self.history_widget = history_widget
        self.stats_label = stats_label
        self.use_gui = use_gui  # Inicializa use_gui antes de usarlo
        self.running = False
        self.paused = False
        self.strategy_type = strategy_type
        self.previous_strategy_type = strategy_type
        self.timeframe = timeframe
        self.previous_timeframe = timeframe
        self.window = None
        self.price_history = []
        self.trades = []
        self.time_difference = time_difference  # Usamos el parámetro pasado
        self.trading_strategy = trading_strategy  # Asignamos la función importada

        # Verifica la inicialización de los widgets de la GUI
        if self.use_gui:
            if not self.log_widget or not self.balance_label or not self.status_label:
                self.log("Error: Widgets de la GUI no inicializados correctamente.", "error")
                return

        self.strategy_descriptions = {
            "rsi": "RSI (Índice de Fuerza Relativa): Utiliza el RSI para identificar condiciones de sobrecompra y sobreventa. Compra cuando el RSI cruza por debajo del nivel de sobreventa (por ejemplo, 30), indicando un posible rebote alcista. Vende cuando el RSI cruza por encima del nivel de sobrecompra (por ejemplo, 70), sugiriendo una corrección bajista.",
            "threshold": "Threshold (Umbral): Opera con niveles de soporte y resistencia definidos. Compra cuando el precio cae por debajo del soporte, esperando un rebote. Vende cuando el precio supera la resistencia, anticipando una corrección. Incluye un stop-loss para limitar pérdidas.",
            "macd": "MACD (Convergencia/Divergencia de Medias Móviles): Usa el indicador MACD, que mide la diferencia entre dos medias móviles exponenciales (EMA rápida y lenta). Compra cuando la línea MACD cruza por encima de la línea de señal (tendencia alcista). Vende cuando cruza por debajo (tendencia bajista).",
            "ma_rsi": "Moving Average + RSI (Combinada): Combina las estrategias Moving Average y RSI. Compra cuando la media móvil rápida cruza por encima de la lenta Y el RSI cruza por debajo del nivel de sobreventa. Vende cuando la media móvil rápida cruza por debajo de la lenta Y el RSI cruza por encima del nivel de sobrecompra.",
            "wyckoff": "Wyckoff: Basada en la teoría Wyckoff, busca fases de acumulación y distribución. Compra en una fase de acumulación (precio cerca del soporte con aumento de volumen). Vende en una fase de distribución (precio cerca de la resistencia con aumento de volumen). Incluye un stop-loss para limitar pérdidas."
        }

        # Parámetros de estrategias (editables)
        self.strategy_params = {
            "moving_average": {"fast_period": 5, "slow_period": 20},
            "rsi": {"rsi_period": 14, "rsi_overbought": 70, "rsi_oversold": 30},
            "threshold": {"support_level": 49000, "resistance_level": 51000, "stop_loss_percent": 0.02},
            "macd": {"fast_length": 12, "slow_length": 26, "signal_length": 9},
            "ma_rsi": {"fast_period": 5, "slow_period": 20, "rsi_period": 14, "rsi_overbought": 70, "rsi_oversold": 30},
            "wyckoff": {"support_level": 49000, "resistance_level": 51000, "volume_threshold": 1.5, "stop_loss_percent": 0.02}
        }

        # Cargar configuraciones guardadas si existen
        self.load_config()

        # Definir temas predefinidos, incluyendo el tema "High Contrast"
        self.themes = {
            "Midnight Blue": {
                "window_bg": "#1A2634",
                "frame_bg": "#2C3E50",
                "label_fg": "#DDEEFF",
                "button_bg": "#4A90E2",
                "button_fg": "#FFFFFF",
                "text_bg": "#223344",
                "text_fg": "#DDEEFF",
                "highlight": "#FFA726"
            },
            "Soft Light": {
                "window_bg": "#F5F7FA",
                "frame_bg": "#FFFFFF",
                "label_fg": "#333333",
                "button_bg": "#48C774",
                "button_fg": "#FFFFFF",
                "text_bg": "#F9FAFB",
                "text_fg": "#333333",
                "highlight": "#FF6B6B"
            },
            "Twilight Forest": {
                "window_bg": "#2D3E40",
                "frame_bg": "#3E5A5F",
                "label_fg": "#C7E8CA",
                "button_bg": "#6BAF92",
                "button_fg": "#FFFFFF",
                "text_bg": "#344B4D",
                "text_fg": "#C7E8CA",
                "highlight": "#FFD54F"
            },
            "High Contrast": {
                "window_bg": "#FFFFFF",
                "frame_bg": "#F5F5F5",
                "label_fg": "#000000",
                "button_bg": "#1976D2",
                "button_fg": "#FFFFFF",
                "text_bg": "#FFFFFF",
                "text_fg": "#212121",
                "highlight": "#D32F2F"
            }
        }
        self.current_theme = "High Contrast"

    def load_config(self):
        if os.path.exists("bot_config.json"):
            try:
                with open("bot_config.json", "r") as f:
                    config = json.load(f)
                    self.strategy_params = config.get("strategy_params", self.strategy_params)
                    self.timeframe = config.get("timeframe", self.timeframe)
                    self.log("Configuración cargada desde bot_config.json")
            except Exception as e:
                self.log(f"Error al cargar configuración: {str(e)}", "error")

        if os.path.exists("themes.json"):
            try:
                with open("themes.json", "r") as f:
                    self.themes = json.load(f)
                    self.log("Temas cargados desde themes.json")
            except Exception as e:
                self.log(f"Error al cargar temas: {str(e)}", "error")

    def save_config(self):
        try:
            config = {
                "strategy_params": self.strategy_params,
                "timeframe": self.timeframe
            }
            with open("bot_config.json", "w") as f:
                json.dump(config, f, indent=4)
                self.log("Configuración guardada en bot_config.json")
        except Exception as e:
            self.log(f"Error al guardar configuración: {str(e)}", "error")

    def apply_theme(self, theme_name):
        try:
            self.current_theme = theme_name
            theme = self.themes[theme_name]

            emoji_font = ("Apple Color Emoji", 11) if "Apple Color Emoji" in font.families() else ("Arial Unicode MS", 11)

            style = ttk.Style()
            style.configure("TFrame", background=theme["frame_bg"])
            style.configure("TLabel", font=("Helvetica", 16, "bold"), background=theme["frame_bg"], foreground=theme["label_fg"])
            style.configure("Small.TLabel", font=("Helvetica", 11), background=theme["frame_bg"], foreground=theme["label_fg"])
            style.configure("TButton", font=emoji_font, padding=8, foreground=theme["button_fg"], background=theme["button_bg"])
            style.map("TButton", background=[("active", theme["button_bg"])], foreground=[("active", theme["button_fg"])])

            if self.window:
                self.window.configure(bg=theme["window_bg"])
            if self.log_widget:
                self.log_widget.configure(bg=theme["text_bg"], fg=theme["text_fg"], insertbackground=theme["label_fg"])
                self.log_widget.tag_config("info", foreground=theme["text_fg"])
                self.log_widget.tag_config("error", foreground=theme["highlight"])
            if self.history_widget:
                self.history_widget.configure(bg=theme["text_bg"], fg=theme["text_fg"])
            if self.status_label:
                status_text = self.status_label.cget("text")
                if "Ejecutando" in status_text:
                    self.status_label.configure(foreground=theme["highlight"])
                elif "Pausado" in status_text:
                    self.status_label.configure(foreground="#FFAA00")
                else:
                    self.status_label.configure(foreground="#FF5555")
            if self.stats_label:
                self.stats_label.configure(foreground=theme["label_fg"])
        except KeyError as e:
            self.log(f"Error al aplicar el tema {theme_name}: {str(e)}", "error")
            self.current_theme = "High Contrast"

    def edit_themes(self):
        try:
            themes_window = tk.Toplevel(self.window)
            themes_window.title("Edit Themes")
            themes_window.geometry("600x600")
            theme = self.themes[self.current_theme]
            themes_window.configure(bg=theme["window_bg"])

            style = ttk.Style()
            style.configure("TLabel", font=("Helvetica", 12), background=theme["window_bg"], foreground=theme["label_fg"])
            style.configure("TButton", font=("Apple Color Emoji", 11) if "Apple Color Emoji" in font.families() else ("Arial Unicode MS", 11), padding=8, foreground=theme["button_fg"], background=theme["button_bg"])
            style.map("TButton", background=[("active", theme["button_bg"])], foreground=[("active", theme["button_fg"])])

            title_label = ttk.Label(themes_window, text="Edit Themes", style="TLabel")
            title_label.pack(pady=10)

            theme_label = ttk.Label(themes_window, text="Select Theme to Edit:", style="TLabel")
            theme_label.pack(pady=5)
            theme_combo = ttk.Combobox(themes_window, values=list(self.themes.keys()), state="readonly")
            theme_combo.set(self.current_theme)
            theme_combo.pack(pady=5)

            edit_frame = ttk.Frame(themes_window)
            edit_frame.pack(pady=10, fill="x", padx=20)

            color_entries = {}
            color_buttons = {}
            elements = ["window_bg", "frame_bg", "label_fg", "button_bg", "button_fg", "text_bg", "text_fg", "highlight"]

            def update_color_buttons():
                selected_theme = theme_combo.get()
                for element in elements:
                    color = self.themes[selected_theme][element]
                    color_buttons[element].configure(bg=color)

            for element in elements:
                frame = ttk.Frame(edit_frame)
                frame.pack(fill="x", pady=5)
                ttk.Label(frame, text=f"{element}:", style="TLabel").pack(side=tk.LEFT, padx=5)
                color_entries[element] = ttk.Entry(frame)
                color_entries[element].insert(0, self.themes[theme_combo.get()][element])
                color_entries[element].pack(side=tk.LEFT, padx=5, fill="x", expand=True)
                color_buttons[element] = tk.Button(frame, width=2, command=lambda e=element: pick_color(e))
                color_buttons[element].pack(side=tk.LEFT, padx=5)

            def pick_color(element):
                color = colorchooser.askcolor(title=f"Choose color for {element}")[1]
                if color:
                    color_entries[element].delete(0, tk.END)
                    color_entries[element].insert(0, color)
                    color_buttons[element].configure(bg=color)

            theme_combo.bind("<<ComboboxSelected>>", lambda event: update_color_buttons())

            def save_theme():
                try:
                    selected_theme = theme_combo.get()
                    for element in elements:
                        self.themes[selected_theme][element] = color_entries[element].get()
                    self.apply_theme(selected_theme)
                    self.log(f"Tema {selected_theme} actualizado correctamente.")
                    with open("themes.json", "w") as f:
                        json.dump(self.themes, f, indent=4)
                    self.log("Temas guardados en themes.json")
                except Exception as e:
                    self.log(f"Error al guardar el tema: {str(e)}", "error")

            def add_new_theme():
                new_theme_name = tk.simpledialog.askstring("New Theme", "Enter new theme name:")
                if new_theme_name and new_theme_name not in self.themes:
                    self.themes[new_theme_name] = self.themes[self.current_theme].copy()
                    theme_combo["values"] = list(self.themes.keys())
                    theme_combo.set(new_theme_name)
                    update_color_buttons()
                    self.log(f"Nuevo tema {new_theme_name} creado.")
                elif new_theme_name in self.themes:
                    self.log("El nombre del tema ya existe.", "error")

            button_frame = ttk.Frame(themes_window)
            button_frame.pack(pady=20)
            ttk.Button(button_frame, text="Save Theme", command=save_theme).pack(side=tk.LEFT, padx=10)
            ttk.Button(button_frame, text="Add New Theme", command=add_new_theme).pack(side=tk.LEFT, padx=10)
            ttk.Button(button_frame, text="Edit UI Elements", command=lambda: edit_ui_elements(self)).pack(side=tk.LEFT, padx=10)
            ttk.Button(button_frame, text="Close", command=themes_window.destroy).pack(side=tk.LEFT, padx=10)

            update_color_buttons()
        except Exception as e:
            self.log(f"Error al abrir la ventana de edición de temas: {str(e)}", "error")

    def log(self, message, level="info"):
        print(f"Log: {message}")
        if self.use_gui and self.log_widget:
            try:
                if level == "info":
                    logging.info(message)
                    self.log_widget.insert(tk.END, f"{message}\n", "info")
                elif level == "error":
                    logging.error(message)
                    self.log_widget.insert(tk.END, f"{message}\n", "error")
                self.log_widget.see(tk.END)
            except tk.TclError as e:
                logging.error(f"Error al escribir en el widget de log: {str(e)}")
        else:
            if level == "info":
                logging.info(message)
            elif level == "error":
                logging.error(message)

    def update_history(self, message, strategy=None):
        if self.use_gui and self.history_widget:
            try:
                self.history_widget.configure(state="normal")
                self.history_widget.insert(tk.END, f"{message}\n")
                self.history_widget.see(tk.END)
                self.history_widget.configure(state="disabled")
                if "Compra" in message or "Venta" in message or "Stop-loss" in message:
                    self.trades.append({
                        "message": message,
                        "strategy": strategy if strategy else self.strategy_type
                    })
                if self.stats_label:
                    total_trades = len(self.trades)
                    self.stats_label.config(text=f"Total Trades: {total_trades}")
            except tk.TclError as e:
                self.log(f"Error al actualizar el historial: {str(e)}", "error")

    def check_connection_and_balance(self):
        retries = 3
        for attempt in range(retries):
            try:
                client.get_system_status()
                self.log("Conexión con Binance Testnet establecida correctamente.")
                account = client.get_account()
                self.usdt_balance = float(next(item for item in account['balances'] if item['asset'] == 'USDT')['free'])
                self.btc_balance = float(next(item for item in account['balances'] if item['asset'] == 'BTC')['free'])
                self.log(f"Saldo: {self.usdt_balance:.2f} USDT | {self.btc_balance:.6f} BTC")
                if self.balance_label:
                    self.balance_label.config(text=f"Saldo: {self.usdt_balance:.2f} USDT | {self.btc_balance:.6f} BTC")
                return
            except Exception as e:
                self.log(f"Error al conectar con Binance Testnet (intento {attempt + 1}/{retries}): {str(e)}", "error")
                if attempt < retries - 1:
                    time.sleep(5)
                else:
                    if self.balance_label:
                        self.balance_label.config(text="Saldo: Error")
                    raise Exception("No se pudo establecer conexión con Binance Testnet después de varios intentos.")

    def get_historical_data(self, symbol="BTCUSDT", interval="1m", limit=100):
        retries = 3
        for attempt in range(retries):
            try:
                client._request_margin = 5000
                klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
                close_prices = [float(kline[4]) for kline in klines]
                volumes = [float(kline[5]) for kline in klines]
                return close_prices, volumes
            except Exception as e:
                if "Timestamp for this request was" in str(e):
                    self.log("Timestamp desincronizado. Intentando resincronizar...", "error")
                    self.time_difference = sync_time_with_binance()
                self.log(f"Error al obtener datos históricos (intento {attempt + 1}/{retries}): {str(e)}", "error")
                if attempt < retries - 1:
                    time.sleep(5)
                else:
                    return [], []

    def calculate_ema(self, prices, period):
        return calculate_ema(prices, period, self.log)

    def calculate_moving_averages(self, close_prices, fast_period, slow_period):
        return calculate_moving_averages(close_prices, fast_period, slow_period, self.log)

    def calculate_rsi(self, close_prices, period):
        return calculate_rsi(close_prices, period, self.log)

    def calculate_macd(self, close_prices, fast_length, slow_length, signal_length):
        return calculate_macd(close_prices, fast_length, slow_length, signal_length, self.log)

    def calculate_pnl(self):
        try:
            total_pnl = 0.0
            strategy_pnl = {
                "moving_average": 0.0,
                "rsi": 0.0,
                "threshold": 0.0,
                "macd": 0.0,
                "ma_rsi": 0.0,
                "wyckoff": 0.0
            }
            strategy_trades = {
                "moving_average": [],
                "rsi": [],
                "threshold": [],
                "macd": [],
                "ma_rsi": [],
                "wyckoff": []
            }

            buy_price = None
            buy_quantity = 0.0

            for trade in self.trades:
                message = trade["message"]
                strategy = trade["strategy"]

                price_match = re.search(r"(\d+\.\d+) USDT", message)
                quantity_match = re.search(r"(\d+\.\d+) BTC", message)
                if not price_match or not quantity_match:
                    continue
                price = float(price_match.group(1))
                quantity = float(quantity_match.group(1))

                if "Compra" in message:
                    if buy_price is None:
                        buy_price = price
                        buy_quantity = quantity
                elif "Venta" in message or "Stop-loss" in message:
                    if buy_price is not None:
                        sell_price = price
                        sell_quantity = quantity
                        if sell_quantity == buy_quantity:
                            trade_pnl = (sell_price - buy_price) * buy_quantity
                            total_pnl += trade_pnl
                            strategy_pnl[strategy] += trade_pnl
                            strategy_trades[strategy].append(trade_pnl)
                            buy_price = None
                            buy_quantity = 0.0

            most_profitable_strategy = max(strategy_pnl, key=strategy_pnl.get) if strategy_pnl else "None"
            most_profitable_pnl = strategy_pnl.get(most_profitable_strategy, 0.0)

            return {
                "total_pnl": total_pnl,
                "strategy_pnl": strategy_pnl,
                "strategy_trades": strategy_trades,
                "most_profitable_strategy": most_profitable_strategy,
                "most_profitable_pnl": most_profitable_pnl
            }
        except Exception as e:
            self.log(f"Error al calcular PnL: {str(e)}", "error")
            return {
                "total_pnl": 0.0,
                "strategy_pnl": {strategy: 0.0 for strategy in strategy_pnl.keys()},
                "strategy_trades": {strategy: [] for strategy in strategy_pnl.keys()},
                "most_profitable_strategy": "None",
                "most_profitable_pnl": 0.0
            }

    def show_pnl_analysis(self):
        try:
            pnl_data = self.calculate_pnl()  # Recalcular siempre al abrir

            pnl_window = tk.Toplevel(self.window)
            pnl_window.title("PnL Analysis")
            pnl_window.geometry("600x400")
            theme = self.themes[self.current_theme]
            pnl_window.configure(bg=theme["window_bg"])

            style = ttk.Style()
            style.configure("TLabel", font=("Helvetica", 12), background=theme["window_bg"], foreground=theme["label_fg"])
            style.configure("TButton", font=("Apple Color Emoji", 11) if "Apple Color Emoji" in font.families() else ("Arial Unicode MS", 11), padding=8, foreground=theme["button_fg"], background=theme["button_bg"])
            style.map("TButton", background=[("active", theme["button_bg"])], foreground=[("active", theme["button_fg"])])

            title_label = ttk.Label(pnl_window, text="Profit and Loss Analysis", style="TLabel")
            title_label.pack(pady=10)

            total_pnl_label = ttk.Label(pnl_window, text=f"Total PnL: {pnl_data['total_pnl']:.2f} USDT", style="TLabel")
            total_pnl_label.pack(pady=5)

            strategy_pnl_label = ttk.Label(pnl_window, text="PnL by Strategy:", style="TLabel")
            strategy_pnl_label.pack(pady=5)
            strategy_labels = []
            for strategy, pnl in pnl_data["strategy_pnl"].items():
                label = ttk.Label(pnl_window, text=f"{strategy}: {pnl:.2f} USDT ({len(pnl_data['strategy_trades'][strategy])} trades)", style="TLabel")
                label.pack(pady=2)
                strategy_labels.append(label)

            most_profitable_label = ttk.Label(
                pnl_window,
                text=f"Most Profitable Strategy: {pnl_data['most_profitable_strategy']} ({pnl_data['most_profitable_pnl']:.2f} USDT)",
                style="TLabel"
            )
            most_profitable_label.pack(pady=10)

            def refresh_pnl():
                new_pnl_data = self.calculate_pnl()
                total_pnl_label.config(text=f"Total PnL: {new_pnl_data['total_pnl']:.2f} USDT")
                for i, (strategy, pnl) in enumerate(new_pnl_data["strategy_pnl"].items()):
                    strategy_labels[i].config(text=f"{strategy}: {pnl:.2f} USDT ({len(new_pnl_data['strategy_trades'][strategy])} trades)")
                most_profitable_label.config(text=f"Most Profitable Strategy: {new_pnl_data['most_profitable_strategy']} ({new_pnl_data['most_profitable_pnl']:.2f} USDT)")

            refresh_button = ttk.Button(pnl_window, text="🔄 Refresh", command=refresh_pnl)
            refresh_button.pack(pady=5)

            close_button = ttk.Button(pnl_window, text="Close", command=pnl_window.destroy)
            close_button.pack(pady=10)
        except Exception as e:
            self.log(f"Error al mostrar análisis de PnL: {str(e)}", "error")

    def show_statistics(self):
        try:
            stats_window = tk.Toplevel(self.window)
            stats_window.title("Bot Statistics")
            stats_window.geometry("500x300")
            theme = self.themes[self.current_theme]
            stats_window.configure(bg=theme["window_bg"])

            style = ttk.Style()
            style.configure("TLabel", font=("Helvetica", 12), background=theme["window_bg"], foreground=theme["label_fg"])
            style.configure("TButton", font=("Apple Color Emoji", 11) if "Apple Color Emoji" in font.families() else ("Arial Unicode MS", 11), padding=8, foreground=theme["button_fg"], background=theme["button_bg"])
            style.map("TButton", background=[("active", theme["button_bg"])], foreground=[("active", theme["button_fg"])])

            title_label = ttk.Label(stats_window, text="Bot Statistics", style="TLabel")
            title_label.pack(pady=10)

            total_trades = len(self.trades)
            total_trades_label = ttk.Label(stats_window, text=f"Total Trades: {total_trades}", style="TLabel")
            total_trades_label.pack(pady=5)

            trades_by_strategy = {}
            for trade in self.trades:
                strategy = trade["strategy"]
                trades_by_strategy[strategy] = trades_by_strategy.get(strategy, 0) + 1

            trades_by_strategy_label = ttk.Label(stats_window, text="Trades by Strategy:", style="TLabel")
            trades_by_strategy_label.pack(pady=5)
            for strategy, count in trades_by_strategy.items():
                strategy_label = ttk.Label(stats_window, text=f"{strategy}: {count}", style="TLabel")
                strategy_label.pack(pady=2)

            close_button = ttk.Button(stats_window, text="Close", command=stats_window.destroy)
            close_button.pack(pady=10)
        except Exception as e:
            self.log(f"Error al mostrar estadísticas: {str(e)}", "error")

    def show_strategy_info(self):
        try:
            info_window = tk.Toplevel(self.window)
            info_window.title("Strategies Info")
            info_window.geometry("700x500")
            theme = self.themes[self.current_theme]
            info_window.configure(bg=theme["window_bg"])

            style = ttk.Style()
            style.configure("TLabel", font=("Helvetica", 12), background=theme["window_bg"], foreground=theme["label_fg"])
            style.configure("TButton", font=("Apple Color Emoji", 11) if "Apple Color Emoji" in font.families() else ("Arial Unicode MS", 11), padding=8, foreground=theme["button_fg"], background=theme["button_bg"])
            style.map("TButton", background=[("active", theme["button_bg"])], foreground=[("active", theme["button_fg"])])

            title_label = ttk.Label(info_window, text="Strategies Information", style="TLabel")
            title_label.pack(pady=10)

            info_text = tk.Text(info_window, wrap=tk.WORD, height=20, bg=theme["text_bg"], fg=theme["text_fg"], font=("Helvetica", 11))
            info_text.pack(padx=10, pady=5, fill="both", expand=True)

            for strategy, description in self.strategy_descriptions.items():
                info_text.insert(tk.END, f"{strategy.upper()}:\n", "bold")
                info_text.insert(tk.END, f"{description}\n\n")
            info_text.tag_configure("bold", font=("Helvetica", 11, "bold"))
            info_text.configure(state="disabled")

            close_button = ttk.Button(info_window, text="Close", command=info_window.destroy)
            close_button.pack(pady=10)
        except Exception as e:
            self.log(f"Error al mostrar información de estrategias: {str(e)}", "error")

    def edit_parameters(self):
        try:
            params_window = tk.Toplevel(self.window)
            params_window.title(f"Edit Parameters - {self.strategy_type}")
            params_window.geometry("400x500")
            theme = self.themes[self.current_theme]
            params_window.configure(bg=theme["window_bg"])

            style = ttk.Style()
            style.configure("TLabel", font=("Helvetica", 12), background=theme["window_bg"], foreground=theme["label_fg"])
            style.configure("TButton", font=("Apple Color Emoji", 11) if "Apple Color Emoji" in font.families() else ("Arial Unicode MS", 11), padding=8, foreground=theme["button_fg"], background=theme["button_bg"])
            style.map("TButton", background=[("active", theme["button_bg"])], foreground=[("active", theme["button_fg"])])

            title_label = ttk.Label(params_window, text=f"Configure {self.strategy_type} Parameters", style="TLabel")
            title_label.pack(pady=10)

            entries = {}
            if self.strategy_type == "moving_average":
                params = self.strategy_params["moving_average"]
                ttk.Label(params_window, text="Fast Period:", style="TLabel").pack(pady=5)
                fast_entry = ttk.Entry(params_window)
                fast_entry.insert(0, str(params["fast_period"]))
                fast_entry.pack()

                ttk.Label(params_window, text="Slow Period:", style="TLabel").pack(pady=5)
                slow_entry = ttk.Entry(params_window)
                slow_entry.insert(0, str(params["slow_period"]))
                slow_entry.pack()

                entries["fast_period"] = fast_entry
                entries["slow_period"] = slow_entry

            elif self.strategy_type == "rsi":
                params = self.strategy_params["rsi"]
                ttk.Label(params_window, text="RSI Period:", style="TLabel").pack(pady=5)
                rsi_period_entry = ttk.Entry(params_window)
                rsi_period_entry.insert(0, str(params["rsi_period"]))
                rsi_period_entry.pack()

                ttk.Label(params_window, text="RSI Overbought Level:", style="TLabel").pack(pady=5)
                overbought_entry = ttk.Entry(params_window)
                overbought_entry.insert(0, str(params["rsi_overbought"]))
                overbought_entry.pack()

                ttk.Label(params_window, text="RSI Oversold Level:", style="TLabel").pack(pady=5)
                oversold_entry = ttk.Entry(params_window)
                oversold_entry.insert(0, str(params["rsi_oversold"]))
                oversold_entry.pack()

                entries["rsi_period"] = rsi_period_entry
                entries["rsi_overbought"] = overbought_entry
                entries["rsi_oversold"] = oversold_entry

            elif self.strategy_type == "threshold":
                params = self.strategy_params["threshold"]
                ttk.Label(params_window, text="Support Level:", style="TLabel").pack(pady=5)
                support_entry = ttk.Entry(params_window)
                support_entry.insert(0, str(params["support_level"]))
                support_entry.pack()

                ttk.Label(params_window, text="Resistance Level:", style="TLabel").pack(pady=5)
                resistance_entry = ttk.Entry(params_window)
                resistance_entry.insert(0, str(params["resistance_level"]))
                resistance_entry.pack()

                ttk.Label(params_window, text="Stop Loss Percent (e.g., 0.02 for 2%):", style="TLabel").pack(pady=5)
                stop_loss_entry = ttk.Entry(params_window)
                stop_loss_entry.insert(0, str(params["stop_loss_percent"]))
                stop_loss_entry.pack()

                entries["support_level"] = support_entry
                entries["resistance_level"] = resistance_entry
                entries["stop_loss_percent"] = stop_loss_entry

            elif self.strategy_type == "macd":
                params = self.strategy_params["macd"]
                ttk.Label(params_window, text="Fast Length:", style="TLabel").pack(pady=5)
                fast_entry = ttk.Entry(params_window)
                fast_entry.insert(0, str(params["fast_length"]))
                fast_entry.pack()

                ttk.Label(params_window, text="Slow Length:", style="TLabel").pack(pady=5)
                slow_entry = ttk.Entry(params_window)
                slow_entry.insert(0, str(params["slow_length"]))
                slow_entry.pack()

                ttk.Label(params_window, text="Signal Length:", style="TLabel").pack(pady=5)
                signal_entry = ttk.Entry(params_window)
                signal_entry.insert(0, str(params["signal_length"]))
                signal_entry.pack()

                entries["fast_length"] = fast_entry
                entries["slow_length"] = slow_entry
                entries["signal_length"] = signal_entry

            elif self.strategy_type == "ma_rsi":
                params = self.strategy_params["ma_rsi"]
                ttk.Label(params_window, text="Fast Period (MA):", style="TLabel").pack(pady=5)
                fast_entry = ttk.Entry(params_window)
                fast_entry.insert(0, str(params["fast_period"]))
                fast_entry.pack()

                ttk.Label(params_window, text="Slow Period (MA):", style="TLabel").pack(pady=5)
                slow_entry = ttk.Entry(params_window)
                slow_entry.insert(0, str(params["slow_period"]))
                slow_entry.pack()

                ttk.Label(params_window, text="RSI Period:", style="TLabel").pack(pady=5)
                rsi_period_entry = ttk.Entry(params_window)
                rsi_period_entry.insert(0, str(params["rsi_period"]))
                rsi_period_entry.pack()

                ttk.Label(params_window, text="RSI Overbought Level:", style="TLabel").pack(pady=5)
                overbought_entry = ttk.Entry(params_window)
                overbought_entry.insert(0, str(params["rsi_overbought"]))
                overbought_entry.pack()

                ttk.Label(params_window, text="RSI Oversold Level:", style="TLabel").pack(pady=5)
                oversold_entry = ttk.Entry(params_window)
                oversold_entry.insert(0, str(params["rsi_oversold"]))
                oversold_entry.pack()

                entries["fast_period"] = fast_entry
                entries["slow_period"] = slow_entry
                entries["rsi_period"] = rsi_period_entry
                entries["rsi_overbought"] = overbought_entry
                entries["rsi_oversold"] = oversold_entry

            elif self.strategy_type == "wyckoff":
                params = self.strategy_params["wyckoff"]
                ttk.Label(params_window, text="Support Level:", style="TLabel").pack(pady=5)
                support_entry = ttk.Entry(params_window)
                support_entry.insert(0, str(params["support_level"]))
                support_entry.pack()

                ttk.Label(params_window, text="Resistance Level:", style="TLabel").pack(pady=5)
                resistance_entry = ttk.Entry(params_window)
                resistance_entry.insert(0, str(params["resistance_level"]))
                resistance_entry.pack()

                ttk.Label(params_window, text="Volume Threshold (e.g., 1.5 for 50% above average):", style="TLabel").pack(pady=5)
                volume_entry = ttk.Entry(params_window)
                volume_entry.insert(0, str(params["volume_threshold"]))
                volume_entry.pack()

                ttk.Label(params_window, text="Stop Loss Percent (e.g., 0.02 for 2%):", style="TLabel").pack(pady=5)
                stop_loss_entry = ttk.Entry(params_window)
                stop_loss_entry.insert(0, str(params["stop_loss_percent"]))
                stop_loss_entry.pack()

                entries["support_level"] = support_entry
                entries["resistance_level"] = resistance_entry
                entries["volume_threshold"] = volume_entry
                entries["stop_loss_percent"] = stop_loss_entry

            def save_params():
                try:
                    if self.strategy_type == "moving_average":
                        self.strategy_params["moving_average"]["fast_period"] = int(entries["fast_period"].get())
                        self.strategy_params["moving_average"]["slow_period"] = int(entries["slow_period"].get())
                    elif self.strategy_type == "rsi":
                        self.strategy_params["rsi"]["rsi_period"] = int(entries["rsi_period"].get())
                        self.strategy_params["rsi"]["rsi_overbought"] = float(entries["rsi_overbought"].get())
                        self.strategy_params["rsi"]["rsi_oversold"] = float(entries["rsi_oversold"].get())
                    elif self.strategy_type == "threshold":
                        self.strategy_params["threshold"]["support_level"] = float(entries["support_level"].get())
                        self.strategy_params["threshold"]["resistance_level"] = float(entries["resistance_level"].get())
                        self.strategy_params["threshold"]["stop_loss_percent"] = float(entries["stop_loss_percent"].get())
                    elif self.strategy_type == "macd":
                        self.strategy_params["macd"]["fast_length"] = int(entries["fast_length"].get())
                        self.strategy_params["macd"]["slow_length"] = int(entries["slow_length"].get())
                        self.strategy_params["macd"]["signal_length"] = int(entries["signal_length"].get())
                    elif self.strategy_type == "ma_rsi":
                        self.strategy_params["ma_rsi"]["fast_period"] = int(entries["fast_period"].get())
                        self.strategy_params["ma_rsi"]["slow_period"] = int(entries["slow_period"].get())
                        self.strategy_params["ma_rsi"]["rsi_period"] = int(entries["rsi_period"].get())
                        self.strategy_params["ma_rsi"]["rsi_overbought"] = float(entries["rsi_overbought"].get())
                        self.strategy_params["ma_rsi"]["rsi_oversold"] = float(entries["rsi_oversold"].get())
                    elif self.strategy_type == "wyckoff":
                        self.strategy_params["wyckoff"]["support_level"] = float(entries["support_level"].get())
                        self.strategy_params["wyckoff"]["resistance_level"] = float(entries["resistance_level"].get())
                        self.strategy_params["wyckoff"]["volume_threshold"] = float(entries["volume_threshold"].get())
                        self.strategy_params["wyckoff"]["stop_loss_percent"] = float(entries["stop_loss_percent"].get())
                    self.save_config()
                    self.log(f"Parameters for {self.strategy_type} updated successfully.")
                    params_window.destroy()
                except ValueError as e:
                    self.log(f"Error updating parameters: {str(e)}", "error")

            save_button = ttk.Button(params_window, text="Save", command=save_params)
            save_button.pack(pady=10)

            cancel_button = ttk.Button(params_window, text="Cancel", command=params_window.destroy)
            cancel_button.pack(pady=5)
        except Exception as e:
            self.log(f"Error al abrir ventana de edición de parámetros: {str(e)}", "error")

    def start(self):
        try:
            if not self.running:
                self.running = True
                self.paused = False
                self.log("Bot iniciado manualmente...")
                # Usamos una lambda para pasar self explícitamente a trading_strategy
                threading.Thread(target=lambda: self.trading_strategy(self), daemon=True).start()
                if self.status_label:
                    self.status_label.config(text="Estado: Ejecutando", foreground=self.themes[self.current_theme]["highlight"])
            else:
                self.log("El bot ya está en ejecución.", "error")
        except Exception as e:
            self.log(f"Error al iniciar el bot: {str(e)}", "error")

    def stop(self):
        try:
            if self.running:
                self.running = False
                self.paused = False
                self.log("Bot detenido manualmente...")
                if self.status_label:
                    self.status_label.config(text="Estado: Detenido", foreground="#FF5555")
            else:
                self.log("El bot ya está detenido.", "error")
        except Exception as e:
            self.log(f"Error al detener el bot: {str(e)}", "error")

    def pause(self):
        try:
            if self.running and not self.paused:
                self.paused = True
                self.log("Bot pausado.")
                if self.status_label:
                    self.status_label.config(text="Estado: Pausado", foreground="#FFAA00")
            else:
                self.log("El bot no está en ejecución o ya está pausado.", "error")
        except Exception as e:
            self.log(f"Error al pausar el bot: {str(e)}", "error")

    def resume(self):
        try:
            if self.running and self.paused:
                self.paused = False
                self.log("Bot reanudado.")
                if self.status_label:
                    self.status_label.config(text="Estado: Ejecutando", foreground=self.themes[self.current_theme]["highlight"])
            else:
                self.log("El bot no está pausado o no está en ejecución.", "error")
        except Exception as e:
            self.log(f"Error al reanudar el bot: {str(e)}", "error")

    def backup_state(self):
        try:
            backup_data = {
                "trades": self.trades,
                "strategy_params": self.strategy_params,
                "timeframe": self.timeframe,
                "usdt_balance": self.usdt_balance,
                "btc_balance": self.btc_balance,
                "timestamp": time.time()
            }
            with open("data/backup.json", "w") as f:
                json.dump(backup_data, f, indent=4)
            self.log("Copia de seguridad realizada correctamente en data/backup.json")
        except Exception as e:
            self.log(f"Error al realizar la copia de seguridad: {str(e)}", "error")