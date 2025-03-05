#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from config import client
from plyer import notification
from tkinter import messagebox

def threshold_strategy(self, current_price, quantity, buy_price):
    params = self.strategy_params["threshold"]
    support_level = params["support_level"]
    resistance_level = params["resistance_level"]
    stop_loss_percent = params["stop_loss_percent"]
    self.log(f"Precio actual: {current_price:.2f}, Soporte: {support_level:.2f}, Resistencia: {resistance_level:.2f}")
    if current_price <= support_level and self.usdt_balance >= quantity * current_price:
        order = client.create_order(
            symbol=self.SYMBOL,
            side=client.SIDE_BUY,
            type=client.ORDER_TYPE_MARKET,
            quantity=quantity
        )
        self.buy_price = current_price
        self.log(f"Compra ejecutada (Precio={current_price:.2f}): {order}")
        self.update_history(f"Compra: {quantity} BTC a {current_price:.2f} USDT", strategy="threshold")
        notification.notify(
            title="Señal de Compra",
            message=f"Compra ejecutada: {quantity} BTC a {current_price:.2f} USDT (Threshold)",
            timeout=10
        )
        if self.use_gui:
            messagebox.showinfo("Compra", f"Compra ejecutada: {quantity} BTC")
    elif current_price >= resistance_level and self.btc_balance >= quantity:
        order = client.create_order(
            symbol=self.SYMBOL,
            side=client.SIDE_SELL,
            type=client.ORDER_TYPE_MARKET,
            quantity=quantity
        )
        self.buy_price = None
        self.log(f"Venta ejecutada (Precio={current_price:.2f}): {order}")
        self.update_history(f"Venta: {quantity} BTC a {current_price:.2f} USDT", strategy="threshold")
        notification.notify(
            title="Señal de Venta",
            message=f"Venta ejecutada: {quantity} BTC a {current_price:.2f} USDT (Threshold)",
            timeout=10
        )
        if self.use_gui:
            messagebox.showinfo("Venta", f"Venta ejecutada: {quantity} BTC")
    elif buy_price is not None and current_price <= buy_price * (1 - stop_loss_percent) and self.btc_balance >= quantity:
        order = client.create_order(
            symbol=self.SYMBOL,
            side=client.SIDE_SELL,
            type=client.ORDER_TYPE_MARKET,
            quantity=quantity
        )
        self.buy_price = None
        self.log(f"Stop-loss ejecutado (Precio={current_price:.2f}): {order}")
        self.update_history(f"Stop-loss: {quantity} BTC a {current_price:.2f} USDT", strategy="threshold")
        notification.notify(
            title="Stop-loss",
            message=f"Stop-loss ejecutado: {quantity} BTC a {current_price:.2f} USDT",
            timeout=10
        )
        if self.use_gui:
            messagebox.showinfo("Stop-loss", f"Stop-loss ejecutado: {quantity} BTC")
