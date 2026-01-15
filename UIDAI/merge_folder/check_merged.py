import pandas as pd

# Load the merged CSV
df = pd.read_csv('merged_aadhar_data.csv')

print(f"Merged CSV Shape: {df.shape}")
print("First 10 rows (state, district, pincode):")
print(df[['state', 'district', 'pincode']].head(10))
print("Duplicates check:")
duplicates = df.duplicated(subset=['date', 'state', 'district', 'pincode']).sum()
print(f"Duplicates: {duplicates}")

# Check if sorted by state, district, pincode
is_sorted = df[['state', 'district', 'pincode']].equals(df[['state', 'district', 'pincode']].sort_values(by=['state', 'district', 'pincode']))
print(f"Is sorted by state, district, pincode: {is_sorted}")

# Check for NaN values
nan_count = df.isnull().sum().sum()
print(f"Total NaN values: {nan_count}")

print("Column names:")
print(df.columns.tolist())
