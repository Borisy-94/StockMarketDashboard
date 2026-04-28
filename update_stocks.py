# ============================================
# STOCK MARKET LIVE DASHBOARD
# Automatische Aktualisierung
# ============================================

import subprocess
import sys
import os
from datetime import datetime

def log(text):
    zeit = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    print(f"[{zeit}] {text}")

# ── Wichtig: Richtiger Pfad ──────────────────
# Ordner wo update_stocks.py liegt
BASIS_PFAD = os.path.dirname(os.path.abspath(__file__))

# Pfade zu den Scripts
FETCH_SCRIPT = os.path.join(BASIS_PFAD, "fetch_stocks.py")
CLEAN_SCRIPT = os.path.join(BASIS_PFAD, "clean_stocks.py")

log("🔄 Automatische Aktualisierung startet...")
log(f"📁 Basis-Pfad: {BASIS_PFAD}")

# ── Schritt 1: Daten holen ───────────────────
log("📥 Starte fetch_stocks.py...")
try:
    subprocess.run(
        [sys.executable, FETCH_SCRIPT],
        check=True,
        cwd=os.path.dirname(BASIS_PFAD)
    )
    log("✅ fetch_stocks.py erfolgreich!")
except Exception as e:
    log(f"❌ Fehler: {e}")
    sys.exit(1)

# ── Schritt 2: Daten bereinigen ──────────────
log("🧹 Starte clean_stocks.py...")
try:
    subprocess.run(
        [sys.executable, CLEAN_SCRIPT],
        check=True,
        cwd=os.path.dirname(BASIS_PFAD)
    )
    log("✅ clean_stocks.py erfolgreich!")
except Exception as e:
    log(f"❌ Fehler: {e}")
    sys.exit(1)

# ── Fertig ───────────────────────────────────
log("=" * 50)
log("✅ AKTUALISIERUNG ABGESCHLOSSEN!")
log("📊 Power BI kann jetzt aktualisiert werden")
log("=" * 50)