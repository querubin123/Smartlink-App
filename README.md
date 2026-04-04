# 🔗 SmartLink - Professional URL Shortener & Analytics

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

A professional, feature-rich URL shortener with real-time analytics, geographic tracking, device detection, and UTM parameter support. Built with Streamlit and SQLite.

![SmartLink Demo](https://via.placeholder.com/800x400?text=SmartLink+URL+Shortener+Demo)

## ✨ Features

- **🔗 URL Shortening** - Create short, memorable links from long URLs
- **🎨 Custom Short Codes** - Personalize your links with custom aliases
- **📊 Real-time Analytics** - Track every click with detailed statistics
- **🌍 Geographic Tracking** - See which countries your visitors come from
- **📱 Device Detection** - Know if users are on desktop, mobile, or tablet
- **🌐 Browser & OS Stats** - Track browser and operating system usage
- **📈 UTM Parameters** - Track marketing campaigns with UTM tags
- **⏰ 24-Hour Activity** - Monitor recent click activity
- **🎨 Modern Dark Theme** - Professional, eye-friendly interface
- **📋 Easy Copy** - One-click copy functionality
- **🔒 Secure** - SQLite database with local storage

## 🚀 Live Demo

[View Live Demo](https://your-app-url.streamlit.app)

## 📋 Table of Contents

- [Installation](#installation)
- [Local Development](#local-development)
- [Deployment](#deployment)
- [Usage Guide](#usage-guide)
- [Analytics Dashboard](#analytics-dashboard)
- [UTM Tracking](#utm-tracking)
- [Database Schema](#database-schema)
- [Technologies Used](#technologies-used)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## 🛠️ Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

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
pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 💻 Local Development

### Requirements.txt

```txt
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.17.0
requests>=2.31.0
```

### Environment Variables

No environment variables are required for local development. The app uses:
- SQLite for database (auto-creates `smartlink.db`)
- ip-api.com for geolocation (free, no API key needed)
- ipify.org for IP detection (free)

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

### Deploy to Render

```bash
# Create render.yaml
services:
  - type: web
    name: smartlink
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.0
```

### Deploy to Heroku

```bash
# Create Procfile
web: streamlit run app.py --server.port $PORT --server.address 0.0.0.0

# Deploy
heroku create your-app-name
git push heroku main
heroku open
```

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
Short URL: http://localhost:8501/?go=abc123
Custom Short URL: http://localhost:8501/?go=my-project
```

### Tracking Analytics

- Each click is automatically tracked
- View real-time stats on the dashboard
- See geographic distribution on the map
- Analyze device and browser usage

## 📊 Analytics Dashboard

The dashboard provides comprehensive insights:

### Overview Tab
- Click activity over last 7 days (line chart)
- Hourly click distribution (bar chart)
- Click distribution by link (pie chart)

### Geographic Tab
- Top countries with click counts
- Geographic distribution pie chart
- Country-based progress bars

### Devices Tab
- Device type distribution (Desktop, Mobile, Tablet)
- Browser usage statistics
- Operating system breakdown

### Link Details Tab
- Individual link performance
- Country breakdown per link
- Click history and timestamps

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
Shortened: http://localhost:8501/?go=summer2024
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

### Clicks Table
```sql
CREATE TABLE clicks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    short_code TEXT,
    click_time TEXT,
    ip_address TEXT,
    country TEXT,
    city TEXT,
    region TEXT,
    latitude REAL,
    longitude REAL,
    device_type TEXT,
    browser TEXT,
    operating_system TEXT,
    referer TEXT,
    user_agent TEXT
);
```

## 🛠️ Technologies Used

- **Frontend**: Streamlit
- **Database**: SQLite3
- **Analytics**: Pandas, Plotly
- **Geolocation**: ip-api.com API
- **IP Detection**: ipify.org API
- **Styling**: Custom CSS, Google Fonts
- **Language**: Python 3.9+

## 📸 Screenshots

### Home Page
![Home Page](https://via.placeholder.com/800x400?text=Home+Page)

### Create Short Link
![Create Link](https://via.placeholder.com/800x400?text=Create+Short+Link)

### Analytics Dashboard
![Analytics](https://via.placeholder.com/800x400?text=Analytics+Dashboard)

### Geographic Tracking
![Geography](https://via.placeholder.com/800x400?text=Geographic+Tracking)

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
pip install -r requirements.txt

# Run tests (if available)
streamlit run app.py
```

## 📝 License

Distributed under the MIT License. See `LICENSE` file for more information.

## 📧 Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter) - email@example.com

Project Link: [https://github.com/querubin123/Smartlink-App](https://github.com/querubin123/Smartlink-App)

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) - Amazing framework for data apps
- [Plotly](https://plotly.com/) - Interactive visualizations
- [ip-api.com](http://ip-api.com/) - Free geolocation API
- [ipify.org](https://www.ipify.org/) - Simple IP detection API
- [Google Fonts](https://fonts.google.com/) - Inter font family

## ⭐ Show your support

Give a ⭐️ if this project helped you!

---

## 📌 Notes for Production Deployment

### Database Persistence on Streamlit Cloud

The SQLite database is ephemeral on Streamlit Cloud. For persistent storage, consider:

1. **Supabase** (Recommended)
```python
# Install: pip install supabase
from supabase import create_client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
```

2. **PostgreSQL** (Render, Heroku)
3. **Firebase Firestore**
4. **AWS RDS**

### Performance Optimization

- Add indexes on frequently queried columns
- Implement caching for static data
- Use pagination for large datasets
- Compress images and assets

### Security Considerations

- Validate all URLs before shortening
- Implement rate limiting
- Add custom domain support
- Use HTTPS in production
- Sanitize user inputs

---

**Made with ❤️ for the Philippines 🇵🇭**

*SmartLink - Shorten, Track, Analyze*
```

This README includes:
- Project overview and features
- Installation instructions
- Deployment guides for multiple platforms
- Usage examples
- Database schema documentation
- UTM tracking guide
- Contributing guidelines
- Production notes

