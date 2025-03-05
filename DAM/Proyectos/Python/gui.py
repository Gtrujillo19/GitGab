import requests
import tkinter as tk
from tkinter import scrolledtext, ttk
import webbrowser
import logging

def create_gui(bot):
    try:
        print("Creando la ventana gráfica...")
        window = tk.Tk()
        log_widget = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=90, height=10)
        balance_label = ttk.Label()
        status_label = ttk.Label()
        history_widget = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=90, height=10, state="disabled")
        stats_label = ttk.Label()
        bot.log_widget = log_widget
        bot.balance_label = balance_label
        bot.status_label = status_label
        bot.history_widget = history_widget
        bot.stats_label = stats_label
        log_widget = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=90, height=10)
        balance_label = ttk.Label()
        status_label = ttk.Label()
        history_widget = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=90, height=10, state="disabled")
        stats_label = ttk.Label()
        bot.log_widget = log_widget
        bot.balance_label = balance_label
        bot.status_label = status_label
        bot.history_widget = history_widget
        bot.stats_label = stats_label
        window.title("Bot Trade Minimalista - Logs")
        window.geometry("900x700")
        bot.window = window

        try:
            webbrowser.register('safari', None, webbrowser.MacOSXOSAScript('safari'))
            tradingview_url = "https://www.tradingview.com/chart/?symbol=BINANCE:BTCUSDT"
            webbrowser.get('safari').open(tradingview_url, new=2)
        except Exception as e:
            bot.log(f"Error al abrir TradingView en Safari: {str(e)}", "error")
            webbrowser.open(tradingview_url, new=2)

        menubar = tk.Menu(window)
        window.config(menu=menubar)
        theme_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Themes", menu=theme_menu)
        for theme_name in bot.themes.keys():
            theme_menu.add_command(label=theme_name, command=lambda t=theme_name: bot.apply_theme(t))
        theme_menu.add_separator()
        theme_menu.add_command(label="Edit Themes", command=bot.edit_themes)
        theme_menu.add_command(label="Edit UI Elements", command=lambda: edit_ui_elements(bot))

        frame = ttk.Frame(window)
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        title_label = ttk.Label(frame, text="Bot Trade Minimalista", style="TLabel")
        title_label.pack(pady=10)

        settings_frame = ttk.Frame(frame)
        settings_frame.pack(fill="x", pady=5)

        strategy_label = ttk.Label(settings_frame, text="Select Strategy:", style="Small.TLabel")
        strategy_label.pack(side=tk.LEFT, padx=5)
        strategies = ["moving_average", "rsi", "threshold", "macd", "ma_rsi", "wyckoff"]
        strategy_combo = ttk.Combobox(settings_frame, values=strategies, state="readonly", width=20)
        strategy_combo.set("moving_average")
        strategy_combo.pack(side=tk.LEFT, padx=5)

        def update_strategy(event):
            bot.strategy_type = strategy_combo.get()
            bot.log(f"Strategy updated to: {bot.strategy_type}")

        strategy_combo.bind("<<ComboboxSelected>>", update_strategy)

        timeframe_label = ttk.Label(settings_frame, text="Select Timeframe:", style="Small.TLabel")
        timeframe_label.pack(side=tk.LEFT, padx=(20, 5))
        timeframes = ["1m", "3m", "5m", "15m", "30m", "1h", "4h", "1d"]
        timeframe_combo = ttk.Combobox(settings_frame, values=timeframes, state="readonly", width=10)
        timeframe_combo.set(bot.timeframe)
        timeframe_combo.pack(side=tk.LEFT, padx=5)

        def update_timeframe(event):
            bot.timeframe = timeframe_combo.get()
            bot.log(f"Timeframe updated to: {bot.timeframe}")
            bot.save_config()

        timeframe_combo.bind("<<ComboboxSelected>>", update_timeframe)

        symbol_label = ttk.Label(settings_frame, text="Select Symbol:", style="Small.TLabel")
        symbol_label.pack(side=tk.LEFT, padx=(20, 5))
        symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
        symbol_combo = ttk.Combobox(settings_frame, values=symbols, state="readonly", width=10)
        symbol_combo.set(bot.SYMBOL if hasattr(bot, "SYMBOL") else "BTCUSDT")
        symbol_combo.pack(side=tk.LEFT, padx=5)

        def update_symbol(event):
            bot.SYMBOL = symbol_combo.get()
            bot.log(f"Symbol updated to: {bot.SYMBOL}")
            bot.save_config()

        symbol_combo.bind("<<ComboboxSelected>>", update_symbol)

        status_frame = ttk.Frame(frame)
        status_frame.pack(fill="x", pady=5)
        status_label = ttk.Label(status_frame, text="Estado: Detenido", style="Small.TLabel")
        status_label.pack(side=tk.LEFT, padx=5)
        bot.status_label = status_label

        balance_label = ttk.Label(status_frame, text="Saldo: Cargando...", style="Small.TLabel")
        balance_label.pack(side=tk.LEFT, padx=20)
        bot.balance_label = balance_label

        stats_label = ttk.Label(status_frame, text="Total Trades: 0", style="Small.TLabel")
        stats_label.pack(side=tk.RIGHT, padx=5)
        bot.stats_label = stats_label

        log_frame = ttk.Frame(frame)
        log_frame.pack(fill="x", pady=5)
        log_label = ttk.Label(log_frame, text="Logs", style="Small.TLabel")
        log_label.pack(anchor="w", padx=5)
        log_widget = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, width=90, height=10)
        log_widget.pack(padx=5, pady=5, fill="x")
        bot.log_widget = log_widget

        history_frame = ttk.Frame(frame)
        history_frame.pack(fill="x", pady=5)
        history_label = ttk.Label(history_frame, text="Trade History", style="Small.TLabel")
        history_label.pack(anchor="w", padx=5)
        history_widget = scrolledtext.ScrolledText(history_frame, wrap=tk.WORD, width=90, height=10, state="disabled")
        history_widget.pack(padx=5, pady=5, fill="x")
        bot.history_widget = history_widget

        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=10)

        start_button_frame = ttk.Frame(button_frame)
        start_button_frame.pack(side=tk.LEFT, padx=10)
        start_button = ttk.Button(start_button_frame, text="▶ Start", command=bot.start, style="TButton")
        start_button.pack()
        start_label = ttk.Label(start_button_frame, text="Iniciar Bot", style="Small.TLabel")
        start_label.pack()

        pause_button_frame = ttk.Frame(button_frame)
        pause_button_frame.pack(side=tk.LEFT, padx=10)
        pause_button = ttk.Button(pause_button_frame, text="⏸ Pause", command=bot.pause, style="TButton")
        pause_button.pack()
        pause_label = ttk.Label(pause_button_frame, text="Pausar/Reanudar", style="Small.TLabel")
        pause_label.pack()

        stop_button_frame = ttk.Frame(button_frame)
        stop_button_frame.pack(side=tk.LEFT, padx=10)
        stop_button = ttk.Button(stop_button_frame, text="⏹ Stop", command=bot.stop, style="TButton")
        stop_button.pack()
        stop_label = ttk.Label(stop_button_frame, text="Detener Bot", style="Small.TLabel")
        stop_label.pack()

        edit_button_frame = ttk.Frame(button_frame)
        edit_button_frame.pack(side=tk.LEFT, padx=10)
        edit_button = ttk.Button(edit_button_frame, text="⚙ Params", command=bot.edit_parameters, style="TButton")
        edit_button.pack()
        edit_label = ttk.Label(edit_button_frame, text="Editar Parámetros", style="Small.TLabel")
        edit_label.pack()

        stats_button_frame = ttk.Frame(button_frame)
        stats_button_frame.pack(side=tk.LEFT, padx=10)
        stats_button = ttk.Button(stats_button_frame, text="📈 Stats", command=bot.show_statistics, style="TButton")
        stats_button.pack()
        stats_label = ttk.Label(stats_button_frame, text="Mostrar Estadísticas", style="Small.TLabel")
        stats_label.pack()

        pnl_button_frame = ttk.Frame(button_frame)
        pnl_button_frame.pack(side=tk.LEFT, padx=10)
        pnl_button = ttk.Button(pnl_button_frame, text="📊 PnL", command=bot.show_pnl_analysis, style="TButton")
        pnl_button.pack()
        pnl_label = ttk.Label(pnl_button_frame, text="Mostrar PnL", style="Small.TLabel")
        pnl_label.pack()

        info_button_frame = ttk.Frame(button_frame)
        info_button_frame.pack(side=tk.LEFT, padx=10)
        info_button = ttk.Button(info_button_frame, text="ℹ Info", command=bot.show_strategy_info, style="TButton")
        info_button.pack()
        info_label = ttk.Label(info_button_frame, text="Info Estrategias", style="Small.TLabel")
        info_label.pack()

        bot.apply_theme("High Contrast")  # Aplicar tema después de crear widgets
        bot.check_connection_and_balance()

        # Frame para mostrar precios en tiempo real
        price_frame = ttk.Frame(window)
        price_frame.pack(pady=10, fill="x")

        btc_label = ttk.Label(price_frame, text="BTC: Loading...", font=("Helvetica", 12))
        btc_label.pack(side=tk.LEFT, padx=10)

        eth_label = ttk.Label(price_frame, text="ETH: Loading...", font=("Helvetica", 12))
        eth_label.pack(side=tk.LEFT, padx=10)

        usdt_label = ttk.Label(price_frame, text="USDT: 1.00", font=("Helvetica", 12))
        usdt_label.pack(side=tk.LEFT, padx=10)

        def fetch_prices():
            """Obtiene precios en tiempo real desde Binance."""
            try:
                url = "https://api.binance.com/api/v3/ticker/price"
                response = requests.get(url, timeout=5)
                data = response.json()
                btc_price = next(item["price"] for item in data if item["symbol"] == "BTCUSDT")
                eth_price = next(item["price"] for item in data if item["symbol"] == "ETHUSDT")
                return btc_price, eth_price
            except Exception as e:
                bot.log(f"Error fetching prices: {str(e)}", "error")
                return "Error", "Error"

        def update_prices():
            """Actualiza las etiquetas con los precios en tiempo real."""
            btc_price, eth_price = fetch_prices()
            btc_label.config(text=f"BTC: {btc_price} USDT")
            eth_label.config(text=f"ETH: {eth_price} USDT")
            window.after(5000, update_prices)  # Actualiza cada 5 segundos

        update_prices()  # Inicia la actualización de precios

        window.mainloop()
    except Exception as e:
        print(f"Error al crear la interfaz gráfica: {str(e)}")
        logging.error(f"Error al crear la interfaz gráfica: {str(e)}")
