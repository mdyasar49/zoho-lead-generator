"""
================================================================================
🚀 UNIFIED MASTER RUNNER: ODOO & ZOHO SALES EXECUTIVE LEAD GENERATORS
================================================================================
Targets:
  1. Odoo Sales Executive Leads  -> Google Sheet 1 (1X_8LbsHisyvoCfjSuTX5yRVsRgXPDEmu3W5RWXuAC1o)
  2. Zoho Sales Executive Leads  -> Google Sheet 2 (18oHqPuo6BhAgI5e_GLSSps5fSc_DpzYEYofgPKxBv9o)
  3. Zoho CRM Live Cloud API     -> All Leads Upserted 24/7
================================================================================
"""

import sys
import json
import subprocess
from pathlib import Path
from zoho_crm import upload_leads_to_zoho_crm

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def main():
    print("=" * 80)
    print("🚀 STARTING UNIFIED LEAD GENERATION PIPELINE (ODOO & ZOHO)")
    print("=" * 80)

    print("\n[1/3] Executing Live Odoo Sales Executive Lead Generator...")
    res_odoo = subprocess.run([sys.executable, "live_odoo_sales_lead_generator.py"])
    if res_odoo.returncode == 0:
        print("[✓] Odoo Lead Generator Completed Successfully!")
    else:
        print("[!] Odoo Lead Generator encountered an issue.")

    print("\n[2/3] Executing Live Zoho Sales Executive Lead Generator...")
    res_zoho = subprocess.run([sys.executable, "live_zoho_sales_lead_generator.py"])
    if res_zoho.returncode == 0:
        print("[✓] Zoho Lead Generator Completed Successfully!")
    else:
        print("[!] Zoho Lead Generator encountered an issue.")

    print("\n[3/3] Uploading all generated leads directly to Zoho CRM Cloud API...")
    output_dir = Path(__file__).resolve().parent / "output"
    total_crm_uploaded = 0

    for json_file in output_dir.glob("*.json"):
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                leads = json.load(f)
                if isinstance(leads, list) and leads:
                    print(f"  -> Uploading {len(leads)} leads from {json_file.name} to Zoho CRM...")
                    count = upload_leads_to_zoho_crm(leads, lead_source="Direct Technology Sales Directory")
                    total_crm_uploaded += count
        except Exception as e:
            print(f"  [!] Error reading {json_file.name}: {e}")

    print("\n" + "=" * 80)
    print(f"🎉 UNIFIED PIPELINE COMPLETED! Total Zoho CRM Upserts: {total_crm_uploaded}")
    print("=" * 80)

if __name__ == "__main__":
    main()
