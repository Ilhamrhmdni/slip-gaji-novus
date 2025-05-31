# utils.py
from num2words import num2words

def format_rupiah(angka):
    return f"Rp {angka:,.0f}".replace(",", ".")

def terbilang_rupiah(angka):
    return num2words(angka, lang='id').capitalize() + " rupiah"
