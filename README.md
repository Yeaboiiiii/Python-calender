# Global Holiday Planner Pro 🌍📅

A comprehensive holiday calendar application that displays holidays for different countries with an interactive calendar interface.

## Features

- 🌐 International Holiday Support: Uses the `holidays` Python library to fetch accurate holiday data for multiple countries
- 📅 Interactive Calendar: Visual calendar with holiday highlights
- 🎨 Color-Coded Weeks: 
  - Light Green: Weeks with one holiday{monday to friday}
  - Dark Green: Weeks with multiple holidays{monday to friday}
- 📊 Multiple Views:
  - Monthly View: See holidays for a specific month
  - Quarterly View: View three months at once
- 🔄 Dynamic Updates: Real-time updates when changing country or date selections

## Technology Stack

- **Streamlit**: For the interactive web interface
- **Holidays**: Python library for accurate holiday data across different countries
- **Pycountry**: For standardized country names and codes
- **Python-DateUtil**: For date manipulation and calculations
- **Pandas**: For data handling

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Holiday_Calender.git
cd Holiday_Calender
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows:
```bash
.\venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
streamlit run app.py
```

2. Open your browser and navigate to:
```
http://localhost:8501
```

3. Select your desired:
   - Country
   - Year
   - Month
   - View Type (Monthly/Quarterly)

## How It Works

The application uses the `holidays` Python library to fetch holiday data for different countries. Here's how it works:

1. **Country Selection**: 
   - Uses `holidays.list_supported_countries()` to get available countries
   - Integrates with `pycountry` for proper country name display

2. **Holiday Data Fetching**:
   ```python
   import holidays
   
   # Example: Get holidays for a specific country and year
   country_holidays = holidays.country_holidays('US', years=2024)
   ```

3. **Calendar Display**:
   - Highlights holidays in red
   - Shows holiday names on hover
   - Color-codes weeks based on number of holidays
