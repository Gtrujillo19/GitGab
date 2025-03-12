
from config import SYMBOL, client
from plyer import notification
import time
from tkinter import messagebox
from strategies.rsi import rsi_strategy
from strategies.support_resistance import threshold_strategy
from strategies.volume_profile import wyckoff_strategy

def trading_strategy(self):
    symbol = SYMBOL
    quantity = 0.001
    previous_fast_ma = None
    previous_slow_ma = None
    previous_macd = None
    previous_signal = None
    previous_rsi = None
    buy_price = None
    average_volume = None

    self.log(f"Iniciando estrategia: {self.strategy_type} con timeframe: {self.timeframe}")
    iterations_without_data = 0

    while self.running:
        if self.paused:
            self.log("Bot pausado. Esperando reanudación...")
            time.sleep(5)
            continue

        try:
            if self.strategy_type != self.previous_strategy_type or self.timeframe != self.previous_timeframe:
                self.log(f"Strategy changed from {self.previous_strategy_type} to {self.strategy_type} or timeframe changed from {self.previous_timeframe} to {self.timeframe}. Resetting variables.")
                previous_fast_ma = None
                previous_slow_ma = None
                previous_macd = None
                previous_signal = None
                previous_rsi = None
                buy_price = None
                average_volume = None
                self.previous_strategy_type = self.strategy_type
                self.previous_timeframe = self.timeframe

            params = self.strategy_params[self.strategy_type]
            if self.strategy_type == "moving_average":
                fast_period = params["fast_period"]
                slow_period = params["slow_period"]
                limit = max(fast_period, slow_period) + 1
            elif self.strategy_type == "rsi":
                rsi_period = params["rsi_period"]
                limit = rsi_period + 1
            elif self.strategy_type == "threshold":
                limit = 100
            elif self.strategy_type == "macd":
                fast_length = params["fast_length"]
                slow_length = params["slow_length"]
                signal_length = params["signal_length"]
                limit = slow_length + signal_length + 1
            elif self.strategy_type == "ma_rsi":
                fast_period = params["fast_period"]
                slow_period = params["slow_period"]
                rsi_period = params["rsi_period"]
                limit = max(fast_period, slow_period, rsi_period) + 1
            elif self.strategy_type == "wyckoff":
                limit = 100

            close_prices, volumes = self.get_historical_data(symbol=symbol, interval=self.timeframe, limit=limit)
            if not close_prices:
                iterations_without_data += 1
                if iterations_without_data >= 3:
                    self.log("Demasiados intentos fallidos para obtener datos históricos. Deteniendo el bot.", "error")
                    self.stop()
                    break
                self.log("No se pudieron obtener datos históricos. Reintentando...", "error")
                time.sleep(60)
                continue
            iterations_without_data = 0
            current_price = close_prices[-1]
            self.log(f"Precio actual de {symbol}: {current_price:.2f} USDT")

            account = client.get_account()
            self.usdt_balance = float(next(item for item in account['balances'] if item['asset'] == 'USDT')['free'])
            self.btc_balance = float(next(item for item in account['balances'] if item['asset'] == 'BTC')['free'])
            if self.balance_label:
                self.balance_label.config(text=f"Saldo: {self.usdt_balance:.2f} USDT | {self.btc_balance:.6f} BTC")

            if self.strategy_type == "moving_average":
                fast_period = params["fast_period"]
                slow_period = params["slow_period"]
                current_fast_ma, current_slow_ma = self.calculate_moving_averages(close_prices, fast_period, slow_period)
                if current_fast_ma is None or current_slow_ma is None:
                    self.log("Esperando más datos para calcular las medias móviles...", "info")
                    time.sleep(60)
                    continue

                self.log(f"Fast MA: {current_fast_ma:.2f}, Slow MA: {current_slow_ma:.2f}")
                if previous_fast_ma is not None and previous_slow_ma is not None:
                    if current_fast_ma > current_slow_ma and previous_fast_ma <= previous_slow_ma:
                        if self.usdt_balance >= quantity * current_price:
                            order = client.create_order(
                                symbol=symbol,
                                side=client.SIDE_BUY,
                                type=client.ORDER_TYPE_MARKET,
                                quantity=quantity
                            )
                            self.log(f"Compra ejecutada (MA): {order}")
                            self.update_history(f"Compra: {quantity} BTC a {current_price:.2f} USDT (MA)", strategy="moving_average")
                            notification.notify(
                                title="Señal de Compra",
                                message=f"Compra ejecutada: {quantity} BTC a {current_price:.2f} USDT (MA)",
                                timeout=10
                            )
                            if self.use_gui:
                                messagebox.showinfo("Compra", f"Compra ejecutada: {quantity} BTC")
                        else:
                            self.log("Saldo USDT insuficiente para comprar.", "error")
                    elif current_fast_ma < current_slow_ma and previous_fast_ma >= previous_slow_ma:
                        if self.btc_balance >= quantity:
                            order = client.create_order(
                                symbol=symbol,
                                side=client.SIDE_SELL,
                                type=client.ORDER_TYPE_MARKET,
                                quantity=quantity
                            )
                            self.log(f"Venta ejecutada (MA): {order}")
                            self.update_history(f"Venta: {quantity} BTC a {current_price:.2f} USDT (MA)", strategy="moving_average")
                            notification.notify(
                                title="Señal de Venta",
                                message=f"Venta ejecutada: {quantity} BTC a {current_price:.2f} USDT (MA)",
                                timeout=10
                            )
                            if self.use_gui:
                                messagebox.showinfo("Venta", f"Venta ejecutada: {quantity} BTC")
                        else:
                            self.log("Saldo BTC insuficiente para vender.", "error")
                previous_fast_ma = current_fast_ma
                previous_slow_ma = current_slow_ma

            elif self.strategy_type == "rsi":
                rsi_strategy(self, close_prices, current_price, quantity)

            elif self.strategy_type == "threshold":
                threshold_strategy(self, current_price, quantity, buy_price)
                buy_price = self.buy_price if hasattr(self, 'buy_price') else None

            elif self.strategy_type == "macd":
                fast_length = params["fast_length"]
                slow_length = params["slow_length"]
                signal_length = params["signal_length"]
                macd_line, signal_line, _ = self.calculate_macd(close_prices, fast_length, slow_length, signal_length)
                if macd_line is None or signal_line is None:
                    self.log("Esperando más datos para calcular el MACD...", "info")
                    time.sleep(60)
                    continue

                current_macd = macd_line[-1]
                current_signal = signal_line[-1]
                self.log(f"MACD: {current_macd:.2f}, Signal: {current_signal:.2f}")
                if previous_macd is not None and previous_signal is not None:
                    if current_macd > current_signal and previous_macd <= previous_signal:
                        if self.usdt_balance >= quantity * current_price:
                            order = client.create_order(
                                symbol=symbol,
                                side=client.SIDE_BUY,
                                type=client.ORDER_TYPE_MARKET,
                                quantity=quantity
                            )
                            self.log(f"Compra ejecutada (MACD): {order}")
                            self.update_history(f"Compra: {quantity} BTC a {current_price:.2f} USDT (MACD)", strategy="macd")
                            notification.notify(
                                title="Señal de Compra",
                                message=f"Compra ejecutada: {quantity} BTC a {current_price:.2f} USDT (MACD)",
                                timeout=10
                            )
                            if self.use_gui:
                                messagebox.showinfo("Compra", f"Compra ejecutada: {quantity} BTC")
                        else:
                            self.log("Saldo USDT insuficiente para comprar.", "error")
                    elif current_macd < current_signal and previous_macd >= previous_signal:
                        if self.btc_balance >= quantity:
                            order = client.create_order(
                                symbol=symbol,
                                side=client.SIDE_SELL,
                                type=client.ORDER_TYPE_MARKET,
                                quantity=quantity
                            )
                            self.log(f"Venta ejecutada (MACD): {order}")
                            self.update_history(f"Venta: {quantity} BTC a {current_price:.2f} USDT (MACD)", strategy="macd")
                            notification.notify(
                                title="Señal de Venta",
                                message=f"Venta ejecutada: {quantity} BTC a {current_price:.2f} USDT (MACD)",
                                timeout=10
                            )
                            if self.use_gui:
                                messagebox.showinfo("Venta", f"Venta ejecutada: {quantity} BTC")
                        else:
                            self.log("Saldo BTC insuficiente para vender.", "error")
                previous_macd = current_macd
                previous_signal = current_signal

            elif self.strategy_type == "ma_rsi":
                fast_period = params["fast_period"]
                slow_period = params["slow_period"]
                rsi_period = params["rsi_period"]
                rsi_overbought = params["rsi_overbought"]
                rsi_oversold = params["rsi_oversold"]

                current_fast_ma, current_slow_ma = self.calculate_moving_averages(close_prices, fast_period, slow_period)
                if current_fast_ma is None or current_slow_ma is None:
                    self.log("Esperando más datos para calcular las medias móviles...", "info")
                    time.sleep(60)
                    continue

                rsi = self.calculate_rsi(close_prices, rsi_period)
                if rsi is None:
                    self.log("Esperando más datos para calcular el RSI...", "info")
                    time.sleep(60)
                    continue

                self.log(f"Fast MA: {current_fast_ma:.2f}, Slow MA: {current_slow_ma:.2f}, RSI: {rsi:.2f}")
                if previous_fast_ma is not None and previous_slow_ma is not None and previous_rsi is not None:
                    ma_buy_signal = current_fast_ma > current_slow_ma and previous_fast_ma <= previous_slow_ma
                    ma_sell_signal = current_fast_ma < current_slow_ma and previous_fast_ma >= previous_slow_ma
                    rsi_buy_signal = rsi < rsi_oversold
                    rsi_sell_signal = rsi > rsi_overbought

                    if ma_buy_signal and rsi_buy_signal:
                        if self.usdt_balance >= quantity * current_price:
                            order = client.create_order(
                                symbol=symbol,
                                side=client.SIDE_BUY,
                                type=client.ORDER_TYPE_MARKET,
                                quantity=quantity
                            )
                            self.log(f"Compra ejecutada (MA+RSI): {order}")
                            self.update_history(f"Compra: {quantity} BTC a {current_price:.2f} USDT (MA+RSI)", strategy="ma_rsi")
                            notification.notify(
                                title="Señal de Compra",
                                message=f"Compra ejecutada: {quantity} BTC a {current_price:.2f} USDT (MA+RSI)",
                                timeout=10
                            )
                            if self.use_gui:
                                messagebox.showinfo("Compra", f"Compra ejecutada: {quantity} BTC")
                        else:
                            self.log("Saldo USDT insuficiente para comprar.", "error")
                    elif ma_sell_signal and rsi_sell_signal:
                        if self.btc_balance >= quantity:
                            order = client.create_order(
                                symbol=symbol,
                                side=client.SIDE_SELL,
                                type=client.ORDER_TYPE_MARKET,
                                quantity=quantity
                            )
                            self.log(f"Venta ejecutada (MA+RSI): {order}")
                            self.update_history(f"Venta: {quantity} BTC a {current_price:.2f} USDT (MA+RSI)", strategy="ma_rsi")
                            notification.notify(
                                title="Señal de Venta",
                                message=f"Venta ejecutada: {quantity} BTC a {current_price:.2f} USDT (MA+RSI)",
                                timeout=10
                            )
                            if self.use_gui:
                                messagebox.showinfo("Venta", f"Venta ejecutada: {quantity} BTC")
                        else:
                            self.log("Saldo BTC insuficiente para vender.", "error")
                previous_fast_ma = current_fast_ma
                previous_slow_ma = current_slow_ma
                previous_rsi = rsi

            elif self.strategy_type == "wyckoff":
                wyckoff_strategy(self, close_prices, volumes, current_price, quantity, buy_price)
                buy_price = self.buy_price if hasattr(self, 'buy_price') else None

            if self.status_label:
                status_text = "Estado: Ejecutando" if not self.paused else "Estado: Pausado"
                status_color = self.themes[self.current_theme]["highlight"] if not self.paused else "#FFAA00"
                self.status_label.config(text=status_text, foreground=status_color)

            time.sleep(30)

        except Exception as e:
            self.log(f"Error en la estrategia: {str(e)}", "error")
            if "Timestamp for this request was" in str(e):
                self.log("Timestamp desincronizado. Intentando resincronizar...", "error")
                self.time_difference = sync_time_with_binance()
            time.sleep(60)