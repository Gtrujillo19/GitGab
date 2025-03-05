#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import requests
import numpy as np

def sync_time_with_binance():
    try:
        response = requests.get("https://api.binance.com/api/v3/time")
        response.raise_for_status()
        server_time = response.json()["serverTime"]
        local_time = int(time.time() * 1000)
        time_difference = server_time - local_time
        import logging
        logging.info(f"Sincronización de tiempo: diferencia de {time_difference} ms con el servidor de Binance.")
        return time_difference
    except Exception as e:
        import logging
        logging.error(f"Error al sincronizar el tiempo con el servidor: {str(e)}")
        return 0

def calculate_ema(prices, period, log):
    try:
        if len(prices) < period:
            return None
        alpha = 2 / (period + 1)
        ema = []
        sma = sum(prices[:period]) / period
        ema.append(sma)
        for price in prices[period:]:
            ema.append(alpha * price + (1 - alpha) * ema[-1])
        return ema
    except Exception as e:
        log(f"Error al calcular EMA: {str(e)}", "error")
        return None

def calculate_moving_averages(close_prices, fast_period, slow_period, log):
    try:
        if len(close_prices) < slow_period:
            log(f"No hay suficientes datos para calcular las medias móviles (se necesitan {slow_period}, se tienen {len(close_prices)}).", "error")
            return None, None
        fast_data = close_prices[-fast_period:]
        slow_data = close_prices[-slow_period:]
        fast_ma = sum(fast_data) / len(fast_data)
        slow_ma = sum(slow_data) / len(slow_data)
        return fast_ma, slow_ma
    except Exception as e:
        log(f"Error al calcular medias móviles: {str(e)}", "error")
        return None, None

def calculate_rsi(close_prices, period, log):
    try:
        if len(close_prices) < period + 1:
            log(f"No hay suficientes datos para calcular el RSI (se necesitan {period + 1}, se tienen {len(close_prices)}).", "error")
            return None
        changes = [(close_prices[i] - close_prices[i-1]) for i in range(1, len(close_prices))]
        gains = []
        losses = []
        for change in changes[-period:]:
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))
        avg_gain = sum(gains) / period if gains else 0
        avg_loss = sum(losses) / period if losses else 0.0001
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    except Exception as e:
        log(f"Error al calcular RSI: {str(e)}", "error")
        return None

def calculate_macd(close_prices, fast_length, slow_length, signal_length, log):
    try:
        if len(close_prices) < slow_length + signal_length:
            log(f"No hay suficientes datos para calcular el MACD (se necesitan {slow_length + signal_length}, se tienen {len(close_prices)}).", "error")
            return None, None, None

        fast_ema = calculate_ema(close_prices, fast_length, log)
        slow_ema = calculate_ema(close_prices, slow_length, log)

        if fast_ema is None or slow_ema is None:
            return None, None, None

        macd_line = [fast - slow for fast, slow in zip(fast_ema, slow_ema)]
        signal_line = calculate_ema(macd_line, signal_length, log)

        if signal_line is None:
            return None, None, None

        histogram = [macd - signal for macd, signal in zip(macd_line[-len(signal_line):], signal_line)]

        return macd_line[-len(signal_line):], signal_line, histogram
    except Exception as e:
        log(f"Error al calcular MACD: {str(e)}", "error")
        return None, None, None
