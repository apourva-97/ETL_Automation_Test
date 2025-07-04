'''
import pandas as pd

# Load the raw data
df = pd.read_csv("etl_Source/sales_data_raw.csv")

# Clean and transform the data
df_clean = df.dropna(subset=["Date", "CustomerName"]).copy()
df_clean["Date"] = pd.to_datetime(df_clean["Date"], errors="coerce").dt.strftime("%Y-%m-%d")
df_clean["Product"] = df_clean["Product"].str.strip()
df_clean["CustomerName"] = df_clean["CustomerName"].str.strip()
df_clean["Region"] = df_clean["Region"].str.strip()
df_clean["Price"] = df_clean["Price"].replace("[\\$,]", "", regex=True).astype(float)
df_clean["Total"] = df_clean["Price"] * df_clean["Quantity"]
df_clean = df_clean.drop(columns=["Status"])

# Save the cleaned data
df_clean.to_csv("etl_Source /sales_data_clean.csv", index=False)
print("sales_data_clean.csv saved to 'etl_download' folder.")
'''
import pandas as pd

data = {
    "ID": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "Name": [
        "John Doe", "Jane Smith", "Bob Johnson", "", "Anna Lee",
        "Mike Chan", "Sara Kim", "Tom O'Brien", "Lucy Lee", "James Wu"
    ],
    "Email": [
        "john.doe@example.com", "jane.smith@domain", "bob.johnson@example.com", "invalid.email.com",
        "anna.lee@example.com", "mikechan@site.com", "sara.kim@example.com", "tom.obrien@example.com",
        "lucy.lee@example.", "james.wu@example.com"
    ],
    "DateOfBirth": [
        "1990-05-14", "1985-11-30", "2003-07-25", "1975-02-20", "2010-10-10",
        "2001-01-01", "1999-03-15", "1998-09-09", "1987-06-06", "1980-12-01"
    ],
    "Age": [34, 39, 21, 49, 14, None, 25, 26, 37, 43],
    "Country": [
        "USA", "Canada", "UK", "", "Australia", "China", "South Korea", "Ireland", "USA", "China"
    ],
    "PhoneNumber": [
        "+1-202-555-0125", "1234567890", "+44 20 7946 0958", "+91-9876543210", "+61-2-1234-5678",
        "555-0000", "+82-2-312-3456", "", "+1-202-555-0155", "+86 10 1234 5678"
    ],
    "SignupDate": [
        "2023-03-01", "2022-12-15", "2021-05-12", "2020-07-20", "2023-09-30",
        "2023-01-01", "invalid_date", "2022-04-04", "2021-11-11", "2024-06-06"
    ],
    "IsActive": [
        "TRUE", "FALSE", "TRUE", "TRUE", "TRUE",
        "FALSE", "TRUE", "yes", "FALSE", "FALSE"
    ]
}

df = pd.DataFrame(data)
#df.to_csv("etl_Source /sample_data_validation.csv", index=False)
df.to_csv("sample_data_validation.csv", index=False) 
print("CSV file 'sample_data_validation.csv' has been created.")

