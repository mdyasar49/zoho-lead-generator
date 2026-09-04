"""
================================================================================
🚀 MASTER RUNNER: ODOO & ZOHO SALES EXECUTIVE LEAD GENERATORS
================================================================================
Targets:
  1. Odoo Sales Executive Leads  -> Google Sheet 1 (1X_8LbsHisyvoCfjSuTX5yRVsRgXPDEmu3W5RWXuAC1o)
  2. Zoho Sales Executive Leads  -> Google Sheet 2 (18oHqPuo6BhAgI5e_GLSSps5fSc_DpzYEYofgPKxBv9o)
================================================================================
"""

import sys
import subprocess

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def main():
    print("=" * 80)
    print("🚀 STARTING UNIFIED LEAD GENERATION PIPELINE (ODOO & ZOHO)")
    print("=" * 80)

    print("\n[1/2] Executing Live Odoo Sales Executive Lead Generator...")
    res_odoo = subprocess.run([sys.executable, "live_odoo_partner_tn_india_scraper.py"])
    if res_odoo.returncode == 0:
        print("[✓] Odoo Lead Generator Completed Successfully!")

    print("\n[2/2] Executing Live Zoho Sales Executive Lead Generator...")
    res_zoho = subprocess.run([sys.executable, "live_zoho_partner_tn_india_scraper.py"])
    if res_zoho.returncode == 0:
        print("[✓] Zoho Lead Generator Completed Successfully!")

    print("\n" + "=" * 80)
    print("🎉 UNIFIED LEAD GENERATION PIPELINE COMPLETED")
    print("=" * 80)

if __name__ == "__main__":
    main()
