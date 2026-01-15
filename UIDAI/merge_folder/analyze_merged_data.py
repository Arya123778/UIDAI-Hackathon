import pandas as pd

# Read the cleaned CSV
df = pd.read_csv('cleaned_aadhar_data.csv')

# Clean column names if needed (remove trailing spaces)
df.columns = df.columns.str.strip()

# Fill NaN with 0 for calculations
df = df.fillna(0)

# Calculate total enrolment per row
df['total_enrolment'] = df['age_0_5'] + df['age_5_17'] + df['age_18_greater']

# Calculate total demographic population per row (assuming demo_age_17_ is demo_age_17_19)
df['total_demo_population'] = df['demo_age_5_17'] + df['demo_age_17_']

# Calculate total biometric updates per row
df['total_bio_updates'] = df['bio_age_5_17'] + df['bio_age_17_']

# Analysis 1: High enrolment areas vs population
# Group by state and district, sum totals
grouped = df.groupby(['state', 'district']).agg({
    'total_enrolment': 'sum',
    'total_demo_population': 'sum'
}).reset_index()

# Filter out areas with zero population to avoid inf
grouped = grouped[grouped['total_demo_population'] > 0]

# Calculate enrolment rate (enrolment / population * 100)
grouped['enrolment_rate'] = (grouped['total_enrolment'] / grouped['total_demo_population'] * 100)

# Sort by enrolment rate descending
high_enrolment_areas = grouped.sort_values('enrolment_rate', ascending=False).head(10)

print("Top 10 High Enrolment Areas vs Population (filtered for population > 0):")
print(high_enrolment_areas[['state', 'district', 'total_enrolment', 'total_demo_population', 'enrolment_rate']])

# Analysis 2: Age group distribution vs biometric updates
# Group by age groups (simplified: 0-5, 5-17, 18+)
age_group_enrolment = df[['age_0_5', 'age_5_17', 'age_18_greater']].sum()
age_group_bio = df[['bio_age_5_17', 'bio_age_17_']].sum()

# Assuming bio_age_5_17 corresponds to 5-17, bio_age_17_ to 18+
# But enrolment has 0-5, 5-17, 18+, bio has 5-17, 17+
# For simplicity, compare 5-17 and 17+ (assuming 17+ is 18+)
age_comparison = pd.DataFrame({
    'age_group': ['5-17', '17+'],
    'enrolment': [age_group_enrolment['age_5_17'], age_group_enrolment['age_18_greater']],
    'biometric_updates': [age_group_bio['bio_age_5_17'], age_group_bio['bio_age_17_']]
})

age_comparison['update_rate'] = (age_comparison['biometric_updates'] / age_comparison['enrolment'] * 100).fillna(0)

print("\nAge Group Distribution vs Biometric Updates:")
print(age_comparison)
