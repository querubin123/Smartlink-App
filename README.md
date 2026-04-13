Here's your updated README file with all the new geolocation features included:

```markdown
# 🔗 SmartLink - Professional URL Shortener & Analytics

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://smartlinkapp.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Smartlink--App-blue)](https://github.com/querubin123/Smartlink-App)

A professional, feature-rich URL shortener with real-time analytics, dual-mode geolocation (GPS + IP), device detection, and UTM parameter support. Built with Streamlit and SQLite.

## ✨ Features

### Core Features
- **🔗 URL Shortening** - Create short, memorable links from long URLs
- **🎨 Custom Short Codes** - Personalize your links with custom aliases
- **📊 Real-time Analytics** - Track every click with detailed statistics
- **📈 UTM Parameters** - Track marketing campaigns with UTM tags
- **⏰ 24-Hour Activity** - Monitor recent click activity

### Location & Device Tracking
- **📍 Dual-Mode Geolocation** - Uses browser GPS when available, falls back to IP detection
- **🎯 GPS Tracking** - Precise location data when users grant permission
- **🌐 IP Detection** - Country/region level data as automatic fallback
- **📱 Device Detection** - Desktop, mobile, or tablet identification
- **🌐 Browser Statistics** - Chrome, Firefox, Safari, Edge, Opera tracking
- **💿 OS Detection** - Windows, macOS, Linux, Android, iOS tracking

### Analytics Dashboard
- **📈 Click Activity Timeline** - Last 7 days click trends (line chart)
- **⏰ Hourly Distribution** - When users click your links (bar chart)
- **🌍 Geographic Distribution** - Worldwide click mapping
- **🎯 Tracking Methods Analysis** - GPS vs IP detection statistics
- **📱 Device Breakdown** - Device type distribution (pie chart)
- **🌐 Browser Usage** - Browser market share analytics
- **💿 OS Distribution** - Operating system statistics

### UI/UX
- **🎨 Modern Dark Theme** - Professional, eye-friendly interface
- **📋 One-Click Copy** - Easy URL copying functionality
- **🔒 Secure** - SQLite database with local storage
- **⚡ Real-time Updates** - Live stats refresh

## 🚀 Live Demo

**[View Live Demo](https://smartlinkapp.streamlit.app/)** - Try the app now!

## 📋 Table of Contents

- [Installation](#installation)
- [Local Development](#local-development)
- [Deployment](#deployment)
- [Usage Guide](#usage-guide)
- [Geolocation System](#geolocation-system)
- [Analytics Dashboard](#analytics-dashboard)
- [UTM Tracking](#utm-tracking)
- [Database Schema](#database-schema)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

## 🛠️ Installation

### Prerequisites

- Python 3.9 or higher
- Python package manager (pip comes with Python)

### Step 1: Clone the Repository

```bash
git clone https://github.com/querubin123/Smartlink-App.git
cd Smartlink-App
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
python -m streamlit run app.py
```

The app will open at `http://localhost:8501`

## 💻 Local Development

### Requirements

Create a `requirements.txt` file:

```txt
streamlit>=1.28.0
streamlit-geolocation>=0.1.0
pandas>=2.0.0
plotly>=5.17.0
requests>=2.31.0
```

Then install using:

```bash
python -m pip install -r requirements.txt
```

### Environment Variables

No environment variables are required for local development. The app uses:
- SQLite for database (auto-creates `smartlink.db`)
- Multiple geolocation APIs (ip-api.com, ipapi.co, ipwhois.io)
- Browser Geolocation API for GPS tracking
- ipify.org for IP detection

## 🚢 Deployment

### Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Click "New app"
4. Select your repository
5. Set:
   - Branch: `main`
   - Main file path: `app.py`
   - Python version: 3.9+
6. Click "Deploy"


## 📖 Usage Guide

### Creating a Short Link

1. Enter your long URL in the "Destination URL" field
2. (Optional) Add a custom short code
3. (Optional) Add UTM parameters for campaign tracking
4. Click "🚀 Generate Short Link"
5. Copy your new short URL

### Example

```
Original URL: https://github.com/querubin123/Smartlink-App
Short URL: https://smartlinkapp.streamlit.app/?go=abc123
Custom Short URL: https://smartlinkapp.streamlit.app/?go=my-project
```

### How Geolocation Works

The app uses a dual-mode geolocation system:

1. **GPS Mode (Priority)** - When users click "Allow" on location permission
   - Captures precise latitude/longitude coordinates
   - Provides city-level accuracy
   - Marked with 🎯 icon in analytics

2. **IP Detection (Fallback)** - When users deny location or GPS unavailable
   - Automatically falls back to IP-based geolocation
   - Provides country/region level data
   - Marked with 🌐 icon in analytics
   - Always works, even without permission

This ensures you always get analytics data while respecting user privacy choices.

## 📊 Analytics Dashboard

The dashboard provides comprehensive insights across 5 tabs:

### 1. Overview Tab
- **Click Activity** - Last 7 days click trends (line chart)
- **Hourly Distribution** - When users click your links (bar chart)
- **Link Distribution** - Click share across different links (pie chart)

### 2. Geographic Tab
- **Top Countries** - Bar chart of top performing countries
- **World Distribution** - Pie chart of global click distribution
- **Country Stats** - Detailed country-by-country breakdown

### 3. Devices Tab
- **Device Types** - Desktop vs Mobile vs Tablet (pie chart)
- **Browser Stats** - Chrome, Firefox, Safari, Edge distribution
- **Operating Systems** - Windows, macOS, Linux, Android, iOS

### 4. Tracking Methods Tab
- **GPS vs IP Detection** - See what percentage of users enable GPS
- **Accuracy Comparison** - Understand your data quality
- **Method Analytics** - Track geolocation source performance

### 5. Link Details Tab
- **Individual Link Performance** - Per-link click statistics
- **Country Breakdown** - Geographic data for each link
- **Recent Activity** - Latest clicks with device and location info

## 📈 UTM Tracking

Track marketing campaigns with UTM parameters:

| Parameter | Description | Example |
|-----------|-------------|---------|
| `utm_source` | Traffic source | google, facebook, newsletter |
| `utm_medium` | Marketing medium | cpc, email, social |
| `utm_campaign` | Campaign name | summer-sale, black-friday |
| `utm_term` | Paid keywords | running+shoes |
| `utm_content` | Content variation | cta-button, banner-ad |

### Example with UTM

```
Original: https://mywebsite.com/product
With UTM: https://mywebsite.com/product?utm_source=facebook&utm_medium=social&utm_campaign=summer-sale
Shortened: https://smartlinkapp.streamlit.app/?go=summer2024
```

## 🗄️ Database Schema

### Links Table
```sql
CREATE TABLE links (
    id TEXT PRIMARY KEY,
    short_code TEXT UNIQUE NOT NULL,
    original_url TEXT NOT NULL,
    clicks INTEGER DEFAULT 0,
    created_date TEXT,
    last_clicked TEXT
);
```

### Clicks Table (Enhanced with Geolocation)
```sql
CREATE TABLE clicks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    short_code TEXT,
    click_time TEXT,
    ip_address TEXT,
    country TEXT DEFAULT 'Unknown',
    city TEXT DEFAULT 'Unknown',
    region TEXT DEFAULT 'Unknown',
    latitude REAL DEFAULT 0,
    longitude REAL DEFAULT 0,
    isp TEXT DEFAULT 'Unknown',
    device_type TEXT DEFAULT 'Unknown',
    browser TEXT DEFAULT 'Unknown',
    browser_version TEXT DEFAULT 'Unknown',
    operating_system TEXT DEFAULT 'Unknown',
    referer TEXT DEFAULT 'Direct',
    user_agent TEXT DEFAULT 'Unknown',
    timezone TEXT DEFAULT 'Unknown',
    postal_code TEXT DEFAULT 'Unknown',
    geo_source TEXT DEFAULT 'ip_detection'  -- 'browser_gps' or 'ip_detection'
);
```

### Indexes for Performance
```sql
CREATE INDEX idx_clicks_short_code ON clicks(short_code);
CREATE INDEX idx_clicks_click_time ON clicks(click_time);
CREATE INDEX idx_clicks_country ON clicks(country);
CREATE INDEX idx_clicks_geo_source ON clicks(geo_source);
```

## 🛠️ Technologies Used

### Frontend
- **Streamlit** - Web application framework
- **Custom CSS** - Modern dark theme with animations
- **Google Fonts** - Inter font family

### Backend
- **Python 3.9+** - Core programming language
- **SQLite3** - Local database storage
- **Streamlit Geolocation** - Browser GPS integration

### Analytics & Data
- **Pandas** - Data manipulation and analysis
- **Plotly** - Interactive charts and visualizations

### APIs & Services
- **ipapi.co** - Primary IP geolocation
- **ip-api.com** - Backup IP geolocation
- **ipwhois.io** - Secondary IP geolocation
- **ipify.org** - IP address detection
- **OpenStreetMap Nominatim** - Reverse geocoding for GPS coordinates

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

```bash
# Fork and clone your fork
git clone https://github.com/your-username/Smartlink-App.git
cd Smartlink-App

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
python -m pip install -r requirements.txt

# Run the app
python -m streamlit run app.py
```

## 📝 License

Distributed under the MIT License. See `LICENSE` file for more information.

## 📧 Contact

GitHub: [@querubin123](https://github.com/querubin123)

Project Link: [https://github.com/querubin123/Smartlink-App](https://github.com/querubin123/Smartlink-App)

Live Demo: [https://smartlinkapp.streamlit.app/](https://smartlinkapp.streamlit.app/)

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) - Amazing framework for data apps
- [Plotly](https://plotly.com/) - Interactive visualizations
- [ip-api.com](http://ip-api.com/) - Free geolocation API
- [ipapi.co](https://ipapi.co/) - Reliable IP geolocation
- [ipify.org](https://www.ipify.org/) - Simple IP detection API
- [OpenStreetMap](https://www.openstreetmap.org/) - Reverse geocoding
- [Google Fonts](https://fonts.google.com/) - Inter font family

## ⭐ Show your support

Give a ⭐️ on [GitHub](https://github.com/querubin123/Smartlink-App) if this project helped you!

---

## 📌 Notes for Production Deployment

### Database Persistence on Streamlit Cloud

The SQLite database is ephemeral on Streamlit Cloud. For persistent storage, consider:

1. **Supabase** (Recommended for PostgreSQL)
```python
# Install: python -m pip install supabase
from supabase import create_client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
```

2. **Turso** (SQLite-compatible, great for this app)
```python
# Install: python -m pip install libsql-experimental
from libsql_client import create_client
client = create_client(TURSO_URL, auth_token=TURSO_TOKEN)
```

3. **PostgreSQL** (Render, Heroku, AWS RDS)
4. **Firebase Firestore**

### Geolocation API Rate Limits

- **ip-api.com**: 45 requests per minute (free tier)
- **ipapi.co**: 1000 requests per day (free tier)
- **ipwhois.io**: 10,000 requests per month (free tier)

The app automatically rotates between these APIs to stay within limits.

### Performance Optimization

- Add indexes on frequently queried columns (already implemented)
- Implement caching for static data
- Use pagination for large datasets
- Consider Redis for session management

### Security Considerations

- Validate all URLs before shortening
- Implement rate limiting for link creation
- Add custom domain support
- Use HTTPS in production (enforced by Streamlit Cloud)
- Sanitize all user inputs
- Consider adding CAPTCHA for public instances

### Privacy & GDPR Compliance

- Users are prompted for location permission (GDPR compliant)
- IP addresses are stored for analytics but can be anonymized
- No personal identifiable information (PII) is collected
- Users can request data deletion via reset button

---

**Made with ❤️ for the Philippines 🇵🇭**

*SmartLink - Shorten, Track, Analyze with Precision*

**Live App:** [https://smartlinkapp.streamlit.app/](https://smartlinkapp.streamlit.app/)
**GitHub Repo:** [https://github.com/querubin123/Smartlink-App](https://github.com/querubin123/Smartlink-App)
```

