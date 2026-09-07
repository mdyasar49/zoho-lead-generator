"""
================================================================================
🚀 CENTRALIZED DATA EXPORTER & ZERO-BOUNCE CRM SYNC PIPELINE
================================================================================
Handles automated sync to Google Sheets, Zoho CRM, and local CSV/JSON files.
STRICT RULE: Discards any lead with an undeliverable, dead, or bouncing email address.
Updating logic here seamlessly applies to all scrapers!
================================================================================
"""

import os
import sys
import csv
import json
import requests
from datetime import datetime
from typing import List, Dict, Any, Optional
from google.oauth2 import service_account
from googleapiclient.discovery import build

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from lead_verifier import is_email_deliverable
from config.settings import settings
from config.schemas import STANDARD_HEADERS, ZOHO_CRM_HEADERS
from core.logger import get_logger

logger = get_logger("DataExporter")

class DataExporter:
    """Enterprise multi-channel data exporter with strict zero-bounce filtering."""

    @staticmethod
    def filter_valid_deliverable_leads(leads: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Strictly filters leads to only retain those with 100% verified, deliverable emails.
        Completely discards leads with bouncing, blacklisted, or dead email addresses.
        """
        clean_leads = []
        for lead in leads:
            email = (
                lead.get("Work Email") or
                lead.get("Primary Work Email") or
                lead.get("Email") or
                lead.get("email") or
                lead.get("verified_email") or
                ""
            ).strip().lower()

            if not email or "@" not in email:
                continue

            ok, clean_em, reason = is_email_deliverable(email)
            if ok:
                clean_leads.append(lead)
            else:
                comp = lead.get("Company Name") or lead.get("Company") or "Unknown"
                logger.warning(f"Dropped bouncing/undeliverable lead '{comp}' (Email: {email}) - Reason: {reason}")

        return clean_leads

    @staticmethod
    def get_sheets_service():
        """Builds an authenticated Google Sheets API client."""
        info = settings.get_service_account_info()
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = service_account.Credentials.from_service_account_info(info, scopes=scopes)
        return build("sheets", "v4", credentials=creds)

    @classmethod
    def sync_to_google_sheet(
        cls,
        leads: List[Dict[str, Any]],
        spreadsheet_id: Optional[str] = None,
        sheet_name: str = "Master Leads",
        headers: Optional[List[str]] = None
    ) -> int:
        """
        Syncs a list of lead dictionaries into Google Sheets.
        Strictly filters out any undeliverable/bouncing email before syncing.
        """
        verified_leads = cls.filter_valid_deliverable_leads(leads)
        if not verified_leads:
            logger.info("No verified deliverable leads to sync to Google Sheets.")
            return 0

        target_spreadsheet_id = spreadsheet_id or settings.SPREADSHEET_ID_MASTER
        target_headers = headers or STANDARD_HEADERS

        try:
            service = cls.get_sheets_service()
            sheet = service.spreadsheets()

            # 1. Check/Add Tab
            spreadsheet_meta = sheet.get(spreadsheetId=target_spreadsheet_id).execute()
            existing_sheets = [s['properties']['title'] for s in spreadsheet_meta.get('sheets', [])]

            if sheet_name not in existing_sheets:
                add_sheet_request = {
                    "requests": [{
                        "addSheet": {
                            "properties": {
                                "title": sheet_name,
                                "gridProperties": {"frozenRowCount": 1}
                            }
                        }
                    }]
                }
                sheet.batchUpdate(spreadsheetId=target_spreadsheet_id, body=add_sheet_request).execute()
                logger.info(f"Created new sheet tab: '{sheet_name}'")

            # 2. Check if headers exist
            read_result = sheet.values().get(
                spreadsheetId=target_spreadsheet_id,
                range=f"'{sheet_name}'!A1:Z1"
            ).execute()
            rows = read_result.get("values", [])

            if not rows:
                # Write header row
                sheet.values().update(
                    spreadsheetId=target_spreadsheet_id,
                    range=f"'{sheet_name}'!A1",
                    valueInputOption="USER_ENTERED",
                    body={"values": [target_headers]}
                ).execute()

            # 3. Format row data according to headers
            row_data = []
            for lead in verified_leads:
                row = [str(lead.get(h, "")) for h in target_headers]
                row_data.append(row)

            # 4. Append rows
            append_result = sheet.values().append(
                spreadsheetId=target_spreadsheet_id,
                range=f"'{sheet_name}'!A1",
                valueInputOption="USER_ENTERED",
                insertDataOption="INSERT_ROWS",
                body={"values": row_data}
            ).execute()

            updates = append_result.get("updates", {})
            updated_rows = updates.get("updatedRows", len(verified_leads))
            logger.info(f"Successfully appended {updated_rows} verified deliverable leads to Google Sheet '{sheet_name}'.")
            return updated_rows

        except Exception as e:
            logger.error(f"Google Sheets sync failed: {e}")
            return 0

    @classmethod
    def export_to_csv(
        cls,
        leads: List[Dict[str, Any]],
        filename: Optional[str] = None,
        headers: Optional[List[str]] = None
    ) -> str:
        """Saves verified scraped leads to a local CSV backup."""
        verified_leads = cls.filter_valid_deliverable_leads(leads)
        if not verified_leads:
            return ""

        now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        target_file = settings.OUTPUT_DIR / (filename or f"scraped_leads_{now_str}.csv")
        target_headers = headers or list(verified_leads[0].keys())

        try:
            with open(target_file, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.DictWriter(f, fieldnames=target_headers, extrasaction="ignore")
                writer.writeheader()
                for lead in verified_leads:
                    writer.writerow(lead)
            
            logger.info(f"Exported {len(verified_leads)} verified leads to CSV: {target_file}")
            return str(target_file)
        except Exception as e:
            logger.error(f"CSV export failed: {e}")
            return ""

    @classmethod
    def export_to_json(
        cls,
        leads: List[Dict[str, Any]],
        filename: Optional[str] = None
    ) -> str:
        """Saves verified scraped leads to a local JSON backup."""
        verified_leads = cls.filter_valid_deliverable_leads(leads)
        if not verified_leads:
            return ""

        now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        target_file = settings.OUTPUT_DIR / (filename or f"scraped_leads_{now_str}.json")

        try:
            with open(target_file, "w", encoding="utf-8") as f:
                json.dump(verified_leads, f, indent=2, ensure_ascii=False)
            logger.info(f"Exported {len(verified_leads)} verified leads to JSON: {target_file}")
            return str(target_file)
        except Exception as e:
            logger.error(f"JSON export failed: {e}")
            return ""

    @classmethod
    def export_all(
        cls,
        leads: List[Dict[str, Any]],
        source_name: str = "Scraper",
        spreadsheet_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes complete multi-channel export for verified deliverable leads:
        1. Strict Zero-Bounce Filter
        2. Local CSV Backup
        3. Local JSON Backup
        4. Google Sheets Live Sync (if enabled)
        """
        verified_leads = cls.filter_valid_deliverable_leads(leads)
        if not verified_leads:
            logger.warning(f"[{source_name}] No verified deliverable leads to export (All invalid/bouncing leads were dropped).")
            return {"count": 0, "status": "Empty"}

        csv_path = cls.export_to_csv(verified_leads, f"{source_name.lower()}_leads.csv")
        json_path = cls.export_to_json(verified_leads, f"{source_name.lower()}_leads.json")

        sheet_synced_count = 0
        if settings.AUTO_SYNC_GOOGLE_SHEETS:
            sheet_synced_count = cls.sync_to_google_sheet(
                leads=verified_leads,
                spreadsheet_id=spreadsheet_id,
                sheet_name=f"{source_name} Leads"
            )

        return {
            "count": len(verified_leads),
            "csv_path": csv_path,
            "json_path": json_path,
            "sheet_synced": sheet_synced_count > 0,
            "sheet_rows": sheet_synced_count
        }
