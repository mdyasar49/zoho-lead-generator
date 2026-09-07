"""
================================================================================
🚀 CENTRALIZED DATA EXPORTER & CRM SYNC PIPELINE
================================================================================
Handles automated sync to Google Sheets, Zoho CRM, and local CSV/JSON files.
Updating logic here seamlessly applies to all scrapers!
"""

import os
import csv
import json
import requests
from datetime import datetime
from typing import List, Dict, Any, Optional
from google.oauth2 import service_account
from googleapiclient.discovery import build

from config.settings import settings
from config.schemas import STANDARD_HEADERS, ZOHO_CRM_HEADERS
from core.logger import get_logger

logger = get_logger("DataExporter")

class DataExporter:
    """Enterprise multi-channel data exporter."""

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
        Automatically creates sheet tab if missing and writes headers.
        """
        if not leads:
            logger.info("No leads to sync to Google Sheets.")
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
            for lead in leads:
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
            updated_rows = updates.get("updatedRows", len(leads))
            logger.info(f"Successfully appended {updated_rows} leads to Google Sheet '{sheet_name}'.")
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
        """Saves scraped leads to a local CSV backup."""
        if not leads:
            return ""

        now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        target_file = settings.OUTPUT_DIR / (filename or f"scraped_leads_{now_str}.csv")
        target_headers = headers or list(leads[0].keys())

        try:
            with open(target_file, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.DictWriter(f, fieldnames=target_headers, extrasaction="ignore")
                writer.writeheader()
                for lead in leads:
                    writer.writerow(lead)
            
            logger.info(f"Exported {len(leads)} leads to CSV: {target_file}")
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
        """Saves scraped leads to a local JSON backup."""
        if not leads:
            return ""

        now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        target_file = settings.OUTPUT_DIR / (filename or f"scraped_leads_{now_str}.json")

        try:
            with open(target_file, "w", encoding="utf-8") as f:
                json.dump(leads, f, indent=2, ensure_ascii=False)
            logger.info(f"Exported {len(leads)} leads to JSON: {target_file}")
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
        Executes complete multi-channel export:
        1. Local CSV Backup
        2. Local JSON Backup
        3. Google Sheets Live Sync (if enabled)
        """
        if not leads:
            logger.warning(f"[{source_name}] No leads to export.")
            return {"count": 0, "status": "Empty"}

        csv_path = cls.export_to_csv(leads, f"{source_name.lower()}_leads.csv")
        json_path = cls.export_to_json(leads, f"{source_name.lower()}_leads.json")

        sheet_synced_count = 0
        if settings.AUTO_SYNC_GOOGLE_SHEETS:
            sheet_synced_count = cls.sync_to_google_sheet(
                leads=leads,
                spreadsheet_id=spreadsheet_id,
                sheet_name=f"{source_name} Leads"
            )

        return {
            "count": len(leads),
            "csv_path": csv_path,
            "json_path": json_path,
            "sheet_synced": sheet_synced_count > 0,
            "sheet_rows": sheet_synced_count
        }
