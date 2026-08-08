"""
extract_kpis.py  –  Reads cleaned_dataset.csv and prints real KPIs as JSON.
Run with the venv python.
"""
import json, os, sys
import pandas as pd
import numpy as np

BASE = r"c:\Users\vadla\OneDrive\Documents\internship\Website-Traffic-Analysis"
df = pd.read_csv(os.path.join(BASE, "cleaned_dataset.csv"))
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["date"]      = pd.to_datetime(df["date"])
df["hour"]      = df["timestamp"].dt.hour
df["day_of_week"] = df["timestamp"].dt.day_name()

# ── session metrics ──────────────────────────────────────────────────────────
sm = df.groupby("session_id").agg(
    user_id      = ("user_id",  "first"),
    start_time   = ("timestamp","min"),
    end_time     = ("timestamp","max"),
    pageviews    = ("event",    lambda x:(x=="pageview").sum()),
    total_events = ("event",    "count"),
    landing_page = ("page_url", "first"),
    exit_page    = ("page_url", "last"),
    device       = ("device",   "first"),
    traffic_source     = ("traffic_source","first"),
    traffic_category   = ("traffic_category","first"),
).reset_index()

sm["session_duration_sec"] = (sm["end_time"]-sm["start_time"]).dt.total_seconds()
sm["is_bounce"] = (sm["total_events"]==1) & (sm["pageviews"]==1)

# ── core KPIs ────────────────────────────────────────────────────────────────
total_sessions   = len(sm)
total_users      = df["user_id"].nunique()
total_pageviews  = int((df["event"]=="pageview").sum())
total_clicks     = int((df["event"]=="click").sum())
total_previews   = int((df["event"]=="preview").sum())
bounce_rate      = round(sm["is_bounce"].mean()*100, 2)
avg_duration     = round(sm["session_duration_sec"].mean(), 1)
avg_pages        = round(sm["pageviews"].mean(), 2)
conv_sessions    = df[df["event"]=="click"]["session_id"].nunique()
conv_rate        = round(conv_sessions/total_sessions*100, 2)

# returning / new users
usr_sess = sm.groupby("user_id").size()
new_users       = int((usr_sess==1).sum())
returning_users = int((usr_sess>1).sum())

# top pages / sources
top_landing = sm["landing_page"].value_counts().head(5).to_dict()
top_exit    = sm["exit_page"].value_counts().head(5).to_dict()
top_src     = df["traffic_source"].value_counts().head(5).to_dict()
top_cat     = df["traffic_category"].value_counts().head(5).to_dict()
top_country = df["country"].value_counts().head(5).to_dict()
top_device  = df["device"].value_counts().to_dict()
top_event   = df["event"].value_counts().to_dict()

# bounce by source
bounce_by_src = sm.groupby("traffic_category").apply(
    lambda g: round(g["is_bounce"].mean()*100,2)).to_dict()

# bounce by device
bounce_by_dev = sm.groupby("device").apply(
    lambda g: round(g["is_bounce"].mean()*100,2)).to_dict()

# hourly traffic
hourly = df["hour"].value_counts().sort_index().to_dict()
peak_hour = int(df["hour"].value_counts().idxmax())
low_hour  = int(df["hour"].value_counts().idxmin())

# daily traffic
day_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
daily = df["day_of_week"].value_counts().reindex(day_order).fillna(0).astype(int).to_dict()

# monthly traffic
df["month_str"] = df["timestamp"].dt.to_period("M").astype(str)
monthly = df["month_str"].value_counts().sort_index().to_dict()

# category performance
cat_perf = {}
for cat, g in sm.groupby("traffic_category"):
    conv_s = df[(df["event"]=="click") & (df["traffic_category"]==cat)]["session_id"].nunique()
    cat_perf[cat] = {
        "sessions": len(g),
        "bounce_rate": round(g["is_bounce"].mean()*100, 2),
        "avg_duration": round(g["session_duration_sec"].mean(), 1),
        "conversion_rate": round(conv_s/len(g)*100, 2) if len(g) else 0,
    }

# raw dataset shape
df_raw = pd.read_csv(os.path.join(BASE, "dataset", "traffic.csv"))

result = {
    "raw_rows": len(df_raw), "raw_cols": len(df_raw.columns),
    "clean_rows": len(df), "clean_cols": len(df.columns),
    "duplicates_removed": len(df_raw)-len(df_raw.drop_duplicates()),
    "date_min": str(df["date"].min().date()),
    "date_max": str(df["date"].max().date()),
    "countries": int(df["country"].nunique()),
    "cities":    int(df["city"].nunique()),
    "artists":   int(df["artist"].nunique()),
    "total_sessions": total_sessions,
    "total_users": total_users,
    "new_users": new_users,
    "returning_users": returning_users,
    "total_pageviews": total_pageviews,
    "total_clicks": total_clicks,
    "total_previews": total_previews,
    "bounce_rate": bounce_rate,
    "avg_duration_sec": avg_duration,
    "avg_duration_min": round(avg_duration/60, 2),
    "avg_pages_per_session": avg_pages,
    "conversion_rate": conv_rate,
    "top_landing": top_landing,
    "top_exit":    top_exit,
    "top_sources": top_src,
    "top_categories": top_cat,
    "top_countries": top_country,
    "top_devices":  top_device,
    "top_events":   top_event,
    "bounce_by_source": bounce_by_src,
    "bounce_by_device": bounce_by_dev,
    "peak_hour": peak_hour,
    "low_hour":  low_hour,
    "hourly_traffic": hourly,
    "daily_traffic":  daily,
    "monthly_traffic": monthly,
    "category_performance": cat_perf,
}
print(json.dumps(result, indent=2))
