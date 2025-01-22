# regression/regression.py
#
# Opis: Plik zawiera funkcje do analizy regresji i wizualizacji danych.
# Autorzy: Michał Miler, Magdalena Różycka, Szymon Kosz
# Data: 22.01.2025

import os
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


# Definicja funkcji wykładniczej
def exponential_func(x, a, b):
    return a * np.exp(-b * x)


# Funkcja do formatowania równania wielomianowego
def format_poly_eq(coeffs):
    terms = []
    for i, coeff in enumerate(coeffs):
        power = len(coeffs) - i - 1
        if power == 0:
            terms.append(f"{coeff:.4e}")
        elif power == 1:
            terms.append(f"{coeff:.4e}x")
        else:
            terms.append(f"{coeff:.4e}x^{power}")
        if i % 2 == 1 and i != len(coeffs) - 1:
            terms.append("\n                       ")
    return " + ".join(terms)


# Główna funkcja programu
def main():
    # Ustawienie globalnych parametrów czcionki
    plt.rc("font", size=16)

    # Pobierz ścieżkę bieżącego skryptu
    current_path = os.path.dirname(os.path.abspath(__file__))

    # Skonstruuj ścieżkę do pliku data.csv
    data_file = os.path.join(current_path, "data.csv")

    # Wczytaj dane z pliku CSV
    data = pd.read_csv(data_file)

    # Wyodrębnij x (pixel) i y (distance)
    x = data["pixel"].values
    y = data["distance"].values

    # Dopasowanie wykładnicze
    initial_guesses = [300, 0.01]
    params, covariance = curve_fit(exponential_func, x, y, p0=initial_guesses)
    a, b = params
    print(f"Dopasowane równanie wykładnicze: y = {a:.4f} * exp(-{b:.4f} * x)")

    # Generuj punkty dla dopasowanej krzywej wykładniczej
    x_fit = np.linspace(0, 640, 640)
    y_fit_exp = exponential_func(x_fit, a, b)

    # Oblicz współczynnik determinacji R^2 dla dopasowania wykładniczego
    residuals_exp = y - exponential_func(x, a, b)
    ss_res_exp = np.sum(residuals_exp**2)
    ss_tot_exp = np.sum((y - np.mean(y)) ** 2)
    r_squared_exp = 1 - (ss_res_exp / ss_tot_exp)

    # Dopasowanie wielomianowe
    degree = 6  # Możliwość wyboru stopnia wielomianu
    poly_coeffs = np.polyfit(x, y, degree)
    poly_func = np.poly1d(poly_coeffs)
    y_fit_poly = poly_func(x_fit)
    print(f"Dopasowane równanie wielomianowe: {poly_func}")

    # Oblicz współczynnik determinacji R^2 dla dopasowania wielomianowego
    residuals_poly = y - poly_func(x)
    ss_res_poly = np.sum(residuals_poly**2)
    ss_tot_poly = np.sum((y - np.mean(y)) ** 2)
    r_squared_poly = 1 - (ss_res_poly / ss_tot_poly)

    # Rozmiar wykresu w centymetrach (konwersja na cale)
    width_cm = 30  # szerokość w cm
    height_cm = 15  # wysokość w cm
    width_in = width_cm / 2.54
    height_in = height_cm / 2.54

    # Wykres danych i dopasowania
    fig1, axs1 = plt.subplots(1, 2, figsize=(width_in, height_in))

    # Wykres wykładniczy
    axs1[0].scatter(x, y, label="Dane")
    axs1[0].plot(x_fit, y_fit_exp, color="red", label="Dopasowana funkcja wykładnicza")
    axs1[0].set_xlabel("Pixel [-]")
    axs1[0].set_ylabel("Odległość [cm]")
    axs1[0].legend(loc="upper right", fontsize=12)
    axs1[0].set_title("Dopasowanie wykładnicze")
    axs1[0].set_xlim(0, 650)
    axs1[0].set_ylim(0, 300)

    # Zamiast fig1.figtext() używamy plt.figtext()
    plt.figtext(
        0.2,  # Pozycja w układzie współrzędnych figury
        0.5,
        f"Równanie: y = {a:.4e} * exp(-{b:.4e} * x)\n\nR^2 = {r_squared_exp:.4f}",
        ha="left",
        va="center",
        fontsize=12,
    )

    # Wykres wielomianowy
    axs1[1].scatter(x, y, label="Dane")
    axs1[1].plot(
        x_fit,
        y_fit_poly,
        color="blue",
        label=f"Dopasowana funkcja wielomianowa (stopień {degree})",
    )
    axs1[1].set_xlabel("Pixel [-]")
    axs1[1].set_ylabel("Odległość [cm]")
    axs1[1].legend(loc="upper right", fontsize=12)
    axs1[1].set_title("Dopasowanie wielomianowe")
    axs1[1].set_xlim(0, 650)
    axs1[1].set_ylim(0, 300)

    # Zamiast fig1.figtext() używamy plt.figtext() dla drugiego wykresu
    plt.figtext(
        0.7,  # Pozycja w układzie współrzędnych figury
        0.5,
        f"Równanie: y = {format_poly_eq(poly_coeffs)}\n\nR^2 = {r_squared_poly:.4f}",
        ha="left",
        va="center",
        fontsize=12,
    )

    fig1.tight_layout(pad=2.0)
    plt.show()

    # Wykres punktów pomiarowych
    fig2, axs2 = plt.subplots(1, 2, figsize=(width_in, height_in))

    axs2[0].scatter(x, y, label="Dane")
    axs2[0].set_xlabel("Pixel [-]")
    axs2[0].set_ylabel("Odległość [cm]")
    axs2[0].set_title("Punkty pomiarowe")
    axs2[0].set_xlim(0, 650)
    axs2[0].set_ylim(0, 300)
    axs2[0].legend(loc="upper right", fontsize=12)

    axs2[1].scatter(x, y, label="Dane")
    axs2[1].set_xlabel("Pixel [-]")
    axs2[1].set_ylabel("Odległość [cm]")
    axs2[1].set_title("Punkty pomiarowe")
    axs2[1].set_xlim(0, 650)
    axs2[1].set_ylim(0, 300)
    axs2[1].legend(loc="upper right", fontsize=12)

    fig2.tight_layout(pad=2.0)
    plt.show()


if __name__ == "__main__":
    main()
