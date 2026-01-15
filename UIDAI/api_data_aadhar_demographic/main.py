import pandas as pd
import os

files = [
    "api_data_aadhar_demographic_0_500000.csv",
    "api_data_aadhar_demographic_500000_1000000.csv",
    "api_data_aadhar_demographic_1000000_1500000.csv",
    "api_data_aadhar_demographic_1500000_2000000.csv",
    "api_data_aadhar_demographic_2000000_2071700.csv"
]

def analyze_file(file_path):
    if not os.path.exists(file_path):
        return f"File {file_path} not found."

    df = pd.read_csv(file_path)

    report = f"Dataset Analysis Report for {file_path}\n"
    report += "=" * 60 + "\n\n"

    # Dataset Shape
    report += f"Dataset Shape: {df.shape}\n\n"

    # First 10 Rows
    report += "First 10 Rows:\n"
    report += str(df.head(10)) + "\n\n"

    # Data Types
    report += "Data Types:\n"
    report += str(df.dtypes) + "\n\n"

    # Missing Values
    report += "Missing Values per Column:\n"
    report += str(df.isnull().sum()) + "\n\n"

    # Unique values for categorical columns
    if 'state' in df.columns:
        report += f"Unique States: {df['state'].nunique()}\n"
    if 'district' in df.columns:
        report += f"Unique Districts: {df['district'].nunique()}\n"
    if 'pincode' in df.columns:
        report += f"Unique Pincodes: {df['pincode'].nunique()}\n\n"

    # Totals for demo_age columns
    if 'demo_age_5_17' in df.columns:
        report += f"Total Demo Age 5-17: {df['demo_age_5_17'].sum()}\n"
    if 'demo_age_17_' in df.columns:
        report += f"Total Demo Age 17+: {df['demo_age_17_'].sum()}\n\n"

    # Summary Statistics for Numeric Columns
    report += "Summary Statistics for Numeric Columns:\n"
    report += str(df.describe()) + "\n\n"

    # Additional insights
    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 0:
        report += "Additional Insights:\n"
        for col in numeric_cols:
            report += f"{col} - Min: {df[col].min()}, Max: {df[col].max()}, Mean: {df[col].mean():.2f}\n"
        report += "\n"

    # Check for duplicates
    duplicates = df.duplicated().sum()
    report += f"Number of Duplicate Rows: {duplicates}\n\n"

    # Date column analysis if exists
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        report += "Date Range:\n"
        report += f"Earliest Date: {df['date'].min()}\n"
        report += f"Latest Date: {df['date'].max()}\n"
        report += f"Number of Unique Dates: {df['date'].nunique()}\n\n"

    return report

for file in files:
    report_content = analyze_file(file)
    report_filename = f"analysis_report_{file.replace('.csv', '')}.txt"
    with open(report_filename, 'w') as f:
        f.write(report_content)
    print(f"Analysis for {file} completed. Results saved to '{report_filename}'")

print("All analyses completed.")
