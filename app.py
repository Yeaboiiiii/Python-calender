import streamlit as st
import pandas as pd
import calendar
import holidays
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import calendar
import pycountry

# Set page config
st.set_page_config(
    page_title="Global Holiday Planner Pro",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for calendar styling
st.markdown("""
<style>
    .light-green-week {
        background-color: #90EE90 !important;
    }
    .dark-green-week {
        background-color: #228B22 !important;
        color: white !important;
    }
    .calendar-table {
        width: 100%;
        text-align: center;
        border-collapse: collapse;
    }
    .calendar-table th, .calendar-table td {
        padding: 10px;
        border: 1px solid #ddd;
    }
    .calendar-table th {
        background-color: #f8f9fa;
    }
    .holiday {
        font-weight: bold;
        color: red;
    }
    .stApp > header {
        background-color: transparent;
    }
    .main-title {
        color: #1E88E5;
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_date' not in st.session_state:
    st.session_state.current_date = datetime.now()
if 'view_type' not in st.session_state:
    st.session_state.view_type = 'monthly'
if 'selected_country' not in st.session_state:
    st.session_state.selected_country = None
if 'selected_year' not in st.session_state:
    st.session_state.selected_year = datetime.now().year
if 'selected_month' not in st.session_state:
    st.session_state.selected_month = datetime.now().month

def navigate_month(direction):
    """Navigate to previous or next month."""
    if direction not in ("prev", "next"):
        return
        
    current_year = st.session_state.selected_year
    current_month = st.session_state.selected_month
    
    if direction == "prev":
        if current_month == 1:
            st.session_state.selected_month = 12
            st.session_state.selected_year = current_year - 1
        else:
            st.session_state.selected_month = current_month - 1
    else:  # direction == "next"
        if current_month == 12:
            st.session_state.selected_month = 1
            st.session_state.selected_year = current_year + 1
        else:
            st.session_state.selected_month = current_month + 1
            
    # Update current_date to match the new month/year
    st.session_state.current_date = datetime(st.session_state.selected_year, st.session_state.selected_month, 1)

def get_country_holidays(country_code, year):
    """Get holidays for a specific country and year."""
    try:
        # Create a holidays object for the specific country and year
        country_holidays = holidays.country_holidays(country_code, years=year)
        return country_holidays
    except (KeyError, ValueError) as e:
        st.error(f"Holiday data not available for country code: {country_code}")
        return {}

def count_weekday_holidays(start_date, end_date, holiday_dict):
    """Count holidays falling on weekdays within a date range."""
    count = 0
    current = start_date
    while current <= end_date:
        if current.weekday() < 5 and current in holiday_dict:  # Monday to Friday
            count += 1
        current += timedelta(days=1)
    return count

def create_month_calendar(year, month, country_holidays):
    """Create a calendar for a specific month with holiday highlighting."""
    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]
    
    # Create calendar HTML
    html = f'<h3>{month_name} {year}</h3>'
    html += '<table class="calendar-table">'
    html += '<tr><th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th><th>Fri</th><th>Sat</th><th>Sun</th></tr>'
    
    for week_idx, week in enumerate(cal):
        # Calculate the actual start and end dates for this week, including days from adjacent months
        first_day_of_week = None
        last_day_of_week = None
        
        # Find the first and last valid days in the week
        valid_days = [d for d in week if d != 0]
        if valid_days:
            if week[0] == 0:  # Week starts in previous month
                first_day = date(year, month, valid_days[0])
                first_day_of_week = first_day - timedelta(days=first_day.weekday())
            else:
                first_day_of_week = date(year, month, week[0])
                
            if week[-1] == 0:  # Week ends in next month
                last_day = date(year, month, valid_days[-1])
                last_day_of_week = last_day + timedelta(days=6-last_day.weekday())
            else:
                last_day_of_week = date(year, month, week[-1])
        
            # Count holidays for the entire week
            weekday_holidays = count_weekday_holidays(first_day_of_week, last_day_of_week, country_holidays)
            
            # Determine week class based on holiday count
            week_class = ''
            if weekday_holidays == 1:
                week_class = 'light-green-week'
            elif weekday_holidays > 1:
                week_class = 'dark-green-week'
            
            html += f'<tr class="{week_class}">'
            for day in week:
                if day == 0:
                    html += '<td></td>'
                else:
                    current_date = date(year, month, day)
                    holiday_name = country_holidays.get(current_date, '')
                    cell_class = 'holiday' if holiday_name else ''
                    tooltip = f' title="{holiday_name}"' if holiday_name else ''
                    html += f'<td class="{cell_class}"{tooltip}>{day}</td>'
            html += '</tr>'
        
    html += '</table>'
    return html

def get_available_countries():
    """Get all available countries from the holidays library with proper country names."""
    available_countries = {}
    
    for country_code in holidays.list_supported_countries():
        try:
            # Try to get the country name from pycountry
            country = pycountry.countries.get(alpha_2=country_code)
            if country:
                country_name = country.name
                available_countries[country_code] = country_name
        except (KeyError, AttributeError, ValueError):
            continue
    
    # Sort by country name and return
    return dict(sorted(available_countries.items(), key=lambda x: x[1]))

# Main content
st.markdown('<h1 class="main-title">🌍 Global Holiday Planner Pro</h1>', unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        Your comprehensive tool for international holiday planning and visualization
    </div>
""", unsafe_allow_html=True)

# Sidebar controls
st.sidebar.title("📋 Planning Controls")

# Country selection with dynamic fetching
if 'countries' not in st.session_state:
    with st.spinner('Loading available countries...'):
        st.session_state.countries = get_available_countries()
        if not st.session_state.countries:
            st.error("Unable to load countries. Please try refreshing the page.")
            st.stop()

# Create a reverse mapping for display
country_names = list(st.session_state.countries.values())
country_codes = list(st.session_state.countries.keys())

selected_country_name = st.sidebar.selectbox(
    "Select Country",
    options=country_names,
    index=0
)

# Get the country code for the selected country name
selected_country = country_codes[country_names.index(selected_country_name)]
st.session_state.selected_country = selected_country

# View type selection
view_type = st.sidebar.radio("Select View", ['Monthly', 'Quarterly'])
st.session_state.view_type = view_type.lower()

# Year selection - show for both monthly and quarterly views
current_year = datetime.now().year
years = list(range(1950, 2051))  # Show years from 1950 to 2050
current_year_index = years.index(current_year)  # Find the index of current year
selected_year = st.sidebar.selectbox("Select Year", years, index=years.index(st.session_state.selected_year))
st.session_state.selected_year = selected_year

# Month selection - only show for quarterly view
if st.session_state.view_type != 'monthly':
    months = list(range(1, 13))
    month_names = [calendar.month_name[m] for m in months]
    selected_month = st.sidebar.selectbox("Select Month", months, format_func=lambda x: calendar.month_name[x], index=st.session_state.selected_month - 1)
    st.session_state.selected_month = selected_month
    
    # Update current_date based on selections
    st.session_state.current_date = datetime(selected_year, selected_month, 1)
else:
    # Update current_date for monthly view (preserve the month from navigation)
    current_month = st.session_state.current_date.month
    st.session_state.current_date = datetime(selected_year, current_month, 1)

# Get current date values
selected_year = st.session_state.selected_year
selected_month = st.session_state.selected_month

# Get holidays for the selected country and year
country_holidays = get_country_holidays(st.session_state.selected_country, selected_year)

# Display calendar
if st.session_state.view_type == 'monthly':
    # Monthly view
    col1, col2, col3 = st.columns([1, 3, 1])
    
    # Navigation buttons
    with col1:
        if st.button("← Previous", key="prev_month"):
            navigate_month("prev")
    with col3:
        if st.button("Next →", key="next_month"):
            navigate_month("next")
    
    # Display calendar with current state
    st.markdown(create_month_calendar(
        st.session_state.selected_year,
        st.session_state.selected_month,
        country_holidays
    ), unsafe_allow_html=True)
else:
    # Quarterly view
    quarter_start = (selected_month - 1) // 3 * 3 + 1
    cols = st.columns(3)
    for i, month in enumerate(range(quarter_start, quarter_start + 3)):
        with cols[i]:
            st.markdown(create_month_calendar(
                selected_year,
                month,
                country_holidays
            ), unsafe_allow_html=True)

# Display holiday list for the current month/quarter
st.subheader(f"Holidays in {selected_country_name}")
if st.session_state.view_type == 'monthly':
    month_start = date(selected_year, selected_month, 1)
    month_end = month_start + relativedelta(months=1) - timedelta(days=1)
else:
    quarter_start = date(selected_year, quarter_start, 1)
    quarter_end = quarter_start + relativedelta(months=3) - timedelta(days=1)
    month_start, month_end = quarter_start, quarter_end

holiday_list = [(date_, name) for date_, name in country_holidays.items() 
                if month_start <= date_ <= month_end]

if holiday_list:
    for holiday_date, holiday_name in sorted(holiday_list):
        st.write(f"**{holiday_date.strftime('%B %d, %Y')}**: {holiday_name}")
else:
    st.write("No holidays in this period.") 