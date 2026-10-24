
import re
from decimal import Decimal, InvalidOperation

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) "
        "Gecko/20100101 Firefox/132.0"
    ),
    "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
}

SESSION = requests.Session()
SESSION.headers.update(HEADERS)


def fiyat_parse(metin):
    """Türkçe fiyat metnini Decimal değerine dönüştürür."""
    if not metin:
        return None

    temiz = re.sub(r"[^\d,.]", "", metin.strip())

    if not temiz:
        return None

    # 1.299,90 -> 1299.90
    if "," in temiz:
        temiz = temiz.replace(".", "").replace(",", ".")
    elif temiz.count(".") > 1:
        temiz = temiz.replace(".", "")

    try:
        return Decimal(temiz)
    except InvalidOperation:
        return None


def sayfayi_getir(url, params):
    try:
        response = SESSION.get(
            url,
            params=params,
            timeout=15,
        )
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as hata:
        print(f"Bağlantı hatası: {hata}")
        return None


def trendyol_fiyat(urun_ismi):
    soup = sayfayi_getir(
        "https://www.trendyol.com/sr",
        {"q": urun_ismi},
    )

    if soup is None:
        return None

    # Sayfanın HTML yapısı değişirse fiyat bulunamayabilir.
    for oge in soup.select("span.prc-dsc"):
        fiyat = fiyat_parse(oge.get_text(" ", strip=True))
        if fiyat is not None:
            return fiyat

    return None


def amazon_fiyat(urun_ismi):
    soup = sayfayi_getir(
        "https://www.amazon.com.tr/s",
        {"k": urun_ismi},
    )

    if soup is None:
        return None

    # Amazon fiyatları bazen tam ve küsurat kısmında ayrıdır.
    for oge in soup.select("span.a-price"):
        tam = oge.select_one("span.a-price-whole")
        kurus = oge.select_one("span.a-price-fraction")

        if tam is None:
            continue

        tam_metin = tam.get_text(strip=True)
        kurus_metin = kurus.get_text(strip=True) if kurus else "00"

        fiyat = fiyat_parse(f"{tam_metin},{kurus_metin}")

        if fiyat is not None:
            return fiyat

    return None


def main():
    urun_ismi = input("Aranacak ürünü girin: ").strip()

    if not urun_ismi:
        print("Ürün adı boş olamaz.")
        return

    print("\nFiyatlar aranıyor...\n")

    fiyatlar = {
        "Trendyol": trendyol_fiyat(urun_ismi),
        "Amazon Türkiye": amazon_fiyat(urun_ismi),
    }

    for site, fiyat in fiyatlar.items():
        if fiyat is not None:
            print(f"{site}: {fiyat:,.2f} TL".replace(",", "X")
                  .replace(".", ",").replace("X", "."))
        else:
            print(f"{site}: Fiyat bulunamadı.")

    trendyol = fiyatlar["Trendyol"]
    amazon = fiyatlar["Amazon Türkiye"]

    if trendyol is not None and amazon is not None:
        print()

        if trendyol < amazon:
            print(f"Trendyol {amazon - trendyol:.2f} TL daha ucuz.")
        elif amazon < trendyol:
            print(f"Amazon Türkiye {trendyol - amazon:.2f} TL daha ucuz.")
        else:
            print("İki sitedeki fiyatlar eşit.")

    print(
        "\nNot: İlk bulunan fiyatlar aynı ürün ve varyant olmayabilir. "
        "Satıcı, kargo ve ürün özelliklerini kontrol et."
    )


if __name__ == "__main__":
    main()
