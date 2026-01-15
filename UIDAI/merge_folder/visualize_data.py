import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the cleaned CSV
df = pd.read_csv('cleaned_aadhar_data.csv')

# Clean column names
df.columns = df.columns.str.strip()

# Fill NaN with 0
df = df.fillna(0)

# Calculate total enrolment per row
df['total_enrolment'] = df['age_0_5'] + df['age_5_17'] + df['age_18_greater']

# Convert date to datetime
df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y', errors='coerce')

# Visualization 1: Bar chart - Enrolments per state
state_enrolment = df.groupby('state')['total_enrolment'].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(10, 6))
state_enrolment.plot(kind='bar')
plt.title('Top 10 States by Total Enrolment')
plt.xlabel('State')
plt.ylabel('Total Enrolment')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('enrolment_per_state.png')
plt.show()

# Visualization 2: Bar chart - Enrolments per district (top 10)
district_enrolment = df.groupby('district')['total_enrolment'].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(10, 6))
district_enrolment.plot(kind='bar')
plt.title('Top 10 Districts by Total Enrolment')
plt.xlabel('District')
plt.ylabel('Total Enrolment')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('enrolment_per_district.png')
plt.show()

# Visualization 3: Line chart - Enrolment trends over time
# Group by date and sum enrolment
time_trend = df.groupby('date')['total_enrolment'].sum().reset_index()
plt.figure(figsize=(12, 6))
plt.plot(time_trend['date'], time_trend['total_enrolment'])
plt.title('Enrolment Trends Over Time')
plt.xlabel('Date')
plt.ylabel('Total Enrolment')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('enrolment_trends_over_time.png')
plt.show()

# Visualization 4: Heatmap - Correlation between demographic and enrolment/biometric updates
# Select relevant columns
correlation_cols = ['age_0_5', 'age_5_17', 'age_18_greater', 'demo_age_5_17', 'demo_age_17_', 'bio_age_5_17', 'bio_age_17_']
corr_df = df[correlation_cols].corr()
plt.figure(figsize=(10, 8))
sns.heatmap(corr_df, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Heatmap: Demographic vs Enrolment/Biometric Updates')
plt.tight_layout()
plt.savefig('correlation_heatmap.png')
plt.show()

print("Visualizations saved as PNG files.")
