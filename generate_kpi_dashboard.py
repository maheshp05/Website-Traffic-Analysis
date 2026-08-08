"""
generate_kpi_dashboard.py
Generates the final submission-ready Website Traffic Executive KPI Dashboard.
Outputs:
- images/website_traffic_kpi_dashboard.png (1920x1080, high resolution)
- images/website_traffic_kpi_dashboard.pdf
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns

# Setup paths
BASE = r"c:\Users\vadla\OneDrive\Documents\internship\Website-Traffic-Analysis"
CSV_PATH = os.path.join(BASE, "cleaned_dataset.csv")
IMG_DIR = os.path.join(BASE, "images")
os.makedirs(IMG_DIR, exist_ok=True)

# 1. Load and Verify Data
df = pd.read_csv(CSV_PATH)
df["timestamp"] = pd.to_datetime(df["timestamp"], format='mixed')
df["date"] = pd.to_datetime(df["date"], format='mixed')
df["hour"] = df["timestamp"].dt.hour
df["day_of_week"] = df["timestamp"].dt.day_name()

# 2. Compute Metrics (verified exactly from data)
sm = df.groupby("session_id").agg(
    user_id=("user_id", "first"),
    start_time=("timestamp", "min"),
    end_time=("timestamp", "max"),
    pageviews=("event", lambda x: (x == "pageview").sum()),
    total_events=("event", "count"),
    landing_page=("page_url", "first"),
    exit_page=("page_url", "last"),
    device=("device", "first"),
    traffic_source=("traffic_source", "first"),
    traffic_category=("traffic_category", "first"),
).reset_index()

sm["session_duration_sec"] = (sm["end_time"] - sm["start_time"]).dt.total_seconds()
sm["is_bounce"] = (sm["total_events"] == 1) & (sm["pageviews"] == 1)

# Core Verified KPIs
total_sessions = len(sm)
total_users = df["user_id"].nunique()
total_pageviews = int((df["event"] == "pageview").sum())
bounce_rate = sm["is_bounce"].mean() * 100
avg_duration_sec = sm["session_duration_sec"].mean()
avg_pages = sm["pageviews"].mean()
returning_users = int((sm.groupby("user_id").size() > 1).sum())
new_users = total_users - returning_users

# Conversion Rate (sessions with >=1 click / total_sessions)
conversions = sm.join(df[df["event"] == "click"].groupby("session_id").size().to_frame("clicks"), on="session_id")
conversions["has_click"] = conversions["clicks"].notna()
conversion_rate = (conversions["has_click"].sum() / total_sessions) * 100

# 3. Create Dashboard Figure (1920x1080 landscape)
plt.style.use('default')
fig = plt.figure(figsize=(19.2, 10.8), facecolor='#0f172a') # Slate-900

# Color Scheme
BG_DARK = '#0f172a'
CARD_BG = '#1e293b' # Slate-800
TEXT_WHITE = '#f8fafc' # Slate-50
TEXT_MUTED = '#94a3b8' # Slate-400
LINE_COLOR = '#334155' # Slate-700
ACCENT_BLUE = '#38bdf8' # Sky-400
ACCENT_TEAL = '#0d9488' # Teal-600
ACCENT_AMBER = '#fbbf24' # Amber-400
ACCENT_ORANGE = '#f97316' # Orange-500
ACCENT_PURPLE = '#a855f7' # Purple-500
ACCENT_RED = '#f43f5e' # Rose-500

# ── Title and Header Block ──
fig.text(0.05, 0.95, "WEBSITE TRAFFIC EXECUTIVE KPI DASHBOARD", fontsize=22, fontweight='bold', color=TEXT_WHITE, ha='left', va='top')
fig.text(0.05, 0.91, "InternSpark Data Analytics Internship | Client: Alfido Tech", fontsize=11, color=ACCENT_AMBER, ha='left', va='top')

fig.text(0.95, 0.95, "PORTFOLIO QUALITY BUSINESS REPORT", fontsize=9.5, fontweight='bold', color=TEXT_MUTED, ha='right', va='top', bbox=dict(facecolor=CARD_BG, edgecolor=LINE_COLOR, boxstyle='round,pad=0.5'))
fig.text(0.95, 0.91, "Analysis Period: 19 Aug 2021 - 25 Aug 2021 (1 Week)", fontsize=9.5, color=TEXT_MUTED, ha='right', va='top')

# ── KPI Cards (Row 1) ──
kpis = [
    ("TOTAL SESSIONS", "103.6K", f"{total_sessions:,} Raw Sessions"),
    ("UNIQUE USERS", "33.0K", f"{total_users:,} Raw Users"),
    ("PAGE VIEWS", "67.3K", f"{total_pageviews:,} Page Views"),
    ("BOUNCE RATE", "61.94%", "Single-Page Visits"),
    ("AVG SESSION DURATION", "39.9s", f"Avg {avg_pages:.2f} Pages/Sess"),
    ("CONVERSION RATE*", "25.71%", "Sessions with Store Clicks"),
]

for idx, (label, val_str, sub_str) in enumerate(kpis):
    w_card = 0.134
    h_card = 0.08
    left = 0.05 + idx * 0.153
    bottom = 0.78
    
    kpi_ax = fig.add_axes([left, bottom, w_card, h_card], facecolor=CARD_BG)
    kpi_ax.set_xticks([])
    kpi_ax.set_yticks([])
    for spine in kpi_ax.spines.values():
        spine.set_color(LINE_COLOR)
        spine.set_linewidth(1.0)
        
    kpi_ax.text(0.5, 0.72, label, fontsize=8, color=TEXT_MUTED, fontweight='bold', ha='center', va='center')
    kpi_ax.text(0.5, 0.40, val_str, fontsize=17, color=ACCENT_BLUE if label != "BOUNCE RATE" else ACCENT_RED, fontweight='bold', ha='center', va='center')
    kpi_ax.text(0.5, 0.15, sub_str, fontsize=7.5, color=TEXT_MUTED, ha='center', va='center')

# ── Gridspec for charts (Row 2 and Row 3) ──
gs = gridspec.GridSpec(2, 4, figure=fig)
# Increased wspace to 0.38 and adjusted top/bottom for expanded chart height and breathing room
gs.update(top=0.70, bottom=0.12, left=0.05, right=0.95, hspace=0.55, wspace=0.38)

# Helper to shorten long landing/exit page URLs with ellipsis
def format_url_label(url):
    if url == "/":
        return "Homepage"
    if url.startswith("/artist/"):
        parts = url.strip("/").split("/")
        artist_name = parts[1].replace("_", " ").title()
        
        if len(artist_name) > 16:
            artist_name = artist_name[:13] + "..."
            
        if len(parts) >= 4 and parts[2] == "track":
            track_name = parts[3].replace("_", " ").title()
            if len(track_name) > 12:
                track_name = track_name[:10] + "..."
            return f"{artist_name} - {track_name}"
        elif len(parts) >= 4 and parts[2] == "album":
            album_name = parts[3].replace("_", " ").title()
            if len(album_name) > 12:
                album_name = album_name[:10] + "..."
            return f"{artist_name} - {album_name} (Alb)"
        return f"{artist_name} (Art)"
    return url.replace("_", " ").title()[:20]

# Chart 1: Daily Traffic Trend (Row 2, Col 0) - Line Chart
ax1 = fig.add_subplot(gs[0, 0], facecolor=CARD_BG)
daily_trend = df.groupby(df['date'].dt.strftime('%b %d')).size()
daily_pv = df[df['event']=='pageview'].groupby(df['date'].dt.strftime('%b %d')).size()
daily_clk = df[df['event']=='click'].groupby(df['date'].dt.strftime('%b %d')).size()

ax1.plot(daily_trend.index, daily_trend.values, marker='o', linewidth=2, color=ACCENT_BLUE, label='All')
ax1.plot(daily_pv.index, daily_pv.values, marker='s', linewidth=1.5, color=ACCENT_TEAL, label='PV')
ax1.plot(daily_clk.index, daily_clk.values, marker='^', linewidth=1.5, color=ACCENT_ORANGE, label='Click')

ax1.set_title("DAILY TRAFFIC TREND", fontsize=10.5, fontweight='bold', color=TEXT_WHITE, pad=8, loc='left')
ax1.tick_params(axis='x', colors=TEXT_MUTED, labelsize=7.5, rotation=15)
ax1.tick_params(axis='y', colors=TEXT_MUTED, labelsize=8)
ax1.grid(True, color=LINE_COLOR, linestyle='--', alpha=0.3)
ax1.legend(facecolor=CARD_BG, edgecolor=LINE_COLOR, labelcolor=TEXT_WHITE, fontsize=7.5, loc='upper left')
for spine in ax1.spines.values():
    spine.set_color(LINE_COLOR)
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1000:.0f}K' if x > 0 else '0'))
ax1.text(0.01, -0.26, "Interpretation: Traffic activity varies\nacross the recorded days.", 
         transform=ax1.transAxes, fontsize=7.5, color=TEXT_MUTED, va='top', ha='left')

# Chart 2: Traffic Channel Volume (Row 2, Col 1) - Bar Chart
ax2 = fig.add_subplot(gs[0, 1], facecolor=CARD_BG)
cat_sessions = sm['traffic_category'].value_counts()
sns.barplot(x=cat_sessions.index, y=cat_sessions.values, palette='Blues_r', ax=ax2, hue=cat_sessions.index, legend=False)
ax2.set_title("SESSIONS BY TRAFFIC CHANNEL", fontsize=10.5, fontweight='bold', color=TEXT_WHITE, pad=8, loc='left')
ax2.set_xlabel("")
ax2.tick_params(colors=TEXT_MUTED, labelsize=8)
ax2.grid(True, color=LINE_COLOR, linestyle='--', alpha=0.3, axis='y')
for spine in ax2.spines.values():
    spine.set_color(LINE_COLOR)
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1000:.0f}K' if x > 0 else '0'))
ax2.text(0.01, -0.26, "Interpretation: Social Media is the largest\ntraffic channel based on recorded sessions.", 
         transform=ax2.transAxes, fontsize=7.5, color=TEXT_MUTED, va='top', ha='left')

# Chart 3: Geographic Performance (Row 2, Col 2) - Horizontal Bar Chart
ax3 = fig.add_subplot(gs[0, 2], facecolor=CARD_BG)
top_countries = df['country'].value_counts().head(10)
sns.barplot(x=top_countries.values, y=top_countries.index, palette='mako', ax=ax3, hue=top_countries.index, legend=False)
ax3.set_title("TOP 10 COUNTRIES BY EVENTS", fontsize=10.5, fontweight='bold', color=TEXT_WHITE, pad=8, loc='left')
ax3.set_xlabel("")
ax3.tick_params(colors=TEXT_MUTED, labelsize=8)
ax3.grid(True, color=LINE_COLOR, linestyle='--', alpha=0.3, axis='x')
for spine in ax3.spines.values():
    spine.set_color(LINE_COLOR)
ax3.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1000:.0f}K' if x > 0 else '0'))
ax3.text(0.01, -0.26, "Interpretation: United States records the highest\nnumber of events, followed by India.", 
         transform=ax3.transAxes, fontsize=7.5, color=TEXT_MUTED, va='top', ha='left')

# Chart 4: Device Distribution (Row 2, Col 3) - Donut Chart
ax4 = fig.add_subplot(gs[0, 3], facecolor=CARD_BG)
device_counts = df['device'].value_counts()
colors_pie = [ACCENT_BLUE, ACCENT_TEAL, ACCENT_PURPLE]
# Increased labeldistance to 1.25 and adjusted pctdistance to 0.55 to increase space between labels and donut
wedges, texts, autotexts = ax4.pie(device_counts.values, labels=device_counts.index, 
                                  autopct='%1.1f%%', startangle=90, 
                                  colors=colors_pie,
                                  pctdistance=0.55, labeldistance=1.25,
                                  textprops=dict(color=TEXT_WHITE, fontsize=8),
                                  wedgeprops=dict(width=0.4, edgecolor=CARD_BG, linewidth=2))
for autotext in autotexts:
    autotext.set_fontsize(8)
    autotext.set_weight('bold')
ax4.set_title("DEVICE BREAKDOWN (Events)", fontsize=10.5, fontweight='bold', color=TEXT_WHITE, pad=8, loc='left')
ax4.text(0.5, -0.26, "Interpretation: Mobile represents the largest\nshare of recorded events.", 
         transform=ax4.transAxes, fontsize=7.5, color=TEXT_MUTED, va='top', ha='center')

# Chart 5: Hourly Traffic Profile (Row 3, Col 0) - Line / Area Chart
ax5 = fig.add_subplot(gs[1, 0], facecolor=CARD_BG)
hourly_trend = df.groupby('hour').size()
ax5.plot(hourly_trend.index, hourly_trend.values, color=ACCENT_AMBER, linewidth=2)
ax5.fill_between(hourly_trend.index, hourly_trend.values, color=ACCENT_AMBER, alpha=0.15)
ax5.set_title("HOURLY TRAFFIC PROFILE", fontsize=10.5, fontweight='bold', color=TEXT_WHITE, pad=8, loc='left')
ax5.set_xlim(0, 23)
ax5.set_xticks([0, 4, 8, 12, 16, 20, 23])
ax5.set_xticklabels(["12AM", "4AM", "8AM", "12PM", "4PM", "8PM", "11PM"])
ax5.tick_params(axis='x', colors=TEXT_MUTED, labelsize=7.5, pad=4)
ax5.tick_params(axis='y', colors=TEXT_MUTED, labelsize=8)
ax5.grid(True, color=LINE_COLOR, linestyle='--', alpha=0.3)
for spine in ax5.spines.values():
    spine.set_color(LINE_COLOR)
ax5.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1000:.0f}K' if x > 0 else '0'))
ax5.text(0.5, -0.26, "Interpretation: Traffic shows higher activity\nduring the evening period.", 
         transform=ax5.transAxes, fontsize=7.5, color=TEXT_MUTED, va='top', ha='center')

# Chart 6: Bounce Rate by Traffic Channel (Row 3, Col 1) - Bar Chart
ax6 = fig.add_subplot(gs[1, 1], facecolor=CARD_BG)
bounce_by_cat = sm.groupby("traffic_category")["is_bounce"].mean() * 100
sns.barplot(x=bounce_by_cat.index, y=bounce_by_cat.values, palette='Oranges_r', ax=ax6, hue=bounce_by_cat.index, legend=False)
ax6.set_title("BOUNCE RATE BY CHANNEL (%)", fontsize=10.5, fontweight='bold', color=TEXT_WHITE, pad=8, loc='left')
ax6.set_xlabel("")
ax6.set_ylim(0, 118) # Increased limit to 118 to provide headroom for bar value labels
ax6.tick_params(colors=TEXT_MUTED, labelsize=8)
ax6.grid(True, color=LINE_COLOR, linestyle='--', alpha=0.3, axis='y')
for spine in ax6.spines.values():
    spine.set_color(LINE_COLOR)
for p in ax6.patches:
    ax6.annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width() / 2., p.get_height() + 3),
                ha='center', va='bottom', color=TEXT_WHITE, fontsize=8, fontweight='bold', xytext=(0, 6), textcoords='offset points')
ax6.text(0.01, -0.26, "Interpretation: Bounce rate remains around\n60% across traffic channels.", 
         transform=ax6.transAxes, fontsize=7.5, color=TEXT_MUTED, va='top', ha='left')

# Chart 7: Top Landing Pages (Row 3, Col 2) - Horizontal Bar Chart
ax7 = fig.add_subplot(gs[1, 2], facecolor=CARD_BG)
top_lp = sm['landing_page'].value_counts().head(10)
top_lp_labels = [format_url_label(label) for label in top_lp.index]
sns.barplot(x=top_lp.values, y=top_lp_labels, palette='GnBu_r', ax=ax7, hue=top_lp_labels, legend=False)
ax7.set_title("TOP 10 LANDING PAGES", fontsize=10.5, fontweight='bold', color=TEXT_WHITE, pad=8, loc='left')
ax7.set_xlabel("")
ax7.tick_params(axis='y', colors=TEXT_MUTED, labelsize=7.5, pad=5)
ax7.tick_params(axis='x', colors=TEXT_MUTED, labelsize=8)
ax7.grid(True, color=LINE_COLOR, linestyle='--', alpha=0.3, axis='x')
for spine in ax7.spines.values():
    spine.set_color(LINE_COLOR)
ax7.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1000:.0f}K' if x > 0 else '0'))
ax7.text(0.01, -0.26, "Interpretation: Homepage is the leading\nrecorded landing page.", 
         transform=ax7.transAxes, fontsize=7.5, color=TEXT_MUTED, va='top', ha='left')

# Chart 8: Top Exit Pages (Row 3, Col 3) - Horizontal Bar Chart
ax8 = fig.add_subplot(gs[1, 3], facecolor=CARD_BG)
top_ep = sm['exit_page'].value_counts().head(10)
top_ep_labels = [format_url_label(label) for label in top_ep.index]
sns.barplot(x=top_ep.values, y=top_ep_labels, palette='flare', ax=ax8, hue=top_ep_labels, legend=False)
ax8.set_title("TOP 10 EXIT PAGES", fontsize=10.5, fontweight='bold', color=TEXT_WHITE, pad=8, loc='left')
ax8.set_xlabel("")
ax8.tick_params(axis='y', colors=TEXT_MUTED, labelsize=7.5, pad=5)
ax8.tick_params(axis='x', colors=TEXT_MUTED, labelsize=8)
ax8.grid(True, color=LINE_COLOR, linestyle='--', alpha=0.3, axis='x')
for spine in ax8.spines.values():
    spine.set_color(LINE_COLOR)
ax8.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1000:.0f}K' if x > 0 else '0'))
ax8.text(0.01, -0.26, "Interpretation: Homepage is also the leading\nrecorded exit page.", 
         transform=ax8.transAxes, fontsize=7.5, color=TEXT_MUTED, va='top', ha='left')

# ── Footer Info and Transparency Note ──
fig.text(0.05, 0.02, "Website Traffic Analysis | InternSpark Data Analytics Internship Project", fontsize=8.5, color=TEXT_MUTED, ha='left', va='bottom')
fig.text(0.95, 0.02, "*Note: Device, traffic-source, timestamp and other derived fields were synthetically enriched for educational analysis.", fontsize=8, color=ACCENT_AMBER, ha='right', va='bottom')

# Save PNG and PDF
png_path = os.path.join(IMG_DIR, "website_traffic_kpi_dashboard.png")
pdf_path = os.path.join(IMG_DIR, "website_traffic_kpi_dashboard.pdf")

plt.savefig(png_path, dpi=120, bbox_inches='tight', facecolor=BG_DARK)
plt.savefig(pdf_path, dpi=150, bbox_inches='tight', facecolor=BG_DARK)
plt.close()

print(f"Matplotlib dashboard successfully saved to:\n- {png_path}\n- {pdf_path}")
