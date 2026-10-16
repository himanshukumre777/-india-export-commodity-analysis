India Export Commodity Analysis
An end-to-end data analytics project studying India's top 15 export commodities by value and comparing Calendar Year (CY) 2024 with CY 2025 (January–December). The project combines SQL analysis, Python-based statistical analysis and forecasting, destination-market analysis, and an interactive Power BI dashboard.
📌 Problem Statement
India's export commodities differ in growth, consistency, market share, destination mix, and seasonal demand. A single growth percentage cannot fully describe export performance: a commodity may grow quickly but be volatile, or remain stable while losing value.
This project evaluates export performance across multiple dimensions to answer:
- Which commodities grew or declined from 2024 to 2025?
- Which commodities show stable versus volatile monthly growth?
- Which commodities gained or lost export market share?
- Which sectors strengthened or weakened?
- Which commodities balance growth, stability, and market-share change?
- What does a short-term forecast indicate for the strongest composite performers?
- Which countries are the leading destinations for each commodity?
- In which month does each commodity reach its export peak?
- How concentrated is each commodity's destination mix?
- Which commodities may be suitable for a first-time exporter?
🗂️ Project Pipeline
TradeStat → Selenium → CSV → PostgreSQL → Python → Power BI
1. TradeStat: Monthly commodity-wise export data from the Ministry of Commerce portal.
2. Selenium: Automated data extraction from the portal.
3. CSV: Cleaned dataset containing 180 monthly records for 15 commodities.
4. PostgreSQL: Structured storage, aggregations, year-over-year comparisons, and market-share analysis.
5. Python: Pandas-based analysis of volatility, sector performance, monthly patterns, composite ranking, and forecasts.
6. Power BI: Interactive dashboard for overview, insights, destination analysis, and a new exporter guide.
🗂️ Repository Structure
export project/
├── SCRAPER/
│   └── tradestat_scraper.py
├── DATA/
│   └── Export_Data_Top15_Clean.csv
├── SQL/
│   └── sqlfinal.sql
├── PYTHON/
│   └── export_final.ipynb
├── POWERBI/
│   └── EXPORTFINAL.pbix
└── README.md
The structure above reflects the files described in the original repository. If destination-country analysis uses additional source files or notebooks, add those actual filenames here before publishing.
🔧 Tech Stack
- TradeStat portal — source for export statistics
- Python and Selenium — automated extraction
- CSV — cleaned data interchange
- PostgreSQL — data storage, aggregation, and SQL analysis
- Python (Pandas, NumPy, Matplotlib) — statistical analysis, sector grouping, ranking, and forecasting
- Jupyter Notebook — analysis workflow
- Power BI — interactive dashboard and commodity-level filtering/tooltips
📊 Data Source and Scope
- Source: Ministry of Commerce, TradeStat portal — https://tradestat.commerce.gov.in/
- Coverage: Top 15 export commodities by value
- Core monthly dataset: 180 records (15 commodities × 12 months)
- Comparison period: January–December 2024 versus January–December 2025
- Calendar-year method: Monthly values are used to construct a calendar-year view because the portal's cumulative reporting convention follows India's fiscal year (April–March).
- Extraction: Automated using a Selenium-based scraper.
The destination-analysis slides use 2025 country × month data, with values expressed in US$ million. The destination findings should be interpreted within that stated scope.
❓ Analytical Questions
SQL Layer
Question	Analysis
Q1	Overall export performance: CY 2024 versus CY 2025
Q2	Commodity-wise year-over-year growth across 15 commodities
Q3	Largest commodity by export value in 2024
Q4	Largest commodity by export value in 2025
Q6	Commodity-level market-share gain or loss


Python Layer
Question	Analysis
Q5	Monthly growth volatility and stability
Q7	Sector-wise export growth
Q8	Monthly export patterns
Q9	Composite ranking using growth, stability, and market-share change
Q10	Three-month forecast for the top three composite performers (Jan–Mar 2026)


Destination and New Exporter Layer
Question	Analysis
Q11	Top destination country for each commodity
Q12	Peak export month for each commodity
Q13	Destination concentration measured by the share going to the top three countries
Q14	Commodities that may suit a first-time exporter, based on stability, positive growth, and destination-market spread


📈 Key Findings
Overall and commodity performance
- Total export value across the selected commodities increased from US$238,017.64 million in CY 2024 to US$241,446.16 million in CY 2025, representing +1.44% growth.
- Telecom Instruments recorded the highest year-over-year growth at +53.61% and the largest market-share gain at +2.63 percentage points.
- Motor Vehicle-Cars recorded the second-highest growth at +22.28%.
- Petroleum Products remained the largest commodity by export value in both years, but declined by −22.22% and had the largest market-share loss at −3.44 percentage points.
Stability, sectors, and composite ranking
- Organic Chemicals was the most stable commodity by the project's volatility measure (standard deviation 7.47).
- Telecom Instruments was the most volatile commodity (standard deviation 26.10).
- Electronics was the strongest sector at +37.06%; Agriculture grew by +15.12% and Automotive by +14.00%.
- Energy was the weakest sector at −22.22%.
- The composite ranking placed Marine Products first (0.69), followed by Telecom Instruments (0.67) and Motor Vehicle-Cars (0.65).
- The three-month forecast covers January–March 2026 for those top three composite performers. It is based on historical monthly behaviour and is not a guarantee of future results.
Destination analysis
- The USA was the top destination for 10 of the 15 commodities in the 2025 destination analysis. Other leading destinations included the UAE, Hong Kong, the Netherlands, South Africa, and Italy.
- Telecom Instruments had the highest single-country share in the destination findings: 58.6% to the USA.
- Peak months differed by commodity. March was the peak for four commodities, while November and July were the peak for three commodities each.
- Telecom Instruments had the highest top-three-country concentration at 76.69%. Residual Chemicals & Allied had the lowest at 23.65%.
- High concentration can indicate greater exposure to demand changes in a small number of destination markets.
New Exporter Guide
The guide applies three screening rules to the 15 commodities:
1. Monthly growth volatility of 15 or less.
2. Positive growth, meaning 2025 export value is higher than 2024.
3. The top three destination countries account for 65% or less of exports.
Eight of the 15 commodities passed all three tests. Marine Products was the top overall pick by composite rank and was described in the presentation as having stable demand and +15.12% growth. Organic Chemicals was presented as a lower-volatility option but had declining growth (−4.42%), while Motor Vehicle-Cars combined +22.28% growth with moderate stability.
The presentation also includes indicative capital levels, potential entry routes, infrastructure or compliance needs, and a step-by-step path from product selection to first shipment. Capital levels are assumptions based on typical business models, not values calculated from the dataset; confirm actual requirements with suppliers and relevant export bodies before investing.
📊 Power BI Dashboard
The dashboard is presented as four pages:
1. Overview — export totals, overall growth, monthly trend, commodity and sector growth, and market share.
2. Insights — composite ranking, growth-versus-volatility analysis, and the three-month forecast.
3. Destination Analysis — destination-country breakdown, top destinations, peak export month, and top-three-market concentration. Commodity selection filters the page visuals.
4. New Exporter Guide — beginner-friendly screening, plain-language tags, indicative capital and entry-route information, and steps toward a first shipment.
Tooltip requirement: Commodity-level detail should be available on hover so users can inspect a visual without leaving the dashboard.
🚀 How to Run
1. Prepare the data. Use DATA/Export_Data_Top15_Clean.csv for the core monthly commodity dataset. The optional Selenium script in SCRAPER/tradestat_scraper.py automates extraction from the TradeStat portal; portal structure or access changes may require script updates.
2. Set up PostgreSQL. Run SQL/sqlfinal.sql in PostgreSQL to create/load the exports_v2 table and run the SQL-layer analyses (Q1, Q2, Q3, Q4, and Q6).
3. Run the Python analysis. Open PYTHON/export_final.ipynb, configure the database connection for your environment, and run the notebook cells. The original README describes generated outputs including composite_ranking.csv, volatility_scores.csv, sector_performance.csv, and forecast_top3.csv.
4. Open Power BI. Open POWERBI/EXPORTFINAL.pbix in Power BI Desktop and configure the PostgreSQL connection and any local CSV paths as required.
5. Destination analysis. The presentation reports destination insights from 2025 country-by-month data. Make sure the corresponding country-level data and model/query dependencies are available in the repository before attempting to refresh this page.
6. Check dashboard interactions. Test commodity slicers, page navigation, and commodity-level tooltips after refreshing the data.
File names and database connection settings may need to be adapted to your local environment. Do not commit passwords, access tokens, or other credentials to GitHub.
🔭 Future Scope
- Automate scheduled refreshes directly from the TradeStat source.
- Extend analysis beyond the current top 15 commodities.
- Validate indicative capital requirements with supplier quotes, processors, and export councils.
- Move the pipeline to cloud infrastructure for automated ETL and refresh.
- Improve forecasting with longer historical time series and additional models.
- Add alerts for unusual volatility or significant market-share changes.
- Strengthen validation and documentation for country-level destination data and dashboard refresh dependencies.
⚠️ Limitations and Disclaimer
- Figures are based on the project's selected commodities and the stated calendar-year methodology; they may differ from official figures presented on a fiscal-year (April–March) basis.
- Destination findings are described as based on 2025 country × month data in the presentation.
- Forecasts are projections based on historical patterns, not guarantees.
- New-exporter recommendations are screening insights, not financial, legal, or export-compliance advice. Confirm current rules and fees with the Directorate General of Foreign Trade (DGFT), the relevant Export Promotion Council, and qualified professionals before acting.
👤 Author
Himanshu Kumre
Project: India Export Commodity Analysis | CY 2024 vs CY 2025
