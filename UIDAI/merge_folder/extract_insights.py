import pandas as pd

# Read the cleaned CSV
df = pd.read_csv('cleaned_aadhar_data.csv')

# Clean column names
df.columns = df.columns.str.strip()

# Fill NaN with 0
df = df.fillna(0)

# Calculate total enrolment per row
df['total_enrolment'] = df['age_0_5'] + df['age_5_17'] + df['age_18_greater']

# Calculate total biometric updates per row
df['total_biometric'] = df['bio_age_5_17'] + df['bio_age_17_']

# Group by district for enrolment insights
district_enrolment = df.groupby('district')['total_enrolment'].sum().reset_index()

# Top 5 districts with highest enrolment
top_districts = district_enrolment[district_enrolment['total_enrolment'] > 0].nlargest(5, 'total_enrolment')

# Bottom 5 districts with lowest enrolment (excluding zero)
bottom_districts = district_enrolment[district_enrolment['total_enrolment'] > 0].nsmallest(5, 'total_enrolment')

# Age group with most updates
age_columns = ['age_0_5', 'age_5_17', 'age_18_greater', 'demo_age_5_17', 'demo_age_17_', 'bio_age_5_17', 'bio_age_17_']
age_totals = df[age_columns].sum()
most_updated_age = age_totals.idxmax()

# States with missing biometric data
state_biometric = df.groupby('state')['total_biometric'].sum().reset_index()
missing_biometric_states = state_biometric[state_biometric['total_biometric'] == 0]['state'].tolist()

# Print insights
print("Insights from Aadhaar Data Analysis:")
print("\n1. Districts with Highest Enrolment:")
for _, row in top_districts.iterrows():
    print(f"   {row['district']}: {int(row['total_enrolment'])} enrolments")

print("\n2. Districts with Lowest Enrolment:")
for _, row in bottom_districts.iterrows():
    print(f"   {row['district']}: {int(row['total_enrolment'])} enrolments")

print(f"\n3. Age Group with Most Updates: {most_updated_age}")

print(f"\n4. States with Missing Biometric Data: {', '.join(missing_biometric_states) if missing_biometric_states else 'None'}")

# Save to file
with open('insights.txt', 'w') as f:
    f.write("Insights from Aadhaar Data Analysis:\n")
    f.write("\n1. Districts with Highest Enrolment:\n")
    for _, row in top_districts.iterrows():
        f.write(f"   {row['district']}: {int(row['total_enrolment'])} enrolments\n")
    f.write("\n2. Districts with Lowest Enrolment:\n")
    for _, row in bottom_districts.iterrows():
        f.write(f"   {row['district']}: {int(row['total_enrolment'])} enrolments\n")
    f.write(f"\n3. Age Group with Most Updates: {most_updated_age}\n")
    f.write(f"\n4. States with Missing Biometric Data: {', '.join(missing_biometric_states) if missing_biometric_states else 'None'}\n")

print("\nInsights saved to insights.txt")
