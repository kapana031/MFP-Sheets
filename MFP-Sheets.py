import datetime
import myfitnesspal
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pathlib

# Set up credentials for Google Sheets API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(pathlib.Path('C:/Users/kapad/OneDrive - Northeastern University/Documents/Visual Studio 2022/mfp-sheets-3825035.json'), scope)
client1 = gspread.authorize(creds)

# Set up connection to MyFitnessPal API
client = myfitnesspal.Client()


# Set date range for data export
start_date = datetime.date(2023, 5, 8)
end_date = datetime.date(2023, 5, 14)

# Retrieve data from MyFitnessPal API
data = []
for date in (start_date + datetime.timedelta(n) for n in range((end_date - start_date).days + 1)):
    diary = client.get_date(date)
    row = [date.strftime('%Y-%m-%d')]
    totals = diary.totals
    row.extend([str(totals.get(k, 0)) for k in ['calories', 'carbohydrates', 'fat', 'protein']])
    data.append(row)

# Write data to Google Sheet
url = 'https://docs.google.com/spreadsheets/d/14Zc89VAJtI1i0i7aRhXEqy6fME3yVvG3vAAQYz0pnZ8/edit#gid=825003555'
  # Replace with your sheet URL
spreadsheet = client1.open_by_url(url)
worksheet = spreadsheet.worksheet('Progress')
worksheet.append_row(['Date', 'Calories', 'Carbs (g)', 'Fat (g)', 'Protein (g)'])
for row in data:
    worksheet.append_row(row)
# Calculate average of each column
average_calories = sum([float(row[1]) for row in data]) / len(data)
average_carbs = sum([float(row[2]) for row in data]) / len(data)
average_fat = sum([float(row[3]) for row in data]) / len(data)
average_protein = sum([float(row[4]) for row in data]) / len(data)

# Round the average values to 2 decimal places
average_calories = round(average_calories, 2)
average_carbs = round(average_carbs, 2)
average_fat = round(average_fat, 2)
average_protein = round(average_protein, 2)


# Add a new row as "Average"
worksheet.append_row(['Average', average_calories, average_carbs, average_fat, average_protein])

print('Data exported to Google Sheet')
