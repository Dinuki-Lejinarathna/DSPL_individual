import pandas as pd
#load dataset
df = pd.read_csv ('D:\streamlit\DSPL_individual\Information for Accommodation.csv')
print(df.head())
import numpy as np

# Clean column names
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Rename for easier reference
df.rename(columns={'ps/mc/uc': 'local_authority'}, inplace=True)
df.rename(columns={'logitiute': 'longitude'}, inplace=True) # Corrected the typo and rename to 'longitude'

# Replace string 'NULL' with actual NaN
df['longitude'] = df['longitude'].replace('NULL', np.nan) #Accessing the column using 'longitude'
df['latitude'] = df['latitude'].replace('NULL', np.nan)

# Convert coordinates and room count to numeric
df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce') # Accessing the column using 'longitude'
df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
df['rooms'] = pd.to_numeric(df['rooms'], errors='coerce')

# Drop rows with missing critical values
df.dropna(subset=['rooms', 'district', 'type', 'aga_division', 'local_authority', 'latitude', 'longitude'], inplace=True) # Use the name 'longitude'


# Add unique hotel ID based on name 

# Create a mapping of unique names to hotel IDs
unique_names = df['name'].dropna().unique()
name_to_id = {name: f"HOTEL_{i+1:04d}" for i, name in enumerate(unique_names)}

# Apply this mapping to the dataframe
df['hotel_id'] = df['name'].map(name_to_id)

# Optional: Move hotel_id to first column
cols = ['hotel_id'] + [col for col in df.columns if col != 'hotel_id']
df = df[cols]

#  Map grade to star rating category
grade_mapping = {
    'Deluxe': 'FIVE',
    'A': 'FIVE',
    'Superior': 'FOUR',
    'B': 'FOUR',
    'Standard': 'THREE',
    'C': 'THREE'
}

df['grade'] = df['grade'].map(grade_mapping)

# Standardize text fields
df['type'] = df['type'].str.title().str.strip()
df['district'] = df['district'].str.title().str.strip()
df['grade'] = df['grade'].fillna('Unrated').str.strip()


# Save cleaned dataset
df.to_csv("cleaned_accommodation.csv", index=False)

# Optional preview
print(df[['hotel_id', 'name', 'district', 'type', 'rooms', 'latitude', 'longitude']].head()) # Use the name 'longitude'