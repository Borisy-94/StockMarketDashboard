# ============================================
# STOCK MARKET LIVE DASHBOARD
# Schritt 1: Aktuelle Börsenkurse holen
# ============================================

import yfinance as yf
import pandas as pd
from datetime import datetime

print("📈 Stock Market Dashboard startet...")
print("⏳ Verbinde mit Yahoo Finance...")
print("")

# ── Unsere 10 Aktien ─────────────────────────
aktien = {
    "AAPL":  "🍎 Apple",
    "MSFT":  "🪟 Microsoft",
    "TSLA":  "🚗 Tesla",
    "GOOGL": "🔍 Google",
    "AMZN":  "📦 Amazon",
    "META":  "👤 Meta",
    "NVDA":  "🎮 Nvidia",
    "NFLX":  "🎬 Netflix",
    "BABA":  "🛒 Alibaba",
    "ADBE":  "🎨 Adobe"
}

# ── Funktion: Daten für eine Aktie holen ─────
def hole_aktie(kuerzel, name):
    try:
        # Aktie von Yahoo Finance holen
        ticker = yf.Ticker(kuerzel)
        info   = ticker.info

        # Kursverlauf der letzten 7 Tage (stündlich)
        verlauf = ticker.history(period="7d", interval="1h")

        # Aktuellen Kurs & Informationen
        aktuell = {
            "Kuerzel":            kuerzel,
            "Firma":              name,
            "Kurs_USD":           info.get("currentPrice",  0),
            "Vortag_USD":         info.get("previousClose", 0),
            "Hoch_heute_USD":     info.get("dayHigh",       0),
            "Tief_heute_USD":     info.get("dayLow",        0),
            "Marktkapital_Mrd":   round(info.get("marketCap", 0) / 1_000_000_000, 2),
            "Volumen":            info.get("volume",        0),
            "52W_Hoch_USD":       info.get("fiftyTwoWeekHigh", 0),
            "52W_Tief_USD":       info.get("fiftyTwoWeekLow",  0),
            "Letzte_Aktualisierung": datetime.now().strftime("%d.%m.%Y %H:%M")
        }

        # Veränderung in % berechnen
        if aktuell["Vortag_USD"] > 0:
            aktuell["Veraenderung_Prozent"] = round(
                ((aktuell["Kurs_USD"] - aktuell["Vortag_USD"])
                 / aktuell["Vortag_USD"]) * 100, 2
            )
        else:
            aktuell["Veraenderung_Prozent"] = 0

        # Gewinner oder Verlierer?
        if aktuell["Veraenderung_Prozent"] > 0:
            aktuell["Status"] = "📈 Gewinner"
            trend = f"+{aktuell['Veraenderung_Prozent']}%"
        elif aktuell["Veraenderung_Prozent"] < 0:
            aktuell["Status"] = "📉 Verlierer"
            trend = f"{aktuell['Veraenderung_Prozent']}%"
        else:
            aktuell["Status"] = "➡️ Neutral"
            trend = "0%"

        print(f"   ✅ {name}: {aktuell['Kurs_USD']}$ ({trend})")

        return pd.DataFrame([aktuell]), verlauf

    except Exception as e:
        print(f"   ❌ Fehler bei {name}: {e}")
        return None, None

# ── Alle 10 Aktien abrufen ───────────────────
alle_kurse    = []
alle_verlaeufe = []

for kuerzel, name in aktien.items():
    kurse_df, verlauf_df = hole_aktie(kuerzel, name)

    if kurse_df is not None:
        alle_kurse.append(kurse_df)

    if verlauf_df is not None and not verlauf_df.empty:
        verlauf_df["Kuerzel"] = kuerzel
        verlauf_df["Firma"]   = name
        verlauf_df = verlauf_df.reset_index()
        verlauf_df = verlauf_df[["Datetime", "Kuerzel",
                                  "Firma", "Close", "Volume"]]
        verlauf_df.columns = ["Zeit", "Kuerzel",
                               "Firma", "Kurs_USD", "Volumen"]
        alle_verlaeufe.append(verlauf_df)

# ── Alles zusammenfügen ──────────────────────
kurse_gesamt   = pd.concat(alle_kurse,     ignore_index=True)
verlauf_gesamt = pd.concat(alle_verlaeufe, ignore_index=True)

# ── Als CSV speichern ────────────────────────
kurse_gesamt.to_csv(
    "data/stocks_aktuell.csv",   index=False, encoding="utf-8-sig")
verlauf_gesamt.to_csv(
    "data/stocks_verlauf.csv",   index=False, encoding="utf-8-sig")

# ── Zusammenfassung ──────────────────────────
print("")
print("=" * 50)
print("✅ FERTIG! Hier die Zusammenfassung:")
print("=" * 50)

gewinner  = kurse_gesamt[kurse_gesamt["Status"] == "📈 Gewinner"]
verlierer = kurse_gesamt[kurse_gesamt["Status"] == "📉 Verlierer"]

print(f"📈 Gewinner heute:  {len(gewinner)} Aktien")
print(f"📉 Verlierer heute: {len(verlierer)} Aktien")
print(f"💾 Gespeichert:     data/stocks_aktuell.csv")
print(f"📊 Kursverlauf:     data/stocks_verlauf.csv")
print(f"🕐 Stand:           {datetime.now().strftime('%d.%m.%Y %H:%M')}")
print("=" * 50)
print("")
print("🏆 Top Performer:")
top = kurse_gesamt.nlargest(3, "Veraenderung_Prozent")
for _, row in top.iterrows():
    print(f"   {row['Firma']}: {row['Kurs_USD']}$ "
          f"(+{row['Veraenderung_Prozent']}%)")