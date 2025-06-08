# utils.py
def to_rupiah(x):
    return f"Rp {x:,.0f}".replace(",", ".")

def terbilang(n):
    angka = ["", "satu", "dua", "tiga", "empat", "lima",
             "enam", "tujuh", "delapan", "sembilan", "sepuluh", "sebelas"]
    if n < 12:
        return angka[n]
    elif n < 20:
        return terbilang(n - 10) + " belas"
    elif n < 100:
        return terbilang(n // 10) + " puluh " + terbilang(n % 10)
    elif n < 200:
        return "seratus " + terbilang(n - 100)
    elif n < 1000:
        return terbilang(n // 100) + " ratus " + terbilang(n % 100)
    elif n < 2000:
        return "seribu " + terbilang(n - 1000)
    elif n < 1000000:
        return terbilang(n // 1000) + " ribu " + terbilang(n % 1000)
    elif n < 1000000000:
        return terbilang(n // 1000000) + " juta " + terbilang(n % 1000000)
    else:
        return "terlalu besar"
