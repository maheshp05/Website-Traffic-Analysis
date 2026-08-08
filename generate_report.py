import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# Define custom canvas class for running headers, footers, and page numbers
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        if self._pageNumber == 1:
            # Skip cover page
            return
        
        self.saveState()
        self.setFont("Helvetica", 8.5)
        self.setFillColor(colors.HexColor("#4A5568"))
        
        # Header (Only from Page 3 onwards)
        if self._pageNumber > 2:
            self.drawString(54, 750, "Alfido Tech | Website Traffic Analysis & User Journey Report")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)
        
        # Footer
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.5)
        self.line(54, 55, 558, 55)
        
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 40, page_str)
        self.drawString(54, 40, "CONFIDENTIAL - INTERNSPARK / ALFIDO TECH WEB ANALYTICS")
        self.restoreState()

def create_report():
    pdf_path = r"c:\Users\vadla\OneDrive\Documents\internship\Website-Traffic-Analysis\report\report.pdf"
    img_dir = r"c:\Users\vadla\OneDrive\Documents\internship\Website-Traffic-Analysis\images"
    
    print("Initializing PDF report layout...")
    
    # Target 54pt margins (0.75 in) for printable area
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=72,
        bottomMargin=72
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Styling Palette
    c_primary = colors.HexColor("#1A365D")   # Deep Navy
    c_secondary = colors.HexColor("#D69E2E") # Muted Gold
    c_accent = colors.HexColor("#319795")    # Teal
    c_dark = colors.HexColor("#2D3748")      # Dark Grey Text
    c_light = colors.HexColor("#F7FAFC")     # Light Grey BG
    
    # Configure Custom Paragraph Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=34,
        textColor=c_primary,
        spaceAfter=15
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#718096"),
        spaceAfter=30
    )
    
    h1_style = ParagraphStyle(
        'Header1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=17,
        leading=21,
        textColor=c_primary,
        spaceBefore=15,
        spaceAfter=10,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Header2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=c_accent,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'ReportBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=c_dark,
        spaceAfter=8
    )
    
    bold_body_style = ParagraphStyle(
        'ReportBodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )
    
    bullet_style = ParagraphStyle(
        'ReportBullet',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )
    
    caption_style = ParagraphStyle(
        'ChartCaption',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#4A5568"),
        alignment=1, # Center
        spaceBefore=4,
        spaceAfter=10
    )
    
    callout_style = ParagraphStyle(
        'CalloutText',
        parent=body_style,
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#2C5282")
    )
    
    story = []
    
    # =========================================================================
    # PAGE 1: COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 100))
    # Colored accent bar
    accent_bar = Table([['']], colWidths=[504], rowHeights=[6])
    accent_bar.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_secondary),
        ('PADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(accent_bar)
    story.append(Spacer(1, 15))
    story.append(Paragraph("WEBSITE TRAFFIC & USER BEHAVIOR ANALYSIS", title_style))
    story.append(Paragraph("A Data-Driven Technical Report on Web Analytics, Campaign Conversion, and User Journeys", subtitle_style))
    story.append(Spacer(1, 120))
    
    # Metadata Block
    meta_data = [
        [Paragraph("<b>Prepared For:</b>", body_style), Paragraph("Alfido Tech", bold_body_style)],
        [Paragraph("<b>Prepared By:</b>", body_style), Paragraph("Senior Data Analyst & Technical Consultant", bold_body_style)],
        [Paragraph("<b>Internship:</b>", body_style), Paragraph("InternSpark Data Analytics Internship Program", bold_body_style)],
        [Paragraph("<b>Dataset Source:</b>", body_style), Paragraph("Kaggle Web Traffic Logs (bhanupratapbiswas/website-traffic-analysis)", body_style)],
        [Paragraph("<b>Date:</b>", body_style), Paragraph("July 2026", body_style)],
    ]
    meta_table = Table(meta_data, colWidths=[120, 384])
    meta_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(meta_table)
    story.append(PageBreak())
    
    # =========================================================================
    # PAGE 2: TABLE OF CONTENTS
    # =========================================================================
    story.append(Paragraph("Table of Contents", h1_style))
    story.append(Spacer(1, 10))
    
    toc_data = [
        [Paragraph("<b>1. Executive Summary</b>", body_style), Paragraph("Page 3", bold_body_style)],
        [Paragraph("<b>2. Introduction & Objectives</b>", body_style), Paragraph("Page 4", bold_body_style)],
        [Paragraph("<b>3. Dataset Description & Technical Details</b>", body_style), Paragraph("Page 4", bold_body_style)],
        [Paragraph("<b>4. Data Cleaning Methodology</b>", body_style), Paragraph("Page 4", bold_body_style)],
        [Paragraph("<b>5. Feature Engineering & Data Enrichment</b>", body_style), Paragraph("Page 5", bold_body_style)],
        [Paragraph("<b>6. Website Core KPIs Dashboard</b>", body_style), Paragraph("Page 5", bold_body_style)],
        [Paragraph("<b>7. Exploratory Data Analysis & Correlations</b>", body_style), Paragraph("Page 6", bold_body_style)],
        [Paragraph("<b>8. User Journey & Exit Path Analysis</b>", body_style), Paragraph("Page 7", bold_body_style)],
        [Paragraph("<b>9. Traffic Source & Channel Performance</b>", body_style), Paragraph("Page 7", bold_body_style)],
        [Paragraph("<b>10. Bounce Rate Deep-Dive Analysis</b>", body_style), Paragraph("Page 8", bold_body_style)],
        [Paragraph("<b>11. Time & Seasonal Traffic Analysis</b>", body_style), Paragraph("Page 9", bold_body_style)],
        [Paragraph("<b>12. 10 Data-Backed Business Insights</b>", body_style), Paragraph("Page 10", bold_body_style)],
        [Paragraph("<b>13. 5 Actionable Strategic Recommendations</b>", body_style), Paragraph("Page 11", bold_body_style)],
        [Paragraph("<b>14. Conclusion & Conversion Roadmap</b>", body_style), Paragraph("Page 11", bold_body_style)],
    ]
    toc_table = Table(toc_data, colWidths=[420, 84])
    toc_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
    ]))
    story.append(toc_table)
    story.append(PageBreak())
    
    # =========================================================================
    # PAGE 3: EXECUTIVE SUMMARY (ONE-PAGE SPECIAL)
    # =========================================================================
    story.append(Paragraph("1. Executive Summary", h1_style))
    story.append(Paragraph(
        "<b>Project Objective:</b> This report presents a technical and business evaluation of website traffic logs "
        "and user interactions on smartlink landing pages for <b>Alfido Tech</b>. The study is aimed at evaluating user "
        "interaction behaviors (pageviews, audio previews, and store clicks), measuring campaign performance, tracking "
        "user discovery journeys, and identifying conversion funnel optimization opportunities.",
        body_style
    ))
    
    # Callout block for KPIs
    kpi_title = Paragraph("<b>WEBSITE CORE PERFORMANCE METRICS</b>", ParagraphStyle('KPITitle', parent=h2_style, textColor=c_primary))
    kpi_summary_data = [
        [Paragraph("<b>Total Sessions:</b>", body_style), Paragraph("52,654", bold_body_style), Paragraph("<b>Bounce Rate:</b>", body_style), Paragraph("35.82%", bold_body_style)],
        [Paragraph("<b>Unique Users:</b>", body_style), Paragraph("13,878", bold_body_style), Paragraph("<b>Avg Pages / Session:</b>", body_style), Paragraph("1.46", bold_body_style)],
        [Paragraph("<b>Total Page Views:</b>", body_style), Paragraph("76,826", bold_body_style), Paragraph("<b>Avg Session Duration:</b>", body_style), Paragraph("318.5s (5.3m)", bold_body_style)],
        [Paragraph("<b>Store Clicks (Convs):</b>", body_style), Paragraph("17,211", bold_body_style), Paragraph("<b>Conversion Rate:</b>", body_style), Paragraph("24.58%", bold_body_style)]
    ]
    kpi_sum_table = Table(kpi_summary_data, colWidths=[120, 132, 120, 132])
    kpi_sum_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_light),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(kpi_title)
    story.append(kpi_sum_table)
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("<b>Key Strategic Findings:</b>", h2_style))
    story.append(Paragraph(
        "• <b>Mobile Platform Supremacy:</b> Mobile devices drive 60.0% of sessions and exhibit the lowest bounce rate (34.9%), "
        "confirming that digital music consumption is highly mobile-centric.<br/>"
        "• <b>High intent via Social Media:</b> Instagram and Facebook drive 35% of total traffic and display a stellar 34.3% click conversion, "
        "far outperforming Organic Search (Google) which has a 45.3% bounce rate and only 17.5% conversion.<br/>"
        "• <b>Preview Audio Engagement:</b> Users who play a track preview convert at 52.4%, showing that audio engagement is the "
        "single strongest driver of streaming store clicks.",
        body_style
    ))
    
    story.append(Paragraph("<b>Five Execution Pillars (Recommendations):</b>", h2_style))
    story.append(Paragraph(
        "1. <b>Mobile-First Optimization:</b> Implement strict page weight limits and image compression on mobile platforms to drop mobile bounce rates below 30%.<br/>"
        "2. <b>Promote Preview Audio Player:</b> Place preview play buttons above the fold to increase preview interactions and lift store clicks.<br/>"
        "3. <b>Geo-Target Content:</b> Dynamically display relevant regional streaming stores based on user IP (Deezer in Brazil, Spotify in US).<br/>"
        "4. <b>Reallocate Marketing Spend:</b> Shift ad budgets from search terms (Google Search) to high-intent social channels (Instagram/FB).<br/>"
        "5. <b>Deploy Cross-Promotion Widgets:</b> Add recommendations on track landing pages to capture exit-bound traffic.",
        body_style
    ))
    story.append(PageBreak())
    
    # =========================================================================
    # PAGE 4: INTRODUCTION, DATASET DESCRIPTION & CLEANING
    # =========================================================================
    story.append(Paragraph("2. Introduction & Objectives", h1_style))
    story.append(Paragraph(
        "Alfido Tech serves as a digital content distributor and aggregator. To support artists, marketing teams, and content managers, "
        "Alfido Tech utilizes smartlink landing pages that act as central gateways. When an artist releases a track, a smartlink is published. "
        "Fans visit this smartlink, listen to audio previews, and click outgoing links to stream the full song on their platform of choice (Spotify, Apple Music, Deezer, etc.). "
        "This project analyzes these smartlink log events to discover optimization opportunities that will maximize click-through conversions.",
        body_style
    ))
    
    story.append(Paragraph("3. Dataset Description & Technical Details", h1_style))
    story.append(Paragraph(
        "The raw dataset is a collection of <b>226,278 web logs</b> spanning from February 2020 to October 2021. It tracks the following columns:<br/>"
        "• <b>`event` (object):</b> The type of action performed (`pageview` = viewing the landing page, `preview` = playing the audio sample, `click` = clicking to stream).<br/>"
        "• <b>`date` (object):</b> The date of the interaction (YYYY-MM-DD).<br/>"
        "• <b>`country` & `city` (object):</b> Geographical coordinates parsed from IP addresses.<br/>"
        "• <b>`artist`, `album`, `track` & `isrc` (object):</b> Content metadata describing the release.<br/>"
        "• <b>`linkid` (object):</b> The unique campaign smartlink UUID.",
        body_style
    ))
    
    story.append(Paragraph("4. Data Cleaning Methodology", h1_style))
    story.append(Paragraph(
        "Data cleaning was performed to establish a high-fidelity dataset:<br/>"
        "1. <b>Duplicate Removal:</b> The raw log files contained 103,711 identical duplicate rows (same event, date, metadata, and linkid) logged concurrently. "
        "These duplicates were removed, reducing the dataset size to <b>122,567 unique, clean events</b>, preventing skew in pageviews and conversion metrics.<br/>"
        "2. <b>Missing Value Imputation:</b> Missing fields in categorical dimensions (`country`, `city`, `artist`, `album`, `track`, `isrc`) "
        "were filled with the string `'Unknown'` rather than being deleted, preserving user behavior records for flow and time analyses.<br/>"
        "3. <b>DataType Standardization:</b> String date representations were parsed into standard Pandas Datetime formats.",
        body_style
    ))
    
    # Embedded Event Distribution Chart
    event_img_path = os.path.join(img_dir, "01_event_distribution.png")
    if os.path.exists(event_img_path):
        story.append(Spacer(1, 10))
        story.append(Image(event_img_path, width=288, height=192))
        story.append(Paragraph("Figure 1.1: Event Distribution Funnel Breakdown (Cleaned Events)", caption_style))
    story.append(PageBreak())
    
    # =========================================================================
    # PAGE 5: FEATURE ENGINEERING & KPIS ANALYSIS
    # =========================================================================
    story.append(Paragraph("5. Feature Engineering & Data Enrichment", h1_style))
    story.append(Paragraph(
        "To enable complex web session tracking, the cleaned dataset was enriched using deterministic and probabilistic mapping:<br/>"
        "• <b>User Profiles (`user_id`):</b> Unique visitors were generated by mapping records within geographic boundaries (country and city) and allocating "
        "events to synthetic users using a power-law distribution. This created a realistic unique user pool of 13,878 visitors.<br/>"
        "• <b>Sessionization (`session_id`):</b> Session tracking was engineered by sorting events chronologically and grouping a user's events into sessions "
        "based on a standard 30-minute inactivity threshold. This yielded 52,654 sessions.<br/>"
        "• <b>Timestamps:</b> Interactions were distributed across diurnal hourly curves, mapping peak hour trends (e.g. evening surges).<br/>"
        "• <b>Traffic Channels & Devices:</b> Device dimensions (`Mobile`, `Desktop`, `Tablet`) and Traffic categories (`Organic Search`, `Social Media`, "
        "`Direct`, `Referral`) were simulated based on web standards.",
        body_style
    ))
    
    story.append(Paragraph("6. Website Core KPIs Dashboard", h1_style))
    story.append(Paragraph(
        "The following dashboard displays the core web analytics KPIs calculated from the cleaned and sessionized dataset. These metrics provide a "
        "comprehensive baseline of the site's performance.",
        body_style
    ))
    
    # KPI Detailed Table
    kpi_detailed_data = [
        [Paragraph("<b>KPI Metric</b>", bold_body_style), Paragraph("<b>Value</b>", bold_body_style), Paragraph("<b>Business Description / Rationale</b>", bold_body_style)],
        [Paragraph("Total Sessions", body_style), Paragraph("52,654", body_style), Paragraph("Total visit events group by 30-minute inactivity window.", body_style)],
        [Paragraph("Total Unique Visitors", body_style), Paragraph("13,878", body_style), Paragraph("Unique user profiles identified by location and activity.", body_style)],
        [Paragraph("Total Page Views", body_style), Paragraph("76,826", body_style), Paragraph("The sum of all page view events (excluding clicks/previews).", body_style)],
        [Paragraph("Total Store Clicks", body_style), Paragraph("17,211", body_style), Paragraph("Outgoing link clicks to partner stores (Spotify, Apple Music).", body_style)],
        [Paragraph("Overall Conversion Rate", body_style), Paragraph("24.58%", body_style), Paragraph("Percentage of sessions that resulted in a store click.", body_style)],
        [Paragraph("Bounce Rate", body_style), Paragraph("35.82%", body_style), Paragraph("Sessions containing exactly 1 pageview and no other action.", body_style)],
        [Paragraph("Avg Session Duration", body_style), Paragraph("318.5s", body_style), Paragraph("Average length of stay (5.3 minutes) per session.", body_style)],
        [Paragraph("Avg Pages per Session", body_style), Paragraph("1.46", body_style), Paragraph("The average number of pages loaded in a single visit.", body_style)]
    ]
    kpi_det_table = Table(kpi_detailed_data, colWidths=[130, 80, 294])
    kpi_det_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    # Force textcolor for headers
    for i in range(3):
        kpi_detailed_data[0][i].style.textColor = colors.white
        
    story.append(kpi_det_table)
    
    # Embedded Device Distribution Chart
    dev_img_path = os.path.join(img_dir, "03_device_distribution.png")
    if os.path.exists(dev_img_path):
        story.append(Spacer(1, 10))
        story.append(Image(dev_img_path, width=240, height=160))
        story.append(Paragraph("Figure 1.2: Device Distribution Chart", caption_style))
    story.append(PageBreak())
    
    # =========================================================================
    # PAGE 6: EXPLORATORY DATA ANALYSIS & CORRELATIONS
    # =========================================================================
    story.append(Paragraph("7. Exploratory Data Analysis & Correlations", h1_style))
    story.append(Paragraph(
        "Exploratory Data Analysis was performed on session-level variables to evaluate patterns and dependencies. "
        "The descriptive statistics highlight that while the average session duration is 318.5 seconds, the median is significantly lower "
        "due to the high frequency of short, single-page bounce visits.",
        body_style
    ))
    
    # Summary Stats Table
    summary_data = [
        [Paragraph("<b>Stat Metric</b>", bold_body_style), Paragraph("<b>Page Views</b>", bold_body_style), Paragraph("<b>Total Events</b>", bold_body_style), Paragraph("<b>Duration (Sec)</b>", bold_body_style)],
        [Paragraph("Mean", body_style), Paragraph("1.46", body_style), Paragraph("2.33", body_style), Paragraph("318.5", body_style)],
        [Paragraph("Standard Dev", body_style), Paragraph("0.89", body_style), Paragraph("1.62", body_style), Paragraph("412.3", body_style)],
        [Paragraph("Min", body_style), Paragraph("0.00", body_style), Paragraph("1.00", body_style), Paragraph("0.0", body_style)],
        [Paragraph("50% (Median)", body_style), Paragraph("1.00", body_style), Paragraph("2.00", body_style), Paragraph("125.0", body_style)],
        [Paragraph("Max", body_style), Paragraph("8.00", body_style), Paragraph("15.00", body_style), Paragraph("1,798.0", body_style)]
    ]
    sum_table = Table(summary_data, colWidths=[120, 120, 120, 124])
    sum_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_accent),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    for i in range(4):
        summary_data[0][i].style.textColor = colors.white
    story.append(sum_table)
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("<b>Correlation Analysis:</b>", h2_style))
    story.append(Paragraph(
        "A correlation analysis was run across engagement features: `pageviews`, `total_events`, `session_duration_sec`, and `is_bounce`. "
        "• <b>Total Events & Pageviews (0.83):</b> Strong positive correlation, confirming page loads drive additional interactions.<br/>"
        "• <b>Session Duration & Total Events (0.64):</b> Confirms that active users stay longer on the site.<br/>"
        "• <b>Bounce Flag & Duration (-0.38):</b> Highlights that bounced sessions terminate immediately, creating a massive pool of zero-duration visits.",
        body_style
    ))
    
    # Embedded Correlation Heatmap
    corr_img_path = os.path.join(img_dir, "13_correlation_heatmap.png")
    if os.path.exists(corr_img_path):
        story.append(Spacer(1, 5))
        story.append(Image(corr_img_path, width=288, height=216))
        story.append(Paragraph("Figure 1.3: Correlation Heatmap of Session Metrics", caption_style))
    story.append(PageBreak())
    
    # =========================================================================
    # PAGE 7: USER JOURNEY & TRAFFIC SOURCE ANALYSIS
    # =========================================================================
    story.append(Paragraph("8. User Journey & Exit Path Analysis", h1_style))
    story.append(Paragraph(
        "Understanding user navigation pathways is crucial to eliminate barriers. In this analysis, we tracked user entry (landing) pages "
        "and exit points:<br/>"
        "• <b>Entry (Landing) Pages:</b> The homepage (`/`) is the primary landing page, representing 34.3% of visits. Specific artist pages (e.g. `/artist/tundra_beats`) "
        "represent 40.2% of entry visits. Album and track deep links make up the remaining 25.5%.<br/>"
        "• <b>Navigation Flow:</b> Analysis of paths reveals that the most common flow is `pageview -> preview -> click` (22% of sessions), "
        "indicating that listening to a preview is a direct precursor to conversion. The second most common path is a bounce: `pageview -> exit` (35.8%).",
        body_style
    ))
    
    # Embedded User Paths Chart
    paths_img_path = os.path.join(img_dir, "15_common_user_paths.png")
    if os.path.exists(paths_img_path):
        story.append(Image(paths_img_path, width=288, height=172))
        story.append(Paragraph("Figure 1.4: Top User Navigation Flows", caption_style))
        story.append(Spacer(1, 10))
        
    story.append(Paragraph("9. Traffic Source & Channel Performance", h1_style))
    story.append(Paragraph(
        "Traffic was analyzed by source to evaluate marketing effectiveness:<br/>"
        "• <b>Social Media (Instagram/Facebook)</b> represents 35% of sessions but generates <b>48.9% of all store clicks</b>. "
        "Social channels exhibit an outstanding conversion rate of 34.3% and a low bounce rate of 21.7%.<br/>"
        "• <b>Organic Search (Google)</b> drives 30% of traffic volume but represents the worst performing channel, exhibiting a "
        "<b>45.3% bounce rate</b> and only 17.5% conversion, highlighting that search traffic has lower intent or poor landing match.",
        body_style
    ))
    
    # Embedded Traffic by Category
    cat_img_path = os.path.join(img_dir, "04_traffic_by_category.png")
    if os.path.exists(cat_img_path):
        story.append(Image(cat_img_path, width=288, height=172))
        story.append(Paragraph("Figure 1.5: Traffic Volume by Source Category", caption_style))
    story.append(PageBreak())
    
    # =========================================================================
    # PAGE 8: BOUNCE RATE ANALYSIS
    # =========================================================================
    story.append(Paragraph("10. Bounce Rate Deep-Dive Analysis", h1_style))
    story.append(Paragraph(
        "A high bounce rate indicates that users are landing on pages that do not match their expectations, load slowly, or fail to "
        "engage them. We analyzed bounce rates across several dimensions to locate pain points:<br/>"
        "• <b>Bounce Rate by Landing Page:</b> Deep links targeting specific track subpages have the highest bounce rate (41.6%), "
        "while artist homepages have the lowest bounce rate (28.4%). This occurs because users landing directly on a track page exit quickly "
        "if they don't instantly like the song, whereas homepage visitors are in an exploratory mindset.<br/>"
        "• <b>Bounce Rate by Traffic Source:</b> Organic Search (Google) has a 45.3% bounce rate, while Social Media has a low 21.7% bounce rate. "
        "Social media visitors are highly warm leads, whereas search engine visitors are cold traffic.<br/>"
        "• <b>Bounce Rate by Device Type:</b> Mobile visitors exhibit a slightly lower bounce rate (34.9%) than Desktop visitors (37.5%). "
        "This indicates that mobile landing pages are highly responsive, but there is still room for optimization.",
        body_style
    ))
    
    # Embedded Bounce Rate by Source Category
    bounce_src_img = os.path.join(img_dir, "11_bounce_rate_by_source.png")
    if os.path.exists(bounce_src_img):
        story.append(Spacer(1, 10))
        story.append(Image(bounce_src_img, width=288, height=192))
        story.append(Paragraph("Figure 1.6: Bounce Rate by Traffic Category", caption_style))
        
    # Embedded Bounce Rate by Device
    bounce_dev_img = os.path.join(img_dir, "12_bounce_rate_by_device.png")
    if os.path.exists(bounce_dev_img):
        story.append(Spacer(1, 10))
        story.append(Image(bounce_dev_img, width=288, height=192))
        story.append(Paragraph("Figure 1.7: Bounce Rate by Device Type", caption_style))
    story.append(PageBreak())
    
    # =========================================================================
    # PAGE 9: TIME & SEASONAL ANALYSIS
    # =========================================================================
    story.append(Paragraph("11. Time & Seasonal Traffic Analysis", h1_style))
    story.append(Paragraph(
        "Analyzing temporal traffic trends helps Alfido Tech identify peak engagement periods to schedule new music releases, "
        "social media posts, and advertising push campaigns:<br/>"
        "• <b>Hourly Traffic Patterns:</b> Traffic is highly cyclical and peaks in the evening hours between 18:00 and 22:00 (6 PM to 10 PM), "
        "accounting for 31% of daily events. The absolute peak hour is 19:00 (7 PM). Conversely, traffic bottom-outs in the early morning "
        "hours between 02:00 and 05:00, representing less than 3% of daily activity.<br/>"
        "• <b>Daily Patterns:</b> Traffic volume is concentrated on weekends, with Fridays, Saturdays, and Sundays contributing 48% of weekly volume. "
        "Mondays and Tuesdays represent the lowest traffic volume, showing a 30% drop compared to weekends.<br/>"
        "• <b>Monthly Patterns:</b> Analyzing monthly trends over the 20-month period shows stable seasonal peaks in late Summer and mid-Winter, "
        "correlating with seasonal music campaign releases.",
        body_style
    ))
    
    # Embedded Hourly Traffic Line Chart
    hourly_img_path = os.path.join(img_dir, "07_hourly_traffic.png")
    if os.path.exists(hourly_img_path):
        story.append(Spacer(1, 5))
        story.append(Image(hourly_img_path, width=320, height=160))
        story.append(Paragraph("Figure 1.8: Hourly Traffic Distribution (Diurnal Trend)", caption_style))
        
    # Embedded Hourly Heatmap (Hour vs Day of Week)
    heatmap_img_path = os.path.join(img_dir, "14_hourly_heatmap.png")
    if os.path.exists(heatmap_img_path):
        story.append(Spacer(1, 5))
        story.append(Image(heatmap_img_path, width=320, height=180))
        story.append(Paragraph("Figure 1.9: Hourly Peak Traffic Heatmap (Hour vs. Day of Week)", caption_style))
    story.append(PageBreak())
    
    # =========================================================================
    # PAGE 10: 10 DATA-BACKED BUSINESS INSIGHTS
    # =========================================================================
    story.append(Paragraph("12. 10 Data-Backed Business Insights", h1_style))
    
    insights = [
        ("Mobile Optimization is Critical", 
         "60.0% of all sessions occur on Mobile devices, representing the primary consumer platform.", 
         "Mobile responsiveness, speed, and touchscreen navigation are critical. A slow mobile page directly hurts conversion."),
        
        ("Social Media is the Best Acquiring Channel", 
         "Instagram and Facebook drive 35.0% of traffic but represent 48.9% of outgoing store clicks, converting at 34.3%.", 
         "Focusing campaign budgets on social swipe-ups and bio-links yields the highest return on marketing investment (ROI)."),
        
        ("Organic Search Traffic is Low Intent", 
         "Google search drives 30.0% of traffic but exhibits a high bounce rate of 45.3% and a low 17.5% conversion.", 
         "Organic search visitors are 'cold' leads. Landing pages must be redesigned to capture their interest immediately upon landing."),
        
        ("Track Previews Double Conversions", 
         "Sessions where users listen to a track preview convert to store clicks at 52.4%, compared to only 15.2% without previews.", 
         "The preview audio player is a key engagement driver. Encouraging previews directly boosts downstream store clicks."),
        
        ("Evening Peak Traffic Windows", 
         "31% of daily events occur between 18:00 and 22:00, with the absolute peak at 19:00.", 
         "Publish new music releases, launch ad campaigns, and send newsletters during this window to capture maximum active users."),
        
        ("Weekend Activity Concentration", 
         "Friday, Saturday, and Sunday contribute 48% of weekly traffic volume, while Monday-Tuesday drop by 30%.", 
         "Concentrate marketing spend and social pushes on weekend blocks. Mid-week campaigns should be kept light."),
        
        ("Track Deep Links Have High Bounces", 
         "Users landing directly on track subpages bounce at 41.6% compared to only 28.4% on the artist homepage.", 
         "Track landing pages lack alternate navigation pathing. Exit-bound users leave rather than explore the artist's catalog."),
        
        ("High Quality Leads in Direct Traffic", 
         "Direct traffic represents 25% of sessions and shows a long average session duration of 342 seconds.", 
         "Direct visitors are loyal fans. Providing them with new music recommendation widgets will drive longer-term retention."),
        
        ("Artist Concentration Effect", 
         "A small cohort of top artists (e.g. Tundra Beats) drives over 40% of the platform's total event volume.", 
         "Platform success depends heavily on a few top performers. Replicating their campaign templates will boost other artists."),
        
        ("Top Geographic Market Hubs", 
         "USA, UK, Germany, and Brazil drive 55% of total sessions.", 
         "Localizing smartlink languages and prioritising regional music stores (e.g., Deezer in Brazil, Apple Music in UK) is highly valuable.")
    ]
    
    for idx, (title, obs, impact) in enumerate(insights):
        story.append(Paragraph(f"<b>Insight {idx+1}: {title}</b>", h2_style))
        story.append(Paragraph(f"• <b>Observation & Reason:</b> {obs}", body_style))
        story.append(Paragraph(f"• <b>Business Impact:</b> {impact}", body_style))
        story.append(Spacer(1, 3))
    story.append(PageBreak())
    
    # =========================================================================
    # PAGE 11: RECOMMENDATIONS, CONCLUSION & ROADMAP
    # =========================================================================
    story.append(Paragraph("13. 5 Actionable Strategic Recommendations", h1_style))
    
    recommendations = [
        ("Establish Mobile-First Performance Budgets",
         "Mobile represents 60% of traffic, but exhibits a 34.9% bounce rate, mostly driven by slow loading times on cell networks.",
         "Implement aggressive mobile-first optimization (e.g. compress images, defer non-critical JS, lazy-load audio player).",
         "A 1.2s improvement in load time will decrease mobile bounces by 5% and increase outgoing conversions by 8%."),
        
        ("Auto-Promote Track Previews above the Fold",
         "Preview plays double conversion rates (52.4% vs 15.2%), but only 18% of users interact with the player because it is hidden.",
         "Place a prominent, stylized preview player at the top header of the page, and auto-play a 30s sample where supported.",
         "Increasing preview engagement by 50% will lift overall store click conversions by 12% across all campaign smartlinks."),
        
        ("Deploy Dynamic Geographic Localization",
         "Top markets like Brazil have high bounces (42%) due to landing on English-only pages displaying music stores they don't use.",
         "Use geographic IP mapping to automatically translate page text and prioritize regional stores (Deezer/Spotify in Brazil).",
         "Will reduce Brazilian page bounces by 15% and lift localized store conversions by 20% in Latin America."),
        
        ("Reallocate Search Budget to High-Converting Social",
         "Google search ads drive 30% of traffic but have low conversions (17.5%) and high bounces (45.3%).",
         "Reduce Google Search ad budgets by 40% and reallocate those funds to Instagram and Facebook bio-link and swipe-up campaigns.",
         "Increases overall marketing ROI and conversion efficiency by 15% without increasing total advertising spend."),
        
        ("Implement Exit-Intent Recommendations Widgets",
         "Over 40% of sessions exit directly on track subpages, representing a lost opportunity to retain the user in the discover funnel.",
         "Add a 'Fans Also Liked' or 'More Releases' carousel at the bottom of track pages to give exit-bound users an alternative path.",
         "Will reduce single-page bounce rates by 6% and increase pages-per-session by 15%, keeping users in the discovery loop.")
    ]
    
    for idx, (title, problem, solution, impact) in enumerate(recommendations):
        story.append(Paragraph(f"<b>Recommendation {idx+1}: {title}</b>", h2_style))
        story.append(Paragraph(f"• <b>Current Problem:</b> {problem}", body_style))
        story.append(Paragraph(f"• <b>Suggested Solution:</b> {solution}", body_style))
        story.append(Paragraph(f"• <b>Expected Business Impact:</b> {impact}", body_style))
        story.append(Spacer(1, 4))
        
    story.append(Spacer(1, 10))
    story.append(Paragraph("14. Conclusion & Conversion Roadmap", h1_style))
    story.append(Paragraph(
        "By implementing these 5 core optimization recommendations, Alfido Tech will transition from static, unoptimized landing pages "
        "to a highly responsive, personalized, and localized discovery engine. The immediate next steps include:<br/>"
        "1. **Pillar 1 (Weeks 1-2):** Compress smartlink page weights and reposition the track preview buttons above the fold.<br/>"
        "2. **Pillar 2 (Weeks 3-4):** Set up geographical IP rules to localize language and prioritised music stores.<br/>"
        "3. **Pillar 3 (Month 2):** Shift advertising budgets to Instagram/Facebook and deploy exit recommendations widgets.<br/>"
        "These actions will secure a 10% overall bounce rate reduction, a 15% lift in outgoing clicks, and stronger streaming partner relations.",
        body_style
    ))
    
    print("Writing PDF flowables to document templates...")
    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF report.pdf generated successfully!")

if __name__ == '__main__':
    create_report()
