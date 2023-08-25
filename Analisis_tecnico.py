import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
import ta
import yfinance as yf
import datetime

def show_graph():
    selected_ticker = ticker_combobox.get()
    
    # Obtener datos históricos de Yahoo Finance
    ticker = selected_ticker  
    end_date = datetime.datetime.now().strftime('%Y-%m-%d')  # Fecha actual
    start_date = (datetime.datetime.now() - datetime.timedelta(days=2*365)).strftime('%Y-%m-%d')  # 2 años atrás
    df = yf.download(ticker, start=start_date, end=end_date)

    # Calculando indicadores técnicos
    # RSI
    df['RSI'] = ta.momentum.RSIIndicator(df['Close']).rsi()

    # MACD
    macd = ta.trend.MACD(df['Close'])
    df['MACD'] = macd.macd()
    df['MACD_signal'] = macd.macd_signal()

    # Moving Averages
    df['SMA_5'] = df['Close'].rolling(window=5).mean()
    df['SMA_10'] = df['Close'].rolling(window=10).mean()

    # Calculando Pivot Points
    pivot = df['Close'].iloc[-1]
    high = df['High'].max()
    low = df['Low'].min()

    s1 = 2 * pivot - high
    s2 = pivot - (high - low)
    s3 = low - 2 * (high - pivot)

    r1 = 2 * pivot - low
    r2 = pivot + (high - low)
    r3 = high + 2 * (pivot - low)

    # Plotting
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(10, 10), sharex=True)

    # Precio de cierre, promedios móviles y Pivot Points
    axes[0].plot(df.index, df['Close'], label='Close Price', color='blue')
    axes[0].plot(df.index, df['SMA_5'], label='5-Day SMA', color='green')
    axes[0].plot(df.index, df['SMA_10'], label='10-Day SMA', color='red')
    axes[0].axhline(s1, color='lightcoral', linestyle='--', label='S1')
    axes[0].axhline(s2, color='firebrick', linestyle='--', label='S2')
    axes[0].axhline(s3, color='darkred', linestyle='--', label='S3')
    axes[0].axhline(r1, color='lightgreen', linestyle='--', label='R1')
    axes[0].axhline(r2, color='forestgreen', linestyle='--', label='R2')
    axes[0].axhline(r3, color='darkgreen', linestyle='--', label='R3')
    axes[0].set_title(f'{selected_ticker} Close Price, Moving Averages, and Pivot Points')
    axes[0].legend()

    # RSI
    axes[1].plot(df.index, df['RSI'], label='RSI', color='purple')
    axes[1].axhline(70, color='red', linestyle='--')
    axes[1].axhline(30, color='green', linestyle='--')
    axes[1].set_title(f'{selected_ticker} Relative Strength Index (RSI)')
    axes[1].legend()

    # MACD
    axes[2].plot(df.index, df['MACD'], label='MACD', color='black')
    axes[2].plot(df.index, df['MACD_signal'], label='Signal Line', color='orange')
    axes[2].set_title(f'{selected_ticker} Moving Average Convergence Divergence (MACD)')
    axes[2].legend()

    plt.tight_layout()
    plt.show()

# Crea la ventana principal
root = tk.Tk()
root.title("Selecciona un instrumento y grafica")

# Añade una etiqueta
label = tk.Label(root, text="Selecciona un instrumento:")
label.pack(pady=10)

# Crea un menú desplegable (Combobox) con algunos tickers de ejemplo
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "FB", "BRK-A", "V", "JPM", "JNJ"]  # Puedes expandir esta lista
ticker_combobox = ttk.Combobox(root, values=tickers)
ticker_combobox.pack(pady=10)
ticker_combobox.set("CSCO")  # Valor por defecto

# Añade un botón para obtener datos y mostrar el gráfico
plot_button = tk.Button(root, text="Mostrar gráfico", command=show_graph)
plot_button.pack(pady=20)

root.mainloop()
