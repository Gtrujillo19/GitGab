#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from config import client
from plyer import notification
from tkinter import messagebox
import time

def rsi_strategy(self, close_prices, current_price, quantity):
    params = self.strategy_params["rsi"]
    rsi_period = params["rsi_period"]
    rsi_overbought = params["rsi_overbought"]
    rsi_oversold = params["rsi_oversold"]
    rsi = self.calculate_rsi(close_prices, rsi_period)
    if rsi is None:
        self.log("Esperando más datos para calcular el RSI...", "info")
        time.sleep(60)
        return

    self.log(f"RSI: {rsi:.2f}")
    if rsi < rsi_oversold:
        if self.usdt_balance >= quantity * current_price:
            order = client.create_order(
                symbol=self.SYMBOL,
                side=client.SIDE_BUY,
                type=client.ORDER_TYPE_MARKET,
                quantity=quantity
            )
            self.log(f"Compra ejecutada (RSI={rsi:.2f}): {order}")
            self.update_history(f"Compra: {quantity} BTC a {current_price:.2f} USDT (RSI={rsi:.2f})", strategy="rsi")
            notification.notify(
                title="Señal de Compra",
                message=f"Compra ejecutada: {quantity} BTC a {current_price:.2f} USDT (RSI={rsi:.2f})",
                timeout=10
            )
            if self.use_gui:
                messagebox.showinfo("Compra", f"Compra ejecutada: {quantity} BTC")
        else:
            self.log("Saldo USDT insuficiente para comprar.", "error")
    elif rsi > rsi_overbought:
        if self.btc_balance >= quantity:
            order = client.create_order(
                symbol=self.SYMBOL,
                side=client.SIDE_SELL,
                type=client.ORDER_TYPE_MARKET,
                quantity=quantity
            )
            self.log(f"Venta ejecutada (RSI={rsi:.2f}): {order}")
            self.update_history(f"Venta: {quantity} BTC a {current_price:.2f} USDT (RSI={rsi:.2f})", strategy="rsi")
            notification.notify(
                title="Señal de Venta",
                message=f"Venta ejecutada: {quantity} BTC a {current_price:.2f} USDT (RSI={rsi:.2f})",
                timeout=10
            )
            if self.use_gui:
                messagebox.showinfo("Venta", f"Venta ejecutada: {quantity} BTC")
        else:
            self.log("Saldo BTC insuficiente para vender.", "error")
