

# 👨‍💻 Exploratory Data Analysis of Bikeshare Data
Simple python script to analyze bikeshare data via console input.

## 🔧 Usage
Run `bikeshare.py` and follow the console prompts.

## 🔍 Description
This analysis script allows the user to choose one of three datasets - one for each city:
- New York
- Chicago
- Washington

### Data Import and Filtering
Once the user selects a city, the corresponding data file (not included here) will be loaded. 
Data can be filtered by month and day of the week once the city is selected.<br>

### Summary Statistics
- Time
  - Most common month for bikeshare usage
  - Most common day of the week for bikeshare usage
  - Most common start hour of bikeshare trip
- Station
  - Most common starting station
  - Most common ending station
  - Most common start/end combination (trip)
- Trip Duration
  - Total travel time
  - Average travel time
- User
  - Customer count by user type
  - Customer count by gender
  - Birth date (youngest, oldest, most common age)

The user can also repeat analysis with a different city/filter criteria or examine 5 records of raw data.

## 📁 Files used
- bikeshare.py (analysis script)
- README.md (you're reading this right now)
## 📅 Date created
April 27, 2022

##  🧾Credits
### 📚 Docs
- 🐼 [Pandas](https://pandas.pydata.org/docs/reference/index.html#api)

