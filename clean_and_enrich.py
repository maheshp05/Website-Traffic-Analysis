import pandas as pd
import numpy as np
import os
import re

def clean_slug(val):
    if not isinstance(val, str):
        return 'unknown'
    val = val.lower()
    val = re.sub(r'[^a-z0-9\s-]', '', val) # remove special chars
    val = re.sub(r'[\s-]+', '_', val) # replace spaces/dashes with underscore
    return val.strip('_')

def main():
    print("Starting data cleaning and enrichment...")
    
    # Define paths
    raw_path = r"c:\Users\vadla\OneDrive\Documents\internship\Website-Traffic-Analysis\dataset\traffic.csv"
    output_path = r"c:\Users\vadla\OneDrive\Documents\internship\Website-Traffic-Analysis\cleaned_dataset.csv"
    
    # 1. Load dataset
    print("Loading dataset...")
    df = pd.read_csv(raw_path)
    print(f"Loaded {len(df)} rows and {len(df.columns)} columns.")
    
    # 2. Data Cleaning
    print("Removing duplicates and handling missing values...")
    # Drop duplicates if any
    before_dups = len(df)
    df = df.drop_duplicates()
    after_dups = len(df)
    print(f"Removed {before_dups - after_dups} duplicate rows.")
    
    # Fill missing values
    df['country'] = df['country'].fillna('Unknown')
    df['city'] = df['city'].fillna('Unknown')
    df['artist'] = df['artist'].fillna('Unknown')
    df['album'] = df['album'].fillna('Unknown')
    df['track'] = df['track'].fillna('Unknown')
    df['isrc'] = df['isrc'].fillna('Unknown')
    
    # 3. Timestamp Simulation
    print("Simulating timestamps with diurnal patterns...")
    # Diurnal hourly probability distribution (peaking in evening, low in early morning)
    hourly_probs = [
        0.015, 0.010, 0.005, 0.005, 0.005, 0.010, # 00:00 - 05:00
        0.020, 0.035, 0.050, 0.060, 0.065, 0.070, # 06:00 - 11:00
        0.070, 0.065, 0.060, 0.055, 0.060, 0.070, # 12:00 - 17:00
        0.080, 0.085, 0.080, 0.065, 0.045, 0.025  # 18:00 - 23:00
    ]
    # Normalize hourly probabilities to sum to 1
    hourly_probs = np.array(hourly_probs) / sum(hourly_probs)
    
    np.random.seed(42)
    n_rows = len(df)
    hours = np.random.choice(range(24), size=n_rows, p=hourly_probs)
    minutes = np.random.randint(0, 60, size=n_rows)
    seconds = np.random.randint(0, 60, size=n_rows)
    
    # Add timestamps
    df['timestamp'] = pd.to_datetime(df['date']) + pd.to_timedelta(hours, unit='h') + \
                       pd.to_timedelta(minutes, unit='m') + pd.to_timedelta(seconds, unit='s')
    
    # 4. User ID Simulation
    print("Generating user IDs based on country and city groups...")
    # Group by country/city and determine number of synthetic users
    group_id = df.groupby(['country', 'city']).ngroup()
    # Determine size of each group
    group_sizes = df.groupby(['country', 'city']).transform('size')
    
    # Determine user count per group (approx 6.6 events per user on average)
    # Clip to at least 1, max is based on size
    user_count_per_group = (group_sizes * 0.15).astype(int).clip(1)
    
    # Assign user indices within groups deterministically
    np.random.seed(42)
    user_idx = np.random.randint(0, user_count_per_group, size=len(df))
    df['user_id'] = 'U_' + group_id.astype(str) + '_' + pd.Series(user_idx).astype(str)
    
    # 5. Session ID Simulation
    print("Generating session IDs based on 30-minute inactivity window...")
    df = df.sort_values(by=['user_id', 'timestamp']).reset_index(drop=True)
    time_diff = df.groupby('user_id')['timestamp'].diff()
    new_session = (time_diff.isnull()) | (time_diff > pd.Timedelta(minutes=30))
    df['session_id'] = 'S_' + new_session.cumsum().astype(str).str.zfill(6)
    
    # 6. Device Allocation
    print("Allocating device types...")
    np.random.seed(42)
    devices = np.random.choice(['Mobile', 'Desktop', 'Tablet'], size=len(df), p=[0.60, 0.30, 0.10])
    df['device'] = devices
    
    # 7. Traffic Source & Traffic Category Allocation
    print("Allocating traffic sources and categories...")
    np.random.seed(42)
    sources = np.random.choice(
        ['Google', 'Direct', 'Instagram', 'Facebook', 'YouTube', 'Referral_Blog'],
        size=len(df),
        p=[0.30, 0.25, 0.20, 0.15, 0.05, 0.05]
    )
    df['traffic_source'] = sources
    source_map = {
        'Google': 'Organic Search',
        'Direct': 'Direct',
        'Instagram': 'Social Media',
        'Facebook': 'Social Media',
        'YouTube': 'Social Media',
        'Referral_Blog': 'Referral'
    }
    df['traffic_category'] = df['traffic_source'].map(source_map)
    
    # 8. Page URL Generation based on Artist, Album, Track
    print("Generating clean page URLs...")
    # Pre-map unique values to clean slugs for performance
    unique_artists = {a: clean_slug(a) for a in df['artist'].unique()}
    unique_albums = {a: clean_slug(a) for a in df['album'].unique()}
    unique_tracks = {t: clean_slug(t) for t in df['track'].unique()}
    
    df['artist_slug'] = df['artist'].map(unique_artists)
    df['album_slug'] = df['album'].map(unique_albums)
    df['track_slug'] = df['track'].map(unique_tracks)
    
    # Randomly select a page type for pageviews (25% home, 40% artist, 20% album, 15% track)
    np.random.seed(42)
    page_types = np.random.choice(['home', 'artist', 'album', 'track'], size=len(df), p=[0.25, 0.40, 0.20, 0.15])
    df['page_type'] = page_types
    
    # Adjust page types to fit event logic:
    # - Previews must be on a track page
    df.loc[df['event'] == 'preview', 'page_type'] = 'track'
    # - Clicks represent outgoing clicks and must happen on an artist, album, or track page, not home
    clicks_mask = df['event'] == 'click'
    df.loc[clicks_mask & (df['page_type'] == 'home'), 'page_type'] = 'artist'
    
    # Construct paths
    home_path = '/'
    artist_path = '/artist/' + df['artist_slug']
    album_path = '/artist/' + df['artist_slug'] + '/album/' + df['album_slug']
    track_path = '/artist/' + df['artist_slug'] + '/track/' + df['track_slug']
    
    df['page_url'] = '/'
    df.loc[df['page_type'] == 'home', 'page_url'] = home_path
    df.loc[df['page_type'] == 'artist', 'page_url'] = artist_path
    df.loc[df['page_type'] == 'album', 'page_url'] = album_path
    df.loc[df['page_type'] == 'track', 'page_url'] = track_path
    
    # Drop temp slug and page type columns to keep dataset clean
    df = df.drop(columns=['artist_slug', 'album_slug', 'track_slug', 'page_type'])
    
    # Sort dataset by timestamp for chronologically ordered analysis
    df = df.sort_values(by='timestamp').reset_index(drop=True)
    
    # 9. Save Cleaned & Enriched Dataset
    print(f"Saving cleaned and enriched dataset to {output_path}...")
    df.to_csv(output_path, index=False)
    print("Cleaned and enriched dataset generated successfully!")
    print(f"Final shape: {df.shape}")
    print("Sample rows:")
    print(df.head())

if __name__ == '__main__':
    main()
