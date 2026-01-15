import pandas as pd
import numpy as np

# Read the cleaned CSV
df = pd.read_csv('cleaned_aadhar_data.csv')

# Clean column names
df.columns = df.columns.str.strip()

# Fill NaN with 0
df = df.fillna(0)

# Convert date to datetime
df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y', errors='coerce')

# Calculate totals
df['total_enrolment'] = df['age_0_5'] + df['age_5_17'] + df['age_18_greater']
df['total_demo_population'] = df['demo_age_5_17'] + df['demo_age_17_']
df['total_bio_updates'] = df['bio_age_5_17'] + df['bio_age_17_']

print("=== ADVANCED INSIGHTS FROM AADHAAR DATA ===\n")

# 1. Overall Statistics
print("1. OVERALL STATISTICS:")
total_enrolment = df['total_enrolment'].sum()
total_population = df['total_demo_population'].sum()
total_bio_updates = df['total_bio_updates'].sum()
coverage_rate = (total_enrolment / total_population * 100) if total_population > 0 else 0
bio_update_rate = (total_bio_updates / total_enrolment * 100) if total_enrolment > 0 else 0

print(f"Total Enrolment: {total_enrolment:,.0f}")
print(f"Total Demographic Population: {total_population:,.0f}")
print(f"Total Biometric Updates: {total_bio_updates:,.0f}")
print(f"Overall Coverage Rate: {coverage_rate:.2f}%")
print(f"Overall Biometric Update Rate: {bio_update_rate:.2f}%\n")

# 2. State-wise Analysis
print("2. STATE-WISE ANALYSIS:")
state_stats = df.groupby('state').agg({
    'total_enrolment': 'sum',
    'total_demo_population': 'sum',
    'total_bio_updates': 'sum'
}).reset_index()

state_stats['coverage_rate'] = (state_stats['total_enrolment'] / state_stats['total_demo_population'] * 100).fillna(0)
state_stats['bio_update_rate'] = (state_stats['total_bio_updates'] / state_stats['total_enrolment'] * 100).fillna(0)

# Top 5 states by coverage
top_coverage = state_stats.nlargest(5, 'coverage_rate')
print("Top 5 States by Coverage Rate:")
for _, row in top_coverage.iterrows():
    print(f"  {row['state']}: {row['coverage_rate']:.2f}% ({row['total_enrolment']:,.0f}/{row['total_demo_population']:,.0f})")

# Bottom 5 states by coverage
bottom_coverage = state_stats.nsmallest(5, 'coverage_rate')
print("\nBottom 5 States by Coverage Rate:")
for _, row in bottom_coverage.iterrows():
    print(f"  {row['state']}: {row['coverage_rate']:.2f}% ({row['total_enrolment']:,.0f}/{row['total_demo_population']:,.0f})")

# Anomalies: States with coverage > 100% (possible data issues)
anomalous_states = state_stats[state_stats['coverage_rate'] > 100]
if not anomalous_states.empty:
    print(f"\nAnomalous States (Coverage > 100%): {len(anomalous_states)} states")
    for _, row in anomalous_states.iterrows():
        print(f"  {row['state']}: {row['coverage_rate']:.2f}% - Possible data inconsistency")

print()

# 3. Age Group Analysis
print("3. AGE GROUP ANALYSIS:")
age_groups = {
    '0-5': 'age_0_5',
    '5-17': 'age_5_17',
    '17+': 'age_18_greater'
}

age_enrolment = df[list(age_groups.values())].sum()
age_bio = {
    '0-5': 0,  # No biometric data for 0-5
    '5-17': df['bio_age_5_17'].sum(),
    '17+': df['bio_age_17_'].sum()
}

print("Enrolment by Age Group:")
for age, col in age_groups.items():
    pct = (age_enrolment[col] / total_enrolment * 100) if total_enrolment > 0 else 0
    print(f"  {age}: {age_enrolment[col]:,.0f} ({pct:.1f}%)")

print("\nBiometric Update Rates by Age Group:")
for age in ['5-17', '17+']:
    enrolment = age_enrolment[age_groups[17+]]
    bio = age_bio[age]
    rate = (bio / enrolment * 100) if enrolment > 0 else 0
    print(f"  {age}: {rate:.2f}% ({bio:,.0f}/{enrolment:,.0f})")

# Trend: Children (0-17) vs Adults (18+)
children_enrolment = age_enrolment['age_0_5'] + age_enrolment['age_5_17']
adult_enrolment = age_enrolment['age_18_greater']
children_pct = (children_enrolment / total_enrolment * 100) if total_enrolment > 0 else 0
adult_pct = (adult_enrolment / total_enrolment * 100) if total_enrolment > 0 else 0

print(f"\nChildren (0-17) Enrolment: {children_enrolment:,.0f} ({children_pct:.1f}%)")
print(f"Adult (18+) Enrolment: {adult_enrolment:,.0f} ({adult_pct:.1f}%)")

if children_pct < 30:
    print("INSIGHT: Low children enrolment - may indicate issues with family enrolment or data collection")
elif children_pct > 50:
    print("INSIGHT: High children enrolment - good inclusion of younger population")

print()

# 4. Time Trends
print("4. TIME TRENDS:")
if df['date'].notna().any():
    time_trends = df.groupby(df['date'].dt.to_period('M')).agg({
        'total_enrolment': 'sum',
        'total_bio_updates': 'sum'
    }).reset_index()

    time_trends['date'] = time_trends['date'].dt.to_timestamp()
    time_trends = time_trends.sort_values('date')

    print("Monthly Enrolment Trends:")
    for _, row in time_trends.iterrows():
        month = row['date'].strftime('%b %Y')
        enrolment = row['total_enrolment']
        print(f"  {month}: {enrolment:,.0f}")

    # Check for anomalies in trends
    time_trends['enrolment_change'] = time_trends['total_enrolment'].pct_change() * 100
    anomalies = time_trends[time_trends['enrolment_change'].abs() > 50]  # >50% change
    if not anomalies.empty:
        print(f"\nAnomalous Months (>{50}% change):")
        for _, row in anomalies.iterrows():
            month = row['date'].strftime('%b %Y')
            change = row['enrolment_change']
            print(f"  {month}: {change:+.1f}% change")

print()

# 5. District-level Anomalies
print("5. DISTRICT-LEVEL ANOMALIES:")
district_stats = df.groupby(['state', 'district']).agg({
    'total_enrolment': 'sum',
    'total_demo_population': 'sum',
    'total_bio_updates': 'sum'
}).reset_index()

district_stats['coverage_rate'] = (district_stats['total_enrolment'] / district_stats['total_demo_population'] * 100).fillna(0)
district_stats['bio_update_rate'] = (district_stats['total_bio_updates'] / district_stats['total_enrolment'] * 100).fillna(0)

# Districts with zero enrolment but population
zero_enrolment = district_stats[(district_stats['total_enrolment'] == 0) & (district_stats['total_demo_population'] > 0)]
if not zero_enrolment.empty:
    print(f"Districts with Population but Zero Enrolment: {len(zero_enrolment)}")
    print("Sample:")
    for _, row in zero_enrolment.head(3).iterrows():
        print(f"  {row['state']} - {row['district']}: Pop {row['total_demo_population']:,.0f}")

# Districts with very high coverage (>150%)
high_coverage = district_stats[district_stats['coverage_rate'] > 150]
if not high_coverage.empty:
    print(f"\nDistricts with Very High Coverage (>150%): {len(high_coverage)}")
    print("Sample:")
    for _, row in high_coverage.head(3).iterrows():
        print(f"  {row['state']} - {row['district']}: {row['coverage_rate']:.1f}%")

print()

# 6. Correlation Analysis
print("6. CORRELATION ANALYSIS:")
correlation_cols = ['age_0_5', 'age_5_17', 'age_18_greater', 'demo_age_5_17', 'demo_age_17_', 'bio_age_5_17', 'bio_age_17_']
corr_matrix = df[correlation_cols].corr()

print("Key Correlations:")
# Enrolment vs Demographics
enrol_demo_corr = corr_matrix.loc['age_5_17', 'demo_age_5_17']
print(f"Enrolment (5-17) vs Demographics (5-17): {enrol_demo_corr:.3f}")

enrol_demo_adult_corr = corr_matrix.loc['age_18_greater', 'demo_age_17_']
print(f"Enrolment (18+) vs Demographics (17+): {enrol_demo_adult_corr:.3f}")

# Biometric vs Enrolment
bio_enrol_corr = corr_matrix.loc['bio_age_5_17', 'age_5_17']
print(f"Biometric (5-17) vs Enrolment (5-17): {bio_enrol_corr:.3f}")

if enrol_demo_corr < 0.5:
    print("INSIGHT: Weak correlation between enrolment and demographics - possible under-enrolment in certain areas")

print()

# 7. Government Decision Insights
print("7. GOVERNMENT DECISION INSIGHTS:")
print("SOCIAL INSIGHTS:")
print("- Population Coverage: Overall coverage rate indicates inclusion level")
print("- Age Distribution: High children enrolment suggests family inclusion efforts")
print("- Regional Disparities: States with low coverage need targeted interventions")
print("- Vulnerable Groups: Monitor enrolment of children and elderly")

print("\nADMINISTRATIVE INSIGHTS:")
print("- Efficiency: Biometric update rates show system effectiveness")
print("- Data Quality: Anomalous high coverage areas need verification")
print("- Resource Allocation: Focus on low-performing states/districts")
print("- Monitoring: Track time trends for policy impact assessment")

print("\nRECOMMENDATIONS:")
print("- Increase enrolment drives in low-coverage states")
print("- Improve biometric update processes in areas with low rates")
print("- Verify data accuracy in anomalous districts")
print("- Monitor seasonal trends for optimal campaign timing")
print("- Enhance inclusion of children and marginalized groups")

# Save detailed report
with open('detailed_insights_report.txt', 'w') as f:
    f.write("DETAILED INSIGHTS REPORT FROM AADHAAR DATA ANALYSIS\n\n")
    f.write(f"Total Records: {len(df)}\n")
    f.write(f"Date Range: {df['date'].min()} to {df['date'].max()}\n")
    f.write(f"States Covered: {df['state'].nunique()}\n")
    f.write(f"Districts Covered: {df['district'].nunique()}\n\n")
    f.write("KEY FINDINGS:\n")
    f.write(f"- Overall Coverage: {coverage_rate:.2f}%\n")
    f.write(f"- Biometric Update Rate: {bio_update_rate:.2f}%\n")
    f.write(f"- Children Enrolment Share: {children_pct:.1f}%\n")
    f.write(f"- Anomalous Districts: {len(zero_enrolment) + len(high_coverage)}\n")

print("\nDetailed report saved to detailed_insights_report.txt")
