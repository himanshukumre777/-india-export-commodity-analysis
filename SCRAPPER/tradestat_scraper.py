"""
TradeStat Export Data Scraper
==============================
Automatically extracts monthly export data (Jan-Dec, 2024 vs 2025)
for 15 selected commodities from https://tradestat.commerce.gov.in
and combines everything into one Excel file (one sheet per commodity).

SETUP (run these once in your terminal / Jupyter):
    pip install selenium webdriver-manager pandas openpyxl --break-system-packages

Then just run this script:
    python tradestat_scraper.py

IMPORTANT NOTES:
- This script controls a real Chrome browser window (you'll see it open
  and click through pages automatically). Do not close it manually.
- Government websites sometimes change their page structure. If this
  script fails with an error, take a screenshot of the error and the
  webpage, and we can fix the selectors together.
- The script saves progress after every commodity, so if it fails
  halfway, you won't lose everything — just re-run it (it will
  overwrite from scratch, so keep the partial CSV if you want to
  inspect what worked).
- TEST_MODE is set to True by default — it will only scrape ONE
  commodity and ONE month first, so you can verify everything works
  before committing to the full ~180-step run. Once you confirm the
  test output looks correct, set TEST_MODE = False and run again.
"""

import time
import re
from io import StringIO
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# ---------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------

TEST_MODE = False  # <-- set to False once the test run looks correct

URL = "https://tradestat.commerce.gov.in/ftspcc/export_commodity_wise"

# Exact dropdown option text for the Commodity field (must match the
# website's spelling exactly, including punctuation).
COMMODITIES = [
    "PETROLEUM PRODUCTS",
    "TELECOM INSTRUMENTS",
    "DRUG FORMULATIONS, BIOLOGICALS",
    "ELECTRIC MACHINERY AND EQUIPME",
    "PEARL, PRECS, SEMIPRECS STONES",
    "GOLD AND OTH PRECS METL JWLERY",
    "RMG COTTON INCL ACCESSORIES",
    "MOTOR VEHICLE/CARS",
    "PRODUCTS OF IRON AND STEEL",
    "IRON AND STEEL",
    "INDL. MACHNRY FOR DAIRY ETC",
    "AUTO COMPONENTS/PARTS",
    "RESIDUL CHEMICL AND ALLED PROD",
    "MARINE PRODUCTS",
    "ORGANIC CHEMICALS",
]

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]

YEAR = "2025"          # this makes the site compare 2025 vs 2024 automatically
VALUES_IN = "US $ Million"

OUTPUT_FILE = "Export_Data_Top15_2024_2025.xlsx"
PROGRESS_CSV = "tradestat_scrape_progress.csv"

# ---------------------------------------------------------------------
# SCRAPER LOGIC
# ---------------------------------------------------------------------


def get_driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.set_window_size(1400, 1000)
    return driver


def scrape_one(driver, commodity, month):
    """Load the page fresh, set all four dropdowns, submit, and
    return the resulting table as a pandas DataFrame (or None if
    something went wrong)."""

    driver.get(URL)
    wait = WebDriverWait(driver, 20)

    # Wait for the form's selects to be present, then grab them in
    # page order: Month, Year, Commodity, Values in.
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "select")))
    selects = driver.find_elements(By.TAG_NAME, "select")
    if len(selects) < 4:
        raise RuntimeError(
            f"Expected 4 dropdowns on the page, found {len(selects)}. "
            "The website layout may have changed."
        )

    month_select, year_select, commodity_select, values_select = selects[:4]

    Select(month_select).select_by_visible_text(month)
    Select(year_select).select_by_visible_text(YEAR)
    Select(commodity_select).select_by_visible_text(commodity)
    Select(values_select).select_by_visible_text(VALUES_IN)

    # Click Submit
    submit_btn = driver.find_element(
        By.XPATH, "//button[contains(text(),'Submit')] | //input[@value='Submit']"
    )
    submit_btn.click()

    # Wait for a results table to appear
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
    time.sleep(1.5)  # small buffer for any AJAX re-render

    tables = pd.read_html(StringIO(driver.page_source))
    # Pick the largest table on the page (the data table, not nav/footer tables)
    data_table = max(tables, key=lambda t: t.shape[1])

    # Drop the "Total" summary row (sums across all commodities) —
    # we only want the row for this specific commodity.
    commodity_col = next(
        (c for c in data_table.columns if "commodity" in str(c).lower()), None
    )
    if commodity_col is not None:
        data_table = data_table[
            ~data_table[commodity_col].astype(str).str.strip().str.lower().eq("total")
        ]

    data_table["commodity_group"] = commodity
    data_table["month"] = month
    return data_table


def main():
    driver = get_driver()
    all_rows = []
    failures = []

    commodities_to_run = COMMODITIES[:1] if TEST_MODE else COMMODITIES
    months_to_run = MONTHS[:1] if TEST_MODE else MONTHS

    total = len(commodities_to_run) * len(months_to_run)
    done = 0

    try:
        for commodity in commodities_to_run:
            for month in months_to_run:
                done += 1
                print(f"[{done}/{total}] Scraping {commodity} - {month} ...", end=" ")
                try:
                    df = scrape_one(driver, commodity, month)
                    all_rows.append(df)
                    print("OK")
                except Exception as e:
                    print(f"FAILED ({e})")
                    failures.append((commodity, month, str(e)))

            # Save progress after each commodity finishes, so nothing
            # is lost if a later commodity fails.
            if all_rows:
                pd.concat(all_rows, ignore_index=True).to_csv(
                    PROGRESS_CSV, index=False
                )

    finally:
        driver.quit()

    if not all_rows:
        print("\nNo data was scraped. Check the failures list below.")
        print(failures)
        return

    combined = pd.concat(all_rows, ignore_index=True)
    print(f"\nScraped {len(combined)} rows total.")

    if failures:
        print(f"\n{len(failures)} combinations failed:")
        for c, m, err in failures:
            print(f"  - {c} / {m}: {err}")

    if TEST_MODE:
        print("\n=== TEST MODE OUTPUT ===")
        print(combined.to_string())
        print(
            "\nIf this looks correct (one row, with Jan 2024 / Jan 2025 "
            "value & share columns), set TEST_MODE = False at the top "
            "of this script and run it again for the full 15 x 12 scrape."
        )
        return

    # ---------------- Full run: build the final Excel workbook ----------------
    with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
        for commodity in COMMODITIES:
            sheet_df = combined[combined["commodity_group"] == commodity]
            # Excel sheet names: max 31 chars, no / \ ? * [ ] :
            sheet_name = re.sub(r"[\\/*?:\[\]]", "-", commodity)[:31]
            sheet_df.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"\n✅ Done! Saved combined workbook to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
