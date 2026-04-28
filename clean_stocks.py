# ============================================
# STOCK MARKET LIVE DASHBOARD
# Schritt 2: Daten bereinigen & aufbereiten
# ============================================

import pandas as pd
from datetime import datetime

print("🧹 Datenbereinigung startet...")

# ── Daten laden ──────────────────────────────
kurse   = pd.read_csv("data/stocks_aktuell.csv")
verlauf = pd.read_csv("data/stocks_verlauf.csv")

print(f"📥 Aktuell geladen:  {len(kurse)} Aktien")
print(f"📥 Verlauf geladen:  {len(verlauf)} Zeilen")

# ── Bereinigung: Aktuell ─────────────────────

# Emojis aus Status entfernen (Power BI mag keine Emojis)
kurse["Status"] = kurse["Status"].str.replace("📈 ", "", regex=False)
kurse["Status"] = kurse["Status"].str.replace("📉 ", "", regex=False)
kurse["Status"] = kurse["Status"].str.replace("➡️ ", "", regex=False)

# Emojis aus Firmenname entfernen
kurse["Firma"] = kurse["Firma"].str.replace("🍎 ", "", regex=False)
kurse["Firma"] = kurse["Firma"].str.replace("🪟 ", "", regex=False)
kurse["Firma"] = kurse["Firma"].str.replace("🚗 ", "", regex=False)
kurse["Firma"] = kurse["Firma"].str.replace("🔍 ", "", regex=False)
kurse["Firma"] = kurse["Firma"].str.replace("📦 ", "", regex=False)
kurse["Firma"] = kurse["Firma"].str.replace("👤 ", "", regex=False)
kurse["Firma"] = kurse["Firma"].str.replace("🎮 ", "", regex=False)
kurse["Firma"] = kurse["Firma"].str.replace("🎬 ", "", regex=False)
kurse["Firma"] = kurse["Firma"].str.replace("🛒 ", "", regex=False)
kurse["Firma"] = kurse["Firma"].str.replace("🎨 ", "", regex=False)

# Fehlende Werte mit 0 füllen
kurse = kurse.fillna(0)

# Neue Spalte: Kurs-Kategorie
def kategorisiere(prozent):
    if prozent >= 3:
        return "Stark positiv"
    elif prozent >= 1:
        return "Positiv"
    elif prozent >= -1:
        return "Neutral"
    elif prozent >= -3:
        return "Negativ"
    else:
        return "Stark negativ"

kurse["Kategorie"] = kurse["Veraenderung_Prozent"].apply(kategorisiere)

# ── Bereinigung: Verlauf ─────────────────────

# Zeit-Spalte bereinigen
verlauf["Zeit"] = pd.to_datetime(verlauf["Zeit"], utc=True)
verlauf["Zeit"] = verlauf["Zeit"].dt.tz_localize(None)  # Zeitzone entfernen
verlauf["Datum"] = verlauf["Zeit"].dt.strftime("%d.%m.%Y")
verlauf["Uhrzeit"] = verlauf["Zeit"].dt.strftime("%H:%M")

# Emojis aus Firma entfernen
for emoji in ["🍎 ", "🪟 ", "🚗 ", "🔍 ", "📦 ", "👤 ", "🎮 ", "🎬 ", "🛒 ", "🎨 "]:
    verlauf["Firma"] = verlauf["Firma"].str.replace(emoji, "", regex=False)

# Fehlende Werte entfernen
verlauf = verlauf.dropna(subset=["Kurs_USD"])
verlauf["Kurs_USD"] = verlauf["Kurs_USD"].round(2)

# ── Speichern ────────────────────────────────
kurse.to_csv("data/stocks_sauber.csv",
             index=False, encoding="utf-8-sig")
verlauf.to_csv("data/stocks_verlauf_sauber.csv",
               index=False, encoding="utf-8-sig")

# ── Zusammenfassung ──────────────────────────
print("")
print("=" * 50)
print("✅ BEREINIGUNG ABGESCHLOSSEN!")
print("=" * 50)
print(f"📊 Aktien verarbeitet: {len(kurse)}")
print(f"📈 Gewinner:           {len(kurse[kurse['Status'] == 'Gewinner'])}")
print(f"📉 Verlierer:          {len(kurse[kurse['Status'] == 'Verlierer'])}")
print(f"📁 Aktuell:            data/stocks_sauber.csv")
print(f"📁 Verlauf:            data/stocks_verlauf_sauber.csv")
print("=" * 50)

# ── Vorschau ─────────────────────────────────
print("\n📋 Aktuelle Kurse:")
print(kurse[["Firma", "Kurs_USD", "Veraenderung_Prozent",
             "Status", "Kategorie"]].to_string(index=False))