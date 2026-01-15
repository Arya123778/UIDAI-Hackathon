import pandas as pd

# Read the merged CSV
df = pd.read_csv('merged_aadhar_data.csv')

print(f"Original data shape: {df.shape}")

# Clean column names (remove trailing spaces)
df.columns = df.columns.str.strip()

# Remove duplicates based on key columns: date, state, district, pincode
# Keep the first occurrence
key_columns = ['date', 'state', 'district', 'pincode']
df_cleaned = df.drop_duplicates(subset=key_columns, keep='first')

# Filter out invalid rows where state, district, or pincode are '100000' (placeholder data)
df_cleaned = df_cleaned[~((df_cleaned['state'] == '100000') | (df_cleaned['district'] == '100000') | (df_cleaned['pincode'] == 100000))]

print(f"Cleaned data shape: {df_cleaned.shape}")
print(f"Removed {df.shape[0] - df_cleaned.shape[0]} duplicate rows and invalid entries")

# Save the cleaned dataframe to a new CSV
df_cleaned.to_csv('cleaned_aadhar_data.csv', index=False)

print("Cleaned CSV created successfully: cleaned_aadhar_data.csv")
