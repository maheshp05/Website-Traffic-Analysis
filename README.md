# Website Traffic Analysis - Alfido Tech Internship Project

This repository contains the complete deliverables for the **Website Traffic Analysis** project, completed as part of the **InternSpark Data Analytics Internship** for **Alfido Tech**.

The project transforms raw, anonymous event logs from a music distribution smartlink platform into a rich, structured dataset, followed by an in-depth exploratory data analysis (EDA), sessionization, conversion funnel profiling, user journey analysis, and the compilation of a high-resolution KPI dashboard and business report.

---

## 📊 Executive KPI Dashboard

Below is the generated portfolio-quality Executive KPI Dashboard, summarizing the core findings of the website traffic analysis.

![Executive KPI Dashboard](images/website_traffic_kpi_dashboard.png)

### Dashboard Highlights & Business Interpretation:
*   **Acquisition & Volume:** Social Media (Instagram, Facebook, YouTube) is the dominant traffic channel, driving **40.4%** (41.9K) of all sessions. Organic Search is a strong second at **29.4%** (30.4K).
*   **Mobile-First Audience:** Mobile devices represent **59.9%** of all site interactions, highlighting the critical importance of mobile optimization and speed.
*   **Funnel Conversions:** The overall conversion rate (sessions resulting in an outgoing click to a music store like Spotify or Apple Music) is **25.71%** (27.6K store clicks), indicating high purchase intent among visitors.
*   **Engagement Challenge:** The overall bounce rate is **61.94%**, meaning nearly 3 in 5 users leave after a single pageview. The average session duration is short at **39.9 seconds**.
*   **Peak Timing:** Traffic peaks significantly on **Thursdays** and during the evening hours (**7:00 PM** peak), showing the optimal window for new artist campaign launches.

---

## 🗂️ Project Repository Structure

```
Website-Traffic-Analysis/
├── Website_Traffic_Analysis.ipynb    # Main analytical notebook (fully executed)
├── cleaned_dataset.csv               # Enriched sessionized dataset (108,723 rows)
├── clean_and_enrich.py               # ETL script: Raw data to cleaned/enriched CSV
├── create_notebook.py                # Script used to programmatically build the Jupyter notebook
├── generate_kpi_dashboard.py         # Script that generates the high-res dashboard (PNG, PDF, HTML)
├── README.md                         # Project documentation and dashboard display
├── dataset/
│   └── traffic.csv                   # Raw original dataset (226,278 rows)
├── images/                           # Directory containing all 16 generated visualizations
│   ├── website_traffic_kpi_dashboard.png  # Main Executive Dashboard (PNG)
│   ├── website_traffic_kpi_dashboard.pdf  # Main Executive Dashboard (PDF)
│   ├── 01_event_distribution.png     # Funnel breakdown (Pageviews vs Previews vs Clicks)
│   └── ...                           # Other analytical charts (02 to 15)
└── report/
    ├── report.pdf                    # Final multi-page PDF Business Report (928 KB, 27 pages)
    ├── generate_report_final.py      # Python ReportLab script generating the PDF report
    ├── extract_kpis.py               # Helper script extracting metrics from cleaned CSV
    └── requirements.txt              # Project dependency requirements
```

---

## 🛠️ Installation & Reproduction

To reproduce the analysis, visualizations, KPI dashboard, and final PDF report:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/<your-username>/Website-Traffic-Analysis.git
    cd Website-Traffic-Analysis
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    # On Windows:
    .venv\Scripts\activate
    # On macOS/Linux:
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r report/requirements.txt
    ```

4.  **Run the ETL cleaning & enrichment script:**
    ```bash
    python clean_and_enrich.py
    ```

5.  **Generate the KPI dashboard:**
    ```bash
    python generate_kpi_dashboard.py
    ```

6.  **Compile the PDF business report:**
    ```bash
    python report/generate_report_final.py
    ```

---

## ⚠ Data Transparency & Enriched Fields Disclosure

This project is developed for educational purposes to demonstrate advanced web analytics methodologies. Please note the following regarding the fields:
*   **Original Fields:** The raw dataset (`dataset/traffic.csv`) contains `event`, `date`, `country`, `city`, `artist`, `album`, `track`, `isrc`, and `linkid`.
*   **Synthetically Enriched Fields:** The fields `user_id`, `session_id`, `timestamp` (precise hour/minute/second), `device`, `traffic_source`, `traffic_category`, and `page_url` were synthetically generated in `clean_and_enrich.py` using seeded random distributions and deterministic grouping logic.
*   **Methodology Demonstration:** These synthetic fields simulate real-world tracking parameters (such as cookie IDs and UTM referrers) to enable demonstration of **sessionization**, **bounce rate estimation**, **user journey pathing**, and **device/traffic channel profiling**. The derived metrics (e.g. bounce rate by device) should be interpreted as demonstrating the analytical pipeline rather than representing real, observed user-level data.

---

## 📈 Key Insights & Recommendations

The final business report identifies several core insights and recommendations for Alfido Tech:
1.  **Audio Preview Optimization:** The average session duration is **39.9s** and bounce rate is **61.94%**. Placing a prominent audio preview player above-the-fold on mobile/desktop will engage users earlier and reduce quick exits.
2.  **Geo-Localised Store Alignment:** India (15.3%), France (8.6%), and Saudi Arabia (6.3%) are key traffic drivers. Dynamically re-ordering store links (e.g. JioSaavn in India, Deezer in France, Anghami in Saudi Arabia) based on user IP geolocation will lift conversion rates.
3.  **Homepage Content Discovery:** The homepage (`/`) is both the #1 landing and #1 exit point. Adding a curated "Trending Now" or search bar on the homepage will guide passive landing-page traffic deeper into specific artist/track pages.
4.  **Release Campaign Timing:** Launch new campaigns and promotional pushes on Thursdays between 7:00 PM and 9:00 PM to align with the peak activity window of music listeners.
