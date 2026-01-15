import pandas as pd

# Read the CSV files
enrolment_df = pd.read_csv('api_data_aadhar_enrolment_500000_1000000.csv')
demographic_df = pd.read_csv('api_data_aadhar_demographic_500000_1000000.csv')
biometric_df = pd.read_csv('api_data_aadhar_biometric_1000000_1500000.csv')

# Merge enrolment with demographic on common columns
merged_df = pd.merge(enrolment_df, demographic_df, on=['date', 'state', 'district', 'pincode'], how='outer')

# Merge the result with biometric on common columns
merged_df = pd.merge(merged_df, biometric_df, on=['date', 'state', 'district', 'pincode'], how='outer')

# Clean the merged data
# Clean column names (remove trailing spaces)
merged_df.columns = merged_df.columns.str.strip()

# Remove duplicates based on key columns: date, state, district, pincode
# Keep the first occurrence
key_columns = ['date', 'state', 'district', 'pincode']
merged_df = merged_df.drop_duplicates(subset=key_columns, keep='first')

# Sort by state, district, pincode for neat order
merged_df = merged_df.sort_values(by=['state', 'district', 'pincode'])

# Fill NaN values with 0 for neatness (assuming missing data means 0 enrolments/updates)
merged_df = merged_df.fillna(0)

# Save the cleaned, sorted, and filled merged dataframe to a new CSV
merged_df.to_csv('merged_aadhar_data.csv', index=False)

print("Cleaned and sorted merged CSV created successfully: merged_aadhar_data.csv")
