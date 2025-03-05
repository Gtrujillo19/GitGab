#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from config import client
from plyer import notification
from tkinter import messagebox

def wyckoff_strategy(self, close_prices, volumes, current_price, quantity, buy_price):
    params = self.strategy_params["wyckoff"]
    support_level = params["support_level"]
    resistance_level = params["resistance_level"]
    volume_threshold = params["volume_threshold"]
    stop_loss_percent = params["stop_loss_percent"]

    average_volume = sum(volumes[:-1]) / (len(volumes) - 1) if len(volumes) > 1 else 0
    current_volume = volumes[-1]

    volume_increase = current_volume > average_volume * volume_threshold if average_volume > 0 else False
    accumulation = current_price <= support_level and volume_increase
    distribution = current_price >= resistance_level and volume_increase

    self.log(f"Precio actual: {current_price:.2f}, Soporte: {support_level:.2f}, Resistencia: {resistance_level:.2f}, Volumen: {current_volume:.2f}, Volumen Promedio: {average_volume:.2f}")
    if accumulation and self.usdt_balance >= quantity * current_price:
        order = client.create_order(
            symbol=self.SYMBOL,
            side=client.SIDE_BUY,
            type=client.ORDER_TYPE_MARKET,
            quantity=quantity
        )
        self.buy_price = current_price
        self.log(f"Compra ejecutada (Wyckoff - Acumulación): {order}")
        self.update_history(f"Compra: {quantity} BTC a {current_price:.2f} USDT (Wyckoff)", strategy="wyckoff")
        notification.notify(
            title="Señal de Compra",
            message=f"Compra ejecutada: {quantity} BTC a {current_price:.2f} USDT (Wyckoff - Acumulación)",
            timeout=10
        )
        if self.use_gui:
            messagebox.showinfo("Compra", f"Compra ejecutada: {quantity} BTC")
    elif distribution and self.btc_balance >= quantity:
        order = client.create_order(
            symbol=self.SYMBOL,
            side=client.SIDE_SELL,
            type=client.ORDER_TYPE_MARKET,
            quantity=quantity
        )
        self.buy_price = None
        self.log(f"Venta ejecutada (Wyckoff - Distribución): {order}")
        self.update_history(f"Venta: {quantity} BTC a {current_price:.2f} USDT (Wyckoff)", strategy="wyckoff")
        notification.notify(
            title="Señal de Venta",
            message=f"Venta ejecutada: {quantity} BTC a {current_price:.2f} USDT (Wyckoff - Distribución)",
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
        self.log(f"Stop-loss ejecutado (Wyckoff): {order}")
        self.update_history(f"Stop-loss: {quantity} BTC a {current_price:.2f} USDT (Wyckoff)", strategy="wyckoff")
        notification.notify(
            title="Stop-loss",
            message=f"Stop-loss ejecutado: {quantity} BTC a {current_price:.2f} USDT (Wyckoff)",
            timeout=10
        )
        if self.use_gui:
            messagebox.showinfo("Stop-loss", f"Stop-loss ejecutado: {quantity} BTC")
