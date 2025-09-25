"""
DAY 1 - MTA Datathon
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# STEP 1: DOWNLOADED DATASET
DATA_FILE = "/Users/sneharoy/Downloads/Datathon/data/MTA_Bus_Automated_Camera_Enforcement_Violations__Beginning_October_2019_20250922.csv"

print("🚌 MTA Datathon - Day 1 Quick Analysis")
print("=" * 40)


# STEP 2: LOAD THE DATA
print("📊 Loading your filtered MTA dataset...")

# Load with progress indication
import time
start_time = time.time()

df = pd.read_csv(DATA_FILE)

load_time = time.time() - start_time
print(f"✅ Loaded {len(df):,} rows and {len(df.columns)} columns in {load_time:.1f} seconds")

# Clean up column names (remove spaces and special characters)
df.columns = df.columns.str.strip()
print(f"📋 Columns: {list(df.columns)}")

# Show data range
if 'First Occurrence' in df.columns:
    print(f"📅 Date range: {df['First Occurrence'].min()} to {df['First Occurrence'].max()}")

# ============================================================================
# STEP 3: ANSWER THE 3 BUSINESS QUESTIONS QUICKLY
# ============================================================================

print("\n🎯 BUSINESS QUESTION ANALYSIS")
print("=" * 40)

# Question 1: CUNY Routes
print("\n1️⃣ CUNY Route Analysis:")
if 'Bus Route ID' in df.columns:
    route_counts = df['Bus Route ID'].value_counts()
    print(f"   📍 Total unique routes: {len(route_counts)}")
    print(f"   🔝 Top 10 routes by violations:")
    for i, (route, count) in enumerate(route_counts.head(10).items(), 1):
        print(f"      {i}. {route}: {count:,} violations")
        
    # CUNY route 
    # BX36, M101, BX6, M2, M42, etc.
    known_cuny_routes = ['M101', 'M15', 'M103', 'M11', 'M104', 'M23', 'B12', 'B49', 'Q17', 'Q25', 'Q34', 'Bx19', 'Bx26']
    cuny_found = [r for r in known_cuny_routes if r in route_counts.index]
    
    print(f"   🎓 Known CUNY-serving routes found: {cuny_found}")
    
    if cuny_found:
        cuny_violations = df[df['Bus Route ID'].isin(cuny_found)]
        cuny_pct = len(cuny_violations) / len(df) * 100
        print(f"   📊 CUNY route violations: {len(cuny_violations):,} ({cuny_pct:.1f}% of total)")

# Question 2: Exempt Violations  
print("\n2️⃣ Exempt Vehicle Analysis:")
if 'Violation Status' in df.columns:
    status_counts = df['Violation Status'].value_counts()
    print(f"   📊 Violation statuses:")
    for status, count in status_counts.items():
        print(f"      {status}: {count:,}")
    
    # Find exempt violations
    exempt_violations = df[df['Violation Status'].str.contains('EXEMPT', na=False)]
    print(f"   🚫 Total exempt violations: {len(exempt_violations):,}")
    
    if 'Vehicle ID' in df.columns and len(exempt_violations) > 0:
        repeat_offenders = exempt_violations['Vehicle ID'].value_counts()
        vehicles_with_multiple = sum(repeat_offenders > 1)
        print(f"   🚗 Exempt vehicles with repeat violations: {vehicles_with_multiple:,}")
        print(f"   🏆 Most exempt violations by one vehicle: {repeat_offenders.max()}")
        
        print(f"   🔝 Top 5 repeat exempt offenders:")
        for i, (vehicle, count) in enumerate(repeat_offenders.head(5).items(), 1):
            # Show partial vehicle ID for privacy
            masked_id = vehicle[:3] + "***" + vehicle[-3:] if len(str(vehicle)) > 6 else "***"
            print(f"      {i}. Vehicle {masked_id}: {count} violations")

# Question 3: Congestion Pricing
print("\n3️⃣ Congestion Pricing Impact:")
if 'First Occurrence' in df.columns:
    # Convert timestamp (handle the format from your data)
    df['First Occurrence'] = pd.to_datetime(df['First Occurrence'])
    
    # Split before/after Jan 5, 2025
    before_cp = df[df['First Occurrence'] < '2025-01-05']
    after_cp = df[df['First Occurrence'] >= '2025-01-05']
    
    print(f"   📅 Before congestion pricing (pre-Jan 5, 2025): {len(before_cp):,} violations")
    print(f"   📅 After congestion pricing (post-Jan 5, 2025): {len(after_cp):,} violations")
    
    if len(before_cp) > 0 and len(after_cp) > 0:
        # Calculate per-day averages
        before_days = (pd.to_datetime('2025-01-05') - before_cp['First Occurrence'].min()).days
        after_days = (df['First Occurrence'].max() - pd.to_datetime('2025-01-05')).days
        
        before_daily = len(before_cp) / max(before_days, 1)
        after_daily = len(after_cp) / max(after_days, 1)
        
        change = (after_daily - before_daily) / before_daily * 100
        print(f"   📈 Daily average before: {before_daily:.1f} violations/day")
        print(f"   📈 Daily average after: {after_daily:.1f} violations/day")
        print(f"   📊 Change: {change:+.1f}%")
    
    # Manhattan CBD analysis (if we have lat/lon)
    if 'Violation Latitude' in df.columns and 'Violation Longitude' in df.columns:
        # CBD bounds (below 60th St)
        cbd_violations = df[
            (df['Violation Latitude'] >= 40.7047) &  # Battery Park
            (df['Violation Latitude'] <= 40.7614) &  # 60th Street
            (df['Violation Longitude'] >= -74.0200) &  # Hudson River
            (df['Violation Longitude'] <= -73.9442)   # East River
        ]
        print(f"   🏙️ Violations in Manhattan CBD: {len(cbd_violations):,} ({len(cbd_violations)/len(df)*100:.1f}%)")




#VISUALIZATIONS

print("\n📊 Creating visualizations...")

# Visualization 1: Top routes
plt.figure(figsize=(15, 10))

if 'Bus Route ID' in df.columns:
    # Top routes chart
    plt.subplot(2, 2, 1)
    top_routes = df['Bus Route ID'].value_counts().head(15)
    top_routes.plot(kind='bar', color='skyblue')
    plt.title('Top 15 Routes by Violations', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45)
    plt.ylabel('Number of Violations')
    
    # CUNY vs Non-CUNY routes
    plt.subplot(2, 2, 2)
    known_cuny_routes = ['M101', 'M15', 'M103', 'M11', 'M104', 'M23', 'B12', 'B49', 'Q17', 'Q25', 'Q34', 'Bx19', 'Bx26']
    cuny_routes_found = [r for r in known_cuny_routes if r in df['Bus Route ID'].values]
    
    is_cuny = df['Bus Route ID'].isin(cuny_routes_found)
    cuny_counts = is_cuny.value_counts()
    
    plt.pie([cuny_counts[False], cuny_counts[True]], 
           labels=['Non-CUNY Routes', 'CUNY Routes'], 
           autopct='%1.1f%%',
           colors=['lightcoral', 'lightgreen'])
    plt.title('CUNY vs Non-CUNY Route Violations')

# Visualization 2: Time series
if 'First Occurrence' in df.columns:
    plt.subplot(2, 2, 3)
    df['Date'] = pd.to_datetime(df['First Occurrence']).dt.date
    daily_violations = df.groupby('Date').size()
    
    daily_violations.plot(color='orange', linewidth=2)
    plt.title('Violations Over Time')
    plt.axvline(pd.to_datetime('2025-01-05').date(), color='red', linestyle='--', linewidth=2, label='Congestion Pricing')
    plt.legend()
    plt.xticks(rotation=45)
    plt.ylabel('Daily Violations')

# Visualization 3: Violation types
if 'Violation Status' in df.columns:
    plt.subplot(2, 2, 4)
    status_counts = df['Violation Status'].value_counts()
    status_counts.plot(kind='bar', color='lightblue')
    plt.title('Violation Status Distribution')
    plt.xticks(rotation=45)
    plt.ylabel('Count')

plt.tight_layout()
plt.savefig('day1_mta_analysis.png', dpi=150, bbox_inches='tight')
plt.show()

print("✅ Visualizations saved as 'day1_mta_analysis.png'")






# Key Findings
findings = {
    'dataset_size': len(df),
    'date_range': [str(df['first_occurrence'].min()), str(df['first_occurrence'].max())] if 'first_occurrence' in df.columns else None,
    'top_routes': df['bus_route_id'].value_counts().head(10).to_dict() if 'bus_route_id' in df.columns else {},
    'total_routes': df['bus_route_id'].nunique() if 'bus_route_id' in df.columns else 0,
}

print(f"\n💾 Key findings saved for your team:")
print(f"   📊 Total violations analyzed: {findings['dataset_size']:,}")
print(f"   📅 Date range: {findings['date_range']}")
print(f"   🚌 Total routes: {findings['total_routes']}")

