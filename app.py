import streamlit as st
from streamlit_geolocation import streamlit_geolocation
import sqlite3
import random
import string
import hashlib
from datetime import datetime, timedelta
import os as os_module
import tempfile
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import time
import urllib.parse
import json
import re

# Page config must be the first Streamlit command
st.set_page_config(
    page_title="SmartLink - Professional URL Shortener & Analytics",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def get_app_domain():
    """Automatically detect the correct domain for the app"""

    # 1) Best source: the current browser URL
    try:
        app_url = st.context.url
        if app_url:
            return app_url.rstrip("/")
    except:
        pass

    # 2) Fallback: request host header
    try:
        host = st.context.headers.get("host", "")
        if host:
            protocol = "https" if not host.startswith("localhost") else "http"
            return f"{protocol}://{host}"
    except:
        pass

    # 3) Local development fallback
    try:
        server_port = st.get_option("server.port") or 8501
        return f"http://localhost:{server_port}"
    except:
        return "http://localhost:8501"

# Get the automatically detected domain
app_domain = get_app_domain()

# Initialize session state
if 'show_success' not in st.session_state:
    st.session_state['show_success'] = False
if 'success_full_url' not in st.session_state:
    st.session_state['success_full_url'] = ""
if 'success_short_code' not in st.session_state:
    st.session_state['success_short_code'] = ""
if 'success_final_url' not in st.session_state:
    st.session_state['success_final_url'] = ""
if 'success_utm_params' not in st.session_state:
    st.session_state['success_utm_params'] = {}
if 'browser_location' not in st.session_state:
    st.session_state['browser_location'] = None
if 'geolocation_permission_granted' not in st.session_state:
    st.session_state['geolocation_permission_granted'] = False

# ============================================================================
# PROFESSIONAL MODERN DARK THEME CSS - ENHANCED UX
# ============================================================================
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Main theme colors */
    :root {
        --primary: #3b82f6;
        --primary-light: #60a5fa;
        --primary-dark: #2563eb;
        --primary-glow: rgba(59, 130, 246, 0.4);
        --success: #10b981;
        --success-light: #34d399;
        --warning: #f59e0b;
        --danger: #ef4444;
        --danger-light: #f87171;
        --bg-primary: #0a0f1e;
        --bg-secondary: #111827;
        --bg-card: #1a2332;
        --bg-card-hover: #1f2a3e;
        --text-primary: #f3f4f6;
        --text-secondary: #e5e7eb;
        --text-muted: #9ca3af;
        --border: #2d3748;
        --border-light: #3a4a5e;
        --shadow-sm: 0 2px 4px rgba(0,0,0,0.3);
        --shadow-md: 0 4px 8px rgba(0,0,0,0.4);
        --shadow-lg: 0 8px 16px rgba(0,0,0,0.5);
        --shadow-glow: 0 0 20px rgba(59, 130, 246, 0.2);
    }

    /* Global styles */
    .stApp {
        background: linear-gradient(135deg, #0a0f1e 0%, #0d1424 50%, #111827 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container padding optimization */
    .main .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        max-width: 1400px;
        margin: 0 auto;
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-secondary);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-dark);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary);
    }

    /* Title styling with glow effect */
    .main-title {
        text-align: center;
        padding: 0.75rem 0 0.25rem 0;
        background: linear-gradient(135deg, #60a5fa, #3b82f6, #2563eb, #1e40af);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.2rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em;
        margin-bottom: 0 !important;
        animation: fadeIn 0.6s ease-out;
        text-shadow: 0 0 30px rgba(59, 130, 246, 0.3);
    }

    .sub-title {
        text-align: center;
        color: var(--text-muted);
        font-size: 0.9rem;
        margin-bottom: 0.75rem;
        font-weight: 400;
        letter-spacing: 0.3px;
        animation: fadeInUp 0.6s ease-out;
    }

    /* Card styling with glass morphism */
    .card {
        background: rgba(26, 35, 50, 0.8);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(59, 130, 246, 0.15);
        border-radius: 20px;
        padding: 1.2rem;
        margin: 0.5rem 0;
        box-shadow: var(--shadow-md), var(--shadow-glow);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .card:hover {
        transform: translateY(-4px);
        border-color: rgba(59, 130, 246, 0.4);
        box-shadow: var(--shadow-lg), 0 0 30px rgba(59, 130, 246, 0.15);
    }

    /* URL display card */
    .url-card {
        background: linear-gradient(135deg, rgba(26, 35, 50, 0.9), rgba(31, 42, 62, 0.95));
        border: 1px solid var(--primary);
        border-radius: 20px;
        padding: 1rem;
        margin: 0.75rem 0;
        text-align: center;
        box-shadow: var(--shadow-md), 0 0 20px rgba(59, 130, 246, 0.2);
        animation: slideUp 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    .url-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.05), transparent);
        transition: left 0.5s ease;
    }

    .url-card:hover::before {
        left: 100%;
    }

    .short-url-display {
        font-size: 1.15rem;
        font-weight: 600;
        color: var(--primary-light);
        text-decoration: none;
        word-break: break-all;
        display: inline-flex;
        align-items: center;
        padding: 0.6rem 1.5rem;
        background: rgba(59, 130, 246, 0.1);
        border-radius: 40px;
        margin: 0.5rem 0;
        border: 1px solid var(--primary);
        transition: all 0.3s ease;
        gap: 0.25rem;
    }

    .short-url-display:hover {
        background: rgba(59, 130, 246, 0.2);
        transform: translateY(-2px) scale(1.02);
        box-shadow: var(--shadow-md);
        color: white;
    }

    .url-prefix {
        color: var(--text-muted);
        font-size: 0.9rem;
    }
    
    .url-code {
        color: var(--success);
        font-weight: 700;
        background: linear-gradient(135deg, var(--success), var(--success-light));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Metric cards grid */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 0.75rem;
        margin: 0.5rem 0;
    }

    .metric-card {
        background: linear-gradient(135deg, var(--bg-card), var(--bg-secondary));
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 0.75rem 0.5rem;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }

    .metric-card::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--primary), var(--success));
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }

    .metric-card:hover::after {
        transform: scaleX(1);
    }

    .metric-card:hover {
        transform: translateY(-4px);
        border-color: var(--primary);
        box-shadow: var(--shadow-md);
    }

    .metric-value {
        font-size: 1.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--primary), var(--primary-light));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.2;
        margin-bottom: 0.25rem;
    }

    .metric-label {
        color: var(--text-muted);
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        font-weight: 600;
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary), var(--primary-dark));
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        font-size: 0.85rem;
        transition: all 0.3s ease;
        text-transform: none;
        letter-spacing: 0.3px;
        height: auto;
        min-height: 38px;
        width: 100%;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }

    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s ease;
    }

    .stButton > button:hover::before {
        left: 100%;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
    }

    /* Input styling */
    .stTextInput > div > div > input {
        background-color: var(--bg-secondary);
        border: 1.5px solid var(--border);
        border-radius: 12px;
        color: var(--text-primary);
        padding: 0.6rem 1rem;
        font-size: 0.9rem;
        transition: all 0.3s ease;
    }

    .stTextInput > div > div > input:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
        background-color: var(--bg-card);
    }
    
    .stTextInput > div > div > input:hover {
        border-color: var(--primary-light);
    }
    
    /* Tooltip styling */
    .field-label {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.4rem;
        color: var(--text-muted);
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    .tooltip-container {
        position: relative;
        display: inline-block;
        cursor: help;
    }
    
    .tooltip-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 18px;
        height: 18px;
        border-radius: 50%;
        background: var(--primary);
        color: white;
        font-size: 11px;
        font-weight: bold;
        transition: all 0.2s ease;
    }
    
    .tooltip-icon:hover {
        background: var(--primary-light);
        transform: scale(1.1);
    }
    
    .tooltip-container .tooltip-text {
        visibility: hidden;
        width: 260px;
        background-color: var(--bg-card);
        color: var(--text-primary);
        text-align: left;
        border-radius: 12px;
        padding: 0.7rem;
        position: absolute;
        z-index: 1000;
        bottom: 125%;
        left: 50%;
        margin-left: -130px;
        opacity: 0;
        transition: opacity 0.3s, visibility 0.3s;
        border: 1px solid var(--primary);
        font-size: 0.75rem;
        line-height: 1.5;
        pointer-events: none;
        box-shadow: var(--shadow-lg);
    }
    
    .tooltip-container:hover .tooltip-text {
        visibility: visible;
        opacity: 1;
    }
    
    /* UTM Section styling */
    .utm-section {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.05), rgba(16, 185, 129, 0.03));
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 0.8rem;
        margin-top: 0.5rem;
    }
    
    .utm-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
        padding-bottom: 0.4rem;
        border-bottom: 1px solid var(--primary);
    }
    
    .utm-header h3 {
        color: var(--text-primary);
        margin: 0;
        font-size: 0.9rem;
        font-weight: 600;
    }
    
    .utm-badge {
        background: linear-gradient(135deg, var(--primary), var(--primary-dark));
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        font-size: 0.65rem;
        font-weight: 600;
        color: white;
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        color: var(--text-primary);
        font-weight: 600;
        padding: 0.6rem 1rem;
        font-size: 0.85rem;
        transition: all 0.3s ease;
    }

    .streamlit-expanderHeader:hover {
        border-color: var(--primary);
        background-color: var(--bg-card-hover);
        transform: translateX(4px);
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background-color: var(--bg-secondary);
        padding: 0.5rem;
        border-radius: 16px;
        border: 1px solid var(--border);
        margin-bottom: 0.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        padding: 0.5rem 1.2rem;
        color: var(--text-muted);
        font-weight: 500;
        font-size: 0.85rem;
        transition: all 0.3s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--primary), var(--primary-dark));
        color: white;
        box-shadow: var(--shadow-sm);
    }

    /* Alert styling */
    .stAlert {
        border-radius: 12px;
        border: none;
        padding: 0.7rem;
        font-size: 0.85rem;
        font-weight: 500;
    }

    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--primary), var(--success), transparent);
        margin: 1rem 0;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 1rem;
        color: var(--text-muted);
        border-top: 1px solid var(--border);
        margin-top: 1.5rem;
        background: linear-gradient(180deg, transparent, var(--bg-secondary));
        font-size: 0.75rem;
    }
    
    .footer p {
        margin: 0.2rem 0;
    }
    
    .footer-stats {
        display: flex;
        justify-content: center;
        gap: 1.5rem;
        flex-wrap: wrap;
        margin-bottom: 0.5rem;
    }

    /* Progress bar */
    .progress-bar {
        height: 6px;
        background: var(--bg-secondary);
        border-radius: 10px;
        overflow: hidden;
        margin: 0.3rem 0;
    }

    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--primary), var(--success));
        border-radius: 10px;
        transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    .progress-fill::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        animation: shimmer 2s infinite;
    }

    /* Recent click items */
    .recent-click {
        background: linear-gradient(135deg, #1e2a3a, #1a2332);
        border: 1px solid var(--border);
        border-left: 3px solid var(--primary);
        border-radius: 12px;
        padding: 0.6rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }

    .recent-click:hover {
        transform: translateX(4px);
        border-color: var(--primary-light);
        box-shadow: var(--shadow-sm);
    }
    
    /* Status badge */
    .status-badge {
        background: linear-gradient(135deg, #1a2332, #111827);
        padding: 0.3rem 1.2rem;
        border-radius: 30px;
        border: 1px solid var(--border);
        font-size: 0.75rem;
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        transition: all 0.3s ease;
    }
    
    .status-badge:hover {
        border-color: var(--primary);
        transform: translateY(-2px);
    }

    /* Warning modal */
    .warning-modal {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(239, 68, 68, 0.05));
        border: 1px solid var(--danger);
        border-radius: 12px;
        padding: 0.7rem;
        margin: 0.5rem 0;
    }
    
    .warning-title {
        color: var(--danger);
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 0.3rem;
        display: flex;
        align-items: center;
        gap: 0.3rem;
    }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes slideUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.2rem !important;
            padding: 0.5rem 0 !important;
        }
        .short-url-display {
            font-size: 0.85rem;
            padding: 0.4rem 1rem;
        }
        .metric-value {
            font-size: 1.3rem;
        }
        .metric-grid {
            grid-template-columns: repeat(2, 1fr);
            gap: 0.5rem;
        }
        .footer-stats {
            gap: 0.8rem;
        }
    }
    
    /* Loading spinner */
    .stSpinner > div {
        border-color: var(--primary) transparent transparent transparent !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# IMPROVED GEOLOCATION FUNCTIONS - DUAL METHOD (Browser + IP)
# ============================================================================

def get_browser_geolocation():
    """Get geolocation from browser using streamlit_geolocation"""
    try:
        location = streamlit_geolocation()
        
        if location and location != "No Location Info" and isinstance(location, dict):
            if location.get("latitude") and location.get("longitude"):
                st.session_state['browser_location'] = location
                st.session_state['geolocation_permission_granted'] = True
                return {
                    "source": "browser",
                    "latitude": location["latitude"],
                    "longitude": location["longitude"],
                    "accuracy": location.get("accuracy", "Unknown"),
                    "country": get_country_from_coords(location["latitude"], location["longitude"]),
                    "city": get_city_from_coords(location["latitude"], location["longitude"])
                }
    except Exception as e:
        print(f"Browser geolocation error: {e}")
    
    return None

def get_country_from_coords(lat, lon):
    """Get country name from coordinates using reverse geocoding"""
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
        response = requests.get(url, headers={'User-Agent': 'SmartLink URL Shortener'}, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get('address', {}).get('country', 'Unknown')
    except:
        pass
    return "Unknown"

def get_city_from_coords(lat, lon):
    """Get city name from coordinates using reverse geocoding"""
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
        response = requests.get(url, headers={'User-Agent': 'SmartLink URL Shortener'}, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get('address', {}).get('city', data.get('address', {}).get('town', data.get('address', {}).get('village', 'Unknown')))
    except:
        pass
    return "Unknown"

def get_real_ip():
    """Try to get the real IP address of the visitor using multiple sources"""
    ip_sources = [
        'https://api.ipify.org?format=json',
        'https://api.my-ip.io/ip.json',
        'https://ipapi.co/json/'
    ]
    
    for source in ip_sources:
        try:
            response = requests.get(source, timeout=5)
            if response.status_code == 200:
                if 'ipify' in source:
                    return response.json()['ip']
                elif 'my-ip.io' in source:
                    return response.json()['ip']
                elif 'ipapi.co' in source:
                    return response.json()['ip']
        except:
            continue
    
    # Fallback to get IP from headers (for deployed apps)
    try:
        client_ip = st.context.headers.get('X-Forwarded-For', '127.0.0.1')
        if client_ip:
            return client_ip.split(',')[0].strip()
    except:
        pass
    
    return "127.0.0.1"

def get_geolocation_from_ip(ip_address):
    """Get comprehensive geolocation from IP address using multiple APIs"""
    
    # Priority 1: Try ipapi.co (most reliable)
    try:
        response = requests.get(f"https://ipapi.co/{ip_address}/json/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('country_name') and data.get('country_name') != 'None':
                return {
                    "country": data.get("country_name", "Unknown"),
                    "city": data.get("city", "Unknown"),
                    "region": data.get("region", "Unknown"),
                    "lat": data.get("latitude", 0),
                    "lon": data.get("longitude", 0),
                    "isp": data.get("org", "Unknown"),
                    "timezone": data.get("timezone", "Unknown"),
                    "postal": data.get("postal", "Unknown"),
                    "source": "ipapi.co"
                }
    except:
        pass
    
    # Priority 2: Try ip-api.com
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}?fields=status,country,city,regionName,lat,lon,isp,timezone", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                return {
                    "country": data.get("country", "Unknown"),
                    "city": data.get("city", "Unknown"),
                    "region": data.get("regionName", "Unknown"),
                    "lat": data.get("lat", 0),
                    "lon": data.get("lon", 0),
                    "isp": data.get("isp", "Unknown"),
                    "timezone": data.get("timezone", "Unknown"),
                    "postal": "Unknown",
                    "source": "ip-api.com"
                }
    except:
        pass
    
    # Priority 3: Try ipwhois.io
    try:
        response = requests.get(f"https://ipwhois.io/json/{ip_address}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("success") != False and data.get("country"):
                return {
                    "country": data.get("country", "Unknown"),
                    "city": data.get("city", "Unknown"),
                    "region": data.get("region", "Unknown"),
                    "lat": float(data.get("latitude", 0)),
                    "lon": float(data.get("longitude", 0)),
                    "isp": data.get("isp", "Unknown"),
                    "timezone": data.get("timezone", "Unknown"),
                    "postal": data.get("postal", "Unknown"),
                    "source": "ipwhois.io"
                }
    except:
        pass
    
    # Final fallback
    return {
        "country": "Unknown",
        "city": "Unknown",
        "region": "Unknown",
        "lat": 0,
        "lon": 0,
        "isp": "Unknown",
        "timezone": "Unknown",
        "postal": "Unknown",
        "source": "none"
    }

def get_combined_geolocation():
    """Get geolocation from both browser (if available) and IP, then combine for best accuracy"""
    
    # Try browser geolocation first (most accurate)
    browser_geo = get_browser_geolocation()
    
    # Always get IP geolocation as fallback
    ip_address = get_real_ip()
    ip_geo = get_geolocation_from_ip(ip_address)
    
    # If browser geolocation is available and accurate, use it with IP as backup
    if browser_geo and browser_geo.get("latitude") and browser_geo.get("latitude") != 0:
        return {
            "country": browser_geo.get("country", ip_geo.get("country", "Unknown")),
            "city": browser_geo.get("city", ip_geo.get("city", "Unknown")),
            "region": ip_geo.get("region", "Unknown"),
            "lat": browser_geo["latitude"],
            "lon": browser_geo["longitude"],
            "isp": ip_geo.get("isp", "Unknown"),
            "timezone": ip_geo.get("timezone", "Unknown"),
            "postal": ip_geo.get("postal", "Unknown"),
            "source": "browser_gps",
            "ip_address": ip_address
        }
    
    # Otherwise use IP geolocation
    return {
        "country": ip_geo.get("country", "Unknown"),
        "city": ip_geo.get("city", "Unknown"),
        "region": ip_geo.get("region", "Unknown"),
        "lat": ip_geo.get("lat", 0),
        "lon": ip_geo.get("lon", 0),
        "isp": ip_geo.get("isp", "Unknown"),
        "timezone": ip_geo.get("timezone", "Unknown"),
        "postal": ip_geo.get("postal", "Unknown"),
        "source": ip_geo.get("source", "ip_detection"),
        "ip_address": ip_address
    }

def get_client_info():
    """Get comprehensive client information from request headers"""
    try:
        user_agent = st.context.headers.get('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    except:
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    
    device, browser, operating_system = parse_user_agent(user_agent)
    
    return {
        'user_agent': user_agent,
        'device': device,
        'browser': browser,
        'operating_system': operating_system
    }

def parse_user_agent(user_agent_string):
    """Parse user agent string to get device and browser info"""
    user_agent = user_agent_string.lower()
    
    if 'chrome' in user_agent and 'edg' not in user_agent and 'opr' not in user_agent:
        browser = 'Chrome'
    elif 'firefox' in user_agent:
        browser = 'Firefox'
    elif 'safari' in user_agent and 'chrome' not in user_agent:
        browser = 'Safari'
    elif 'edg' in user_agent:
        browser = 'Edge'
    elif 'opr' in user_agent or 'opera' in user_agent:
        browser = 'Opera'
    else:
        browser = 'Unknown'
    
    if 'windows' in user_agent:
        operating_system = 'Windows'
    elif 'mac' in user_agent:
        operating_system = 'macOS'
    elif 'linux' in user_agent:
        operating_system = 'Linux'
    elif 'android' in user_agent:
        operating_system = 'Android'
    elif 'ios' in user_agent or 'iphone' in user_agent or 'ipad' in user_agent:
        operating_system = 'iOS'
    else:
        operating_system = 'Unknown'
    
    if 'mobile' in user_agent or ('android' in user_agent and 'mobile' in user_agent):
        device = 'Mobile'
    elif 'tablet' in user_agent or 'ipad' in user_agent:
        device = 'Tablet'
    else:
        device = 'Desktop'
    
    return device, browser, operating_system

# ============================================================================
# DATABASE FUNCTIONS
# ============================================================================
def get_db_path():
    """Get database path"""
    if os_module.getenv('STREAMLIT_SERVER_ADDRESS'):
        return os_module.path.join(tempfile.gettempdir(), 'smartlink.db')
    return 'smartlink.db'

def init_db():
    """Initialize database tables with proper schema"""
    conn = None
    try:
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()
        
        c.execute('''CREATE TABLE IF NOT EXISTS links (
            id TEXT PRIMARY KEY,
            short_code TEXT UNIQUE NOT NULL,
            original_url TEXT NOT NULL,
            clicks INTEGER DEFAULT 0,
            created_date TEXT,
            last_clicked TEXT
        )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS clicks (
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
            geo_source TEXT DEFAULT 'ip_detection'
        )''')
        
        c.execute('''CREATE INDEX IF NOT EXISTS idx_clicks_short_code ON clicks(short_code)''')
        c.execute('''CREATE INDEX IF NOT EXISTS idx_clicks_click_time ON clicks(click_time)''')
        c.execute('''CREATE INDEX IF NOT EXISTS idx_clicks_country ON clicks(country)''')
        c.execute('''CREATE INDEX IF NOT EXISTS idx_clicks_geo_source ON clicks(geo_source)''')
        
        conn.commit()
    except Exception as e:
        print(f"Database initialization error: {e}")
    finally:
        if conn:
            conn.close()

def check_and_update_schema():
    """Check if the clicks table has all required columns and add them if missing"""
    conn = None
    try:
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()
        
        c.execute("PRAGMA table_info(clicks)")
        existing_columns = [column[1] for column in c.fetchall()]
        
        required_columns = {
            'city': 'TEXT DEFAULT "Unknown"',
            'region': 'TEXT DEFAULT "Unknown"',
            'latitude': 'REAL DEFAULT 0',
            'longitude': 'REAL DEFAULT 0',
            'isp': 'TEXT DEFAULT "Unknown"',
            'device_type': 'TEXT DEFAULT "Unknown"',
            'browser': 'TEXT DEFAULT "Unknown"',
            'browser_version': 'TEXT DEFAULT "Unknown"',
            'operating_system': 'TEXT DEFAULT "Unknown"',
            'referer': 'TEXT DEFAULT "Direct"',
            'user_agent': 'TEXT DEFAULT "Unknown"',
            'timezone': 'TEXT DEFAULT "Unknown"',
            'postal_code': 'TEXT DEFAULT "Unknown"',
            'geo_source': 'TEXT DEFAULT "ip_detection"'
        }
        
        for column, column_type in required_columns.items():
            if column not in existing_columns:
                try:
                    c.execute(f"ALTER TABLE clicks ADD COLUMN {column} {column_type}")
                except Exception as e:
                    pass
        
        conn.commit()
    except Exception as e:
        print(f"Error checking/updating schema: {e}")
    finally:
        if conn:
            conn.close()

# Initialize database and check/update schema
init_db()
check_and_update_schema()

# ============================================================================
# DATA RESET FUNCTIONS
# ============================================================================
def reset_all_data():
    """Delete all data from both tables and reset the database"""
    conn = None
    try:
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()
        
        c.execute("DELETE FROM links")
        c.execute("DELETE FROM clicks")
        c.execute("DELETE FROM sqlite_sequence WHERE name='clicks'")
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Error resetting data: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

def get_total_record_count():
    """Get total number of records in both tables"""
    conn = None
    try:
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()
        
        c.execute("SELECT COUNT(*) FROM links")
        links_count = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM clicks")
        clicks_count = c.fetchone()[0]
        
        return links_count, clicks_count
    except Exception as e:
        print(f"Error getting record count: {e}")
        return 0, 0
    finally:
        if conn:
            conn.close()

# ============================================================================
# HELPER FUNCTIONS
#============================================================================
def generate_short_code(length=6):
    """Generate a random short code"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def get_link(short_code):
    """Get a link by short code"""
    conn = None
    try:
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()
        c.execute("SELECT original_url FROM links WHERE short_code=?", (short_code,))
        result = c.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Error getting link: {e}")
        return None
    finally:
        if conn:
            conn.close()

def check_link_exists(short_code):
    """Check if a short code already exists"""
    conn = None
    try:
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()
        c.execute("SELECT short_code FROM links WHERE short_code=?", (short_code,))
        return c.fetchone() is not None
    except Exception as e:
        print(f"Error checking link: {e}")
        return False
    finally:
        if conn:
            conn.close()

def record_click(short_code):
    """Record a click for a short code with REAL analytics data using combined geolocation"""
    conn = None
    try:
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()
        
        click_time = datetime.now().isoformat()
        geo_data = get_combined_geolocation()
        client_info = get_client_info()
        
        referer = "Direct"
        try:
            referer = st.context.headers.get('Referer', 'Direct')
        except:
            pass
        
        c.execute("""
            INSERT INTO clicks (
                short_code, click_time, ip_address, 
                country, city, region, latitude, longitude, isp,
                device_type, browser, operating_system, referer, user_agent,
                timezone, postal_code, geo_source
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            short_code, click_time, geo_data.get('ip_address', 'Unknown'),
            geo_data['country'], geo_data['city'], geo_data['region'], 
            geo_data['lat'], geo_data['lon'], geo_data.get('isp', 'Unknown'),
            client_info['device'], client_info['browser'], client_info['operating_system'],
            referer, client_info['user_agent'],
            geo_data.get('timezone', 'Unknown'), geo_data.get('postal', 'Unknown'),
            geo_data.get('source', 'ip_detection')
        ))
        
        c.execute("""
            UPDATE links 
            SET clicks = clicks + 1, last_clicked = ? 
            WHERE short_code=?
        """, (click_time, short_code))
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Error recording click: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

def create_link(short_code, original_url):
    """Create a new short link"""
    conn = None
    try:
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()
        
        link_id = hashlib.md5(f"{short_code}{datetime.now()}".encode()).hexdigest()[:8]
        created = datetime.now().isoformat()
        
        c.execute("""
            INSERT INTO links (id, short_code, original_url, clicks, created_date) 
            VALUES (?, ?, ?, 0, ?)
        """, (link_id, short_code, original_url, created))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error creating link: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

def get_stats():
    """Get overall stats with accurate counting"""
    conn = None
    try:
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()
        
        c.execute("SELECT COUNT(*) FROM links")
        total_links = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM clicks")
        total_clicks = c.fetchone()[0]
        
        c.execute("SELECT COUNT(DISTINCT short_code) FROM clicks")
        active_links = c.fetchone()[0]
        
        c.execute("SELECT COUNT(DISTINCT country) FROM clicks WHERE country != 'Unknown'")
        total_countries = c.fetchone()[0]
        
        yesterday = (datetime.now() - timedelta(days=1)).isoformat()
        c.execute("SELECT COUNT(*) FROM clicks WHERE click_time >= ?", (yesterday,))
        clicks_24h = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM clicks WHERE geo_source = 'browser_gps'")
        gps_clicks = c.fetchone()[0]
        
        return total_links, total_clicks, active_links, total_countries, clicks_24h, gps_clicks
    except Exception as e:
        print(f"Error getting stats: {e}")
        return 0, 0, 0, 0, 0, 0
    finally:
        if conn:
            conn.close()

def get_country_stats():
    """Get click statistics by country"""
    conn = None
    try:
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()
        c.execute("""
            SELECT country, COUNT(*) as count 
            FROM clicks 
            WHERE country != 'Unknown'
            GROUP BY country 
            ORDER BY count DESC
        """)
        return c.fetchall()
    except Exception as e:
        print(f"Error getting country stats: {e}")
        return []
    finally:
        if conn:
            conn.close()

def get_device_stats():
    """Get click statistics by device type"""
    conn = None
    try:
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()
        c.execute("""
            SELECT device_type, COUNT(*) as count 
            FROM clicks 
            WHERE device_type != 'Unknown'
            GROUP BY device_type 
            ORDER BY count DESC
        """)
        return c.fetchall()
    except Exception as e:
        print(f"Error getting device stats: {e}")
        return []
    finally:
        if conn:
            conn.close()

def get_browser_stats():
    """Get click statistics by browser"""
    conn = None
    try:
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()
        c.execute("""
            SELECT browser, COUNT(*) as count 
            FROM clicks 
            WHERE browser != 'Unknown'
            GROUP BY browser 
            ORDER BY count DESC
        """)
        return c.fetchall()
    except Exception as e:
        print(f"Error getting browser stats: {e}")
        return []
    finally:
        if conn:
            conn.close()

def get_os_stats():
    """Get click statistics by operating system"""
    conn = None
    try:
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()
        c.execute("""
            SELECT operating_system, COUNT(*) as count 
            FROM clicks 
            WHERE operating_system != 'Unknown'
            GROUP BY operating_system 
            ORDER BY count DESC
        """)
        return c.fetchall()
    except Exception as e:
        print(f"Error getting OS stats: {e}")
        return []
    finally:
        if conn:
            conn.close()

def get_all_links():
    """Get all links with accurate data"""
    conn = None
    try:
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()
        c.execute("""
            SELECT short_code, original_url, clicks, created_date, last_clicked 
            FROM links 
            ORDER BY created_date DESC
        """)
        return c.fetchall()
    except Exception as e:
        print(f"Error getting links: {e}")
        return []
    finally:
        if conn:
            conn.close()

def get_recent_clicks(limit=10):
    """Get recent clicks with all details including geolocation source"""
    conn = None
    try:
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()
        c.execute("""
            SELECT short_code, click_time, country, city, device_type, browser, operating_system, geo_source
            FROM clicks 
            ORDER BY click_time DESC 
            LIMIT ?
        """, (limit,))
        return c.fetchall()
    except Exception as e:
        print(f"Error getting recent clicks: {e}")
        return []
    finally:
        if conn:
            conn.close()

def get_link_country_stats(short_code):
    """Get country statistics for a specific link"""
    conn = None
    try:
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()
        c.execute("""
            SELECT country, COUNT(*) as count 
            FROM clicks 
            WHERE short_code = ? AND country != 'Unknown'
            GROUP BY country 
            ORDER BY count DESC
        """, (short_code,))
        return c.fetchall()
    except Exception as e:
        print(f"Error getting link country stats: {e}")
        return []
    finally:
        if conn:
            conn.close()

def get_click_stats(days=7):
    """Get click statistics for charts"""
    conn = None
    try:
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()
        
        date_range = []
        for i in range(days - 1, -1, -1):
            date_range.append((datetime.now() - timedelta(days=i)).date().isoformat())
        
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        c.execute("""
            SELECT date(click_time) as date, COUNT(*) 
            FROM clicks 
            WHERE click_time >= ? 
            GROUP BY date(click_time) 
            ORDER BY date
        """, (cutoff,))
        
        result = dict(c.fetchall())
        timeline = [(date, result.get(date, 0)) for date in date_range]
        
        return timeline
    except Exception as e:
        print(f"Error getting click stats: {e}")
        return []
    finally:
        if conn:
            conn.close()

def get_hourly_stats():
    """Get click statistics by hour"""
    conn = None
    try:
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()
        c.execute("""
            SELECT strftime('%H', click_time) as hour, COUNT(*) 
            FROM clicks 
            GROUP BY hour 
            ORDER BY hour
        """)
        return c.fetchall()
    except Exception as e:
        print(f"Error getting hourly stats: {e}")
        return []
    finally:
        if conn:
            conn.close()

def get_geo_source_stats():
    """Get statistics on geolocation sources (browser GPS vs IP detection)"""
    conn = None
    try:
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()
        c.execute("""
            SELECT geo_source, COUNT(*) as count 
            FROM clicks 
            GROUP BY geo_source
            ORDER BY count DESC
        """)
        return c.fetchall()
    except Exception as e:
        print(f"Error getting geo source stats: {e}")
        return []
    finally:
        if conn:
            conn.close()

# ============================================================================
# UTM HELPER FUNCTIONS
# ============================================================================
def add_utm_parameters(base_url, utm_params):
    """Add UTM parameters to a URL"""
    utm_params = {k: v for k, v in utm_params.items() if v and v.strip()}
    
    if not utm_params:
        return base_url
    
    parsed = urllib.parse.urlparse(base_url)
    query_params = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
    
    for key, value in utm_params.items():
        if value and value.strip():
            query_params[key] = [value.strip()]
    
    new_query = urllib.parse.urlencode(query_params, doseq=True)
    new_parsed = parsed._replace(query=new_query)
    final_url = urllib.parse.urlunparse(new_parsed)
    
    return final_url

# ============================================================================
# REDIRECT HANDLER - WORKS WITH BOTH ?go= AND /code FORMATS
# ============================================================================

def handle_redirect():
    """Handle the redirect logic when a short link is accessed"""
    short_code = None
    
    try:
        if hasattr(st, 'query_params') and 'go' in st.query_params:
            short_code = st.query_params['go']
    except Exception as e:
        print(f"st.query_params error: {e}")
    
    if not short_code:
        try:
            if hasattr(st, 'context') and hasattr(st.context, 'path'):
                path = st.context.path
                if path:
                    clean_path = path.strip('/')
                    if clean_path and '.' not in clean_path and '/' not in clean_path:
                        short_code = clean_path
        except Exception as e:
            print(f"Path parsing error: {e}")
    
    if not short_code:
        try:
            ctx = st.runtime.scriptrunner.get_script_run_ctx()
            if ctx and hasattr(ctx, 'request'):
                if hasattr(ctx.request, 'url'):
                    full_url = str(ctx.request.url)
                    match = re.search(r'[?&]go=([^&]+)', full_url)
                    if match:
                        short_code = match.group(1)
                    else:
                        path_match = re.search(r'/([a-zA-Z0-9\-_]{3,10})(?:\?|$)', full_url)
                        if path_match:
                            short_code = path_match.group(1)
        except Exception as e:
            print(f"Context parsing error: {e}")
    
    if short_code:
        original_url = get_link(short_code)
        
        if original_url:
            try:
                record_click(short_code)
            except Exception as e:
                print(f"Click recording error: {e}")
            
            st.markdown(f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta http-equiv="refresh" content="0; url={original_url}">
                    <script>
                        window.location.href = "{original_url}";
                        window.location.replace("{original_url}");
                    </script>
                    <title>Redirecting...</title>
                    <style>
                        body {{
                            background: linear-gradient(135deg, #0a0f1e 0%, #111827 100%);
                            font-family: 'Inter', Arial, sans-serif;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            height: 100vh;
                            margin: 0;
                        }}
                        .redirect-box {{
                            text-align: center;
                            padding: 40px;
                            background: rgba(26, 35, 50, 0.9);
                            border-radius: 20px;
                            border: 1px solid #3b82f6;
                        }}
                        .spinner {{
                            border: 3px solid #2d3748;
                            border-top: 3px solid #3b82f6;
                            border-radius: 50%;
                            width: 40px;
                            height: 40px;
                            animation: spin 1s linear infinite;
                            margin: 20px auto;
                        }}
                        @keyframes spin {{
                            0% {{ transform: rotate(0deg); }}
                            100% {{ transform: rotate(360deg); }}
                        }}
                    </style>
                </head>
                <body>
                    <div class="redirect-box">
                        <div class="spinner"></div>
                        <h2>Redirecting you...</h2>
                        <p>If not redirected, <a href="{original_url}">click here</a></p>
                    </div>
                </body>
                </html>
            """, unsafe_allow_html=True)
            st.stop()
        else:
            st.markdown(f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <style>
                        body {{
                            background: linear-gradient(135deg, #0a0f1e 0%, #111827 100%);
                            font-family: 'Inter', Arial, sans-serif;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            height: 100vh;
                            margin: 0;
                        }}
                        .error-box {{
                            text-align: center;
                            padding: 50px;
                            background: rgba(26, 35, 50, 0.9);
                            border-radius: 20px;
                            border: 1px solid #ef4444;
                            max-width: 500px;
                        }}
                        h1 {{ color: #ef4444; font-size: 3rem; }}
                        .code {{
                            background: #1a2332;
                            padding: 10px 20px;
                            border-radius: 10px;
                            color: #60a5fa;
                            font-family: monospace;
                        }}
                        a {{
                            display: inline-block;
                            padding: 12px 24px;
                            background: #3b82f6;
                            color: white;
                            text-decoration: none;
                            border-radius: 10px;
                            margin-top: 20px;
                        }}
                    </style>
                </head>
                <body>
                    <div class="error-box">
                        <h1>404</h1>
                        <h2>Link Not Found</h2>
                        <div class="code">/{short_code}</div>
                        <a href="/">← Go to SmartLink Home</a>
                    </div>
                </body>
                </html>
            """, unsafe_allow_html=True)
            st.stop()

# Call the redirect handler at the very beginning
handle_redirect()

# ============================================================================
# MAIN UI - ENHANCED PROFESSIONAL LAYOUT
# ============================================================================

# Compact Header with animation
st.markdown('<h1 class="main-title">🔗 SmartLink</h1>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-title">Professional URL Shortener with Real-time Analytics • Track every click with precision</p>', unsafe_allow_html=True)

# Display current domain for reference
domain_display = app_domain.replace('https://', '').replace('http://', '')
st.markdown(f"""
<div style="text-align: center; margin-bottom: 0.5rem;">
    <span style="background: rgba(59, 130, 246, 0.15); padding: 0.25rem 1rem; border-radius: 30px; font-size: 0.7rem; color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.3);">
        🌐 Short Domain: {domain_display}
    </span>
</div>
""", unsafe_allow_html=True)

# Get stats for display
total_links, total_clicks, active_links, total_countries, clicks_24h, gps_clicks = get_stats()

# Professional status bar - Enhanced with geolocation info
st.markdown(f"""
<div style="display: flex; justify-content: center; gap: 0.8rem; margin-bottom: 1.5rem; flex-wrap: wrap;">
    <span class="status-badge">⚡ Real-time Analytics</span>
    <span class="status-badge">✓ 100% Free</span>
    <span class="status-badge">🔒 Secure & Reliable</span>
    <span class="status-badge">📊 UTM Tracking</span>
    <span class="status-badge">🌍 {total_countries} Countries</span>
    <span class="status-badge">📍 {gps_clicks} GPS-tracked</span>
</div>
""", unsafe_allow_html=True)

# Main two-column layout with professional spacing
left_col, right_col = st.columns([1.6, 1], gap="large")

with left_col:
    # Create new link section with enhanced card
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        col_icon, col_title = st.columns([0.08, 0.92])
        with col_icon:
            st.markdown("<span style='font-size: 1.3rem;'>✨</span>", unsafe_allow_html=True)
        with col_title:
            st.markdown("<h3 style='margin:0; color: #f3f4f6; font-size: 1.1rem; font-weight: 700;'>Create New Short Link</h3>", unsafe_allow_html=True)
        
        st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)
        
        with st.form("create_link_form", clear_on_submit=False):
            st.markdown("""
            <div class="field-label">
                <span>🔗</span> Destination URL
                <div class="tooltip-container">
                    <span class="tooltip-icon">?</span>
                    <span class="tooltip-text">The full URL you want to shorten. Users will be redirected here.</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            url = st.text_input("", placeholder="https://example.com/very/long/url/path", label_visibility="collapsed", key="destination_url")
            
            col_code, col_submit = st.columns([1.2, 0.8])
            with col_code:
                st.markdown("""
                <div class="field-label">
                    <span>🔑</span> Custom Code (Optional)
                    <div class="tooltip-container">
                        <span class="tooltip-icon">?</span>
                        <span class="tooltip-text">Choose a memorable short code. Letters, numbers, and hyphens only. Min 3 chars.</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                custom_code = st.text_input("", placeholder="my-campaign", label_visibility="collapsed", key="custom_code")
            
            with col_submit:
                st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
                submit = st.form_submit_button("🚀 Generate Short Link", use_container_width=True)
            
            with st.expander("📊 UTM Tracking Parameters (Optional)", expanded=False):
                st.markdown("<p style='color: #9ca3af; font-size: 0.75rem; margin-bottom: 0.75rem;'>Track your marketing campaigns with UTM parameters</p>", unsafe_allow_html=True)
                
                utm_col1, utm_col2 = st.columns(2)
                
                with utm_col1:
                    st.markdown("""
                    <div class="field-label">
                        <span>🎯</span> utm_source
                        <div class="tooltip-container">
                            <span class="tooltip-icon">?</span>
                            <span class="tooltip-text">Identifies the source of traffic (e.g., "google", "facebook", "newsletter").</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    utm_source = st.text_input("", placeholder="e.g., google, facebook", key="utm_source", label_visibility="collapsed")
                    
                    st.markdown("""
                    <div class="field-label">
                        <span>🔍</span> utm_medium
                        <div class="tooltip-container">
                            <span class="tooltip-icon">?</span>
                            <span class="tooltip-text">Identifies the marketing medium (e.g., "cpc", "email", "social").</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    utm_medium = st.text_input("", placeholder="e.g., cpc, email", key="utm_medium", label_visibility="collapsed")
                
                with utm_col2:
                    st.markdown("""
                    <div class="field-label">
                        <span>📢</span> utm_campaign
                        <div class="tooltip-container">
                            <span class="tooltip-icon">?</span>
                            <span class="tooltip-text">Identifies the specific campaign (e.g., "summer-sale", "black-friday").</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    utm_campaign = st.text_input("", placeholder="e.g., summer-sale", key="utm_campaign", label_visibility="collapsed")
                    
                    st.markdown("""
                    <div class="field-label">
                        <span>🏷️</span> utm_term
                        <div class="tooltip-container">
                            <span class="tooltip-icon">?</span>
                            <span class="tooltip-text">Identifies paid search keywords (e.g., "running+shoes").</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    utm_term = st.text_input("", placeholder="e.g., keyword+phrase", key="utm_term", label_visibility="collapsed")
                
                st.markdown("""
                <div class="field-label">
                    <span>📝</span> utm_content
                    <div class="tooltip-container">
                        <span class="tooltip-icon">?</span>
                        <span class="tooltip-text">Differentiates similar content or links within the same campaign (e.g., "cta-button", "banner-ad").</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                utm_content = st.text_input("", placeholder="e.g., cta-button, banner", key="utm_content", label_visibility="collapsed")
            
            if submit and url:
                if not url.startswith(('http://', 'https://')):
                    url = 'https://' + url
                
                utm_params = {
                    'utm_source': utm_source.strip() if utm_source else "",
                    'utm_medium': utm_medium.strip() if utm_medium else "",
                    'utm_campaign': utm_campaign.strip() if utm_campaign else "",
                    'utm_term': utm_term.strip() if utm_term else "",
                    'utm_content': utm_content.strip() if utm_content else ""
                }
                
                utm_params = {k: v for k, v in utm_params.items() if v}
                final_url = add_utm_parameters(url, utm_params)
                
                if custom_code:
                    short_code = custom_code.lower().replace(' ', '-')
                    short_code = ''.join(c for c in short_code if c.isalnum() or c == '-')
                    if not short_code or len(short_code) < 3:
                        short_code = generate_short_code()
                else:
                    short_code = generate_short_code()
                
                if check_link_exists(short_code):
                    st.error(f"❌ Code '{short_code}' is already taken. Try another one.")
                else:
                    if create_link(short_code, final_url):
                        full_url = f"{app_domain}/?go={short_code}"
                        
                        st.session_state['show_success'] = True
                        st.session_state['success_full_url'] = full_url
                        st.session_state['success_short_code'] = short_code
                        st.session_state['success_final_url'] = final_url
                        st.session_state['success_utm_params'] = utm_params
                        
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("Failed to create link. Please try again.")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ========== DISPLAY SUCCESS CONTENT OUTSIDE THE FORM ==========
if st.session_state.get('show_success', False):
    full_url = st.session_state['success_full_url']
    short_code = st.session_state['success_short_code']
    final_url = st.session_state['success_final_url']
    utm_params = st.session_state.get('success_utm_params', {})
    
    st.markdown("""
    <div style="margin: 0.5rem 0 1rem 0;">
    """, unsafe_allow_html=True)
    
    if utm_params:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(16, 185, 129, 0.08)); border-left: 4px solid #3b82f6; padding: 0.75rem 1rem; border-radius: 12px; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                <span style="font-size: 1rem;">📊</span>
                <strong style="color: #60a5fa; font-size: 0.85rem;">UTM Parameters Applied</strong>
            </div>
            <code style="color: #f59e0b; font-size: 0.75rem; background: rgba(0,0,0,0.3); padding: 0.4rem 0.7rem; border-radius: 8px; display: inline-block;">
                {' & '.join([f'{k}={v}' for k, v in utm_params.items()])}
            </code>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="url-card">
        <div style="position: absolute; top: 0.75rem; right: 0.75rem;">
            <span style="background: linear-gradient(135deg, #10b981, #059669); color: white; padding: 0.25rem 0.9rem; border-radius: 30px; font-size: 0.65rem; font-weight: 700;">✓ ACTIVE</span>
        </div>
        <div style="text-align: center; margin-bottom: 0.5rem;">
            <span style="color: #94a3b8; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1px;">Your Shortened URL</span>
        </div>
        <div class="url-container">
            <a href="{full_url}" target="_blank" class="short-url-display">
                <span class="url-prefix">{app_domain}/?go=</span>
                <span class="url-code">{short_code}</span>
            </a>
        </div>
        <div style="margin: 0.75rem 0; display: flex; gap: 0.75rem; justify-content: center; flex-wrap: wrap;">
            <span style="background: #1e2a3a; padding: 0.3rem 1rem; border-radius: 30px; font-size: 0.7rem;">📋 Code: {short_code}</span>
            <span style="background: #1e2a3a; padding: 0.3rem 1rem; border-radius: 30px; font-size: 0.7rem; color: #3b82f6;">🔗 {len(short_code)} chars</span>
            <span style="background: #1e2a3a; padding: 0.3rem 1rem; border-radius: 30px; font-size: 0.7rem; color: #f59e0b;">⚡ Just now</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="margin: 1rem 0 0.5rem 0;">
        <h4 style="color: #f3f4f6; font-size: 0.95rem; font-weight: 600; margin-bottom: 0.75rem;">📋 Copy Your Short Link</h4>
    </div>
    """, unsafe_allow_html=True)
    
    col_btn1, col_btn2 = st.columns([1, 1])
    
    with col_btn1:
        st.link_button("🔗 Test Short Link", full_url, use_container_width=True)
    
    with col_btn2:
        st.markdown("""
        <div style="background: #1a2332; border-radius: 12px; padding: 0.5rem; border: 1px solid #2d3748; text-align: center; height: 38px; display: flex; align-items: center; justify-content: center;">
            <span style="color: #10b981; font-size: 0.7rem;">✓ Link Active</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.code(full_url, language="text")
    
    clean_url = f"{app_domain}/{short_code}"
    st.markdown(f"""
    <div style="margin-top: 0.5rem; padding: 0.5rem; background: rgba(59, 130, 246, 0.05); border-radius: 8px; text-align: center;">
        <span style="color: #6b7280; font-size: 0.65rem;">Clean format also works: </span>
        <code style="color: #60a5fa; font-size: 0.7rem;">{clean_url}</code>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("✖️ Dismiss", key="clear_success", use_container_width=True):
        st.session_state['show_success'] = False
        st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

with right_col:
    # Enhanced Quick Stats Section
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    col_icon, col_title = st.columns([0.1, 0.9])
    with col_icon:
        st.markdown("<span style='font-size: 1.2rem;'>📊</span>", unsafe_allow_html=True)
    with col_title:
        st.markdown("<h3 style='margin:0; color: #f3f4f6; font-size: 1rem; font-weight: 700;'>Live Stats</h3>", unsafe_allow_html=True)
    
    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-card">
            <div class="metric-value">{total_links}</div>
            <div class="metric-label">Total Links</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{total_clicks}</div>
            <div class="metric-label">Total Clicks</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{active_links}</div>
            <div class="metric-label">Active Links</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{total_countries}</div>
            <div class="metric-label">Countries</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1e2a3a, #1a2332); padding: 0.85rem; border-radius: 14px; margin: 0.75rem 0; border-left: 4px solid #3b82f6;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span style="color: #94a3b8; font-size: 0.7rem; font-weight: 500;">⚡ LAST 24 HOURS</span>
            </div>
            <span style="font-size: 1.8rem; font-weight: 800; color: #60a5fa;">{clicks_24h}</span>
        </div>
        <div class="progress-bar" style="margin-top: 0.65rem;">
            <div class="progress-fill" style="width: {min(100, (clicks_24h/10)*100)}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Geolocation Source Stats
    geo_source_stats = get_geo_source_stats()
    if geo_source_stats:
        st.markdown("<div style='margin: 0.75rem 0 0.5rem 0;'><span style='font-size: 0.8rem; font-weight: 700; color: #e5e7eb;'>📍 Tracking Methods</span></div>", unsafe_allow_html=True)
        
        total = sum(count for _, count in geo_source_stats)
        for source, count in geo_source_stats:
            percentage = (count / total) * 100 if total > 0 else 0
            source_name = "🎯 GPS" if source == "browser_gps" else "🌐 IP Detection"
            color = "#10b981" if source == "browser_gps" else "#3b82f6"
            
            st.markdown(f"""
            <div style="margin: 0.4rem 0;">
                <div style="display: flex; justify-content: space-between; font-size: 0.7rem; margin-bottom: 0.25rem;">
                    <span style="color: #e5e7eb;">{source_name}</span>
                    <span style="color: {color}; font-weight: 700;">{count} ({percentage:.1f}%)</span>
                </div>
                <div class="progress-bar"><div class="progress-fill" style="width: {percentage}%; background: {color};"></div></div>
            </div>
            """, unsafe_allow_html=True)
    
    # Enhanced Top Countries Section
    st.markdown("<div style='margin: 1rem 0 0.5rem 0;'><span style='font-size: 0.8rem; font-weight: 700; color: #e5e7eb;'>🌍 Top Countries</span></div>", unsafe_allow_html=True)
    country_stats = get_country_stats()[:5]
    if country_stats:
        max_count = country_stats[0][1] if country_stats else 1
        for country, count in country_stats[:5]:
            percentage = (count / max_count) * 100
            flag = "🌍"
            if "United States" in country:
                flag = "🇺🇸"
            elif "Philippines" in country:
                flag = "🇵🇭"
            elif "United Kingdom" in country:
                flag = "🇬🇧"
            elif "Germany" in country:
                flag = "🇩🇪"
            elif "France" in country:
                flag = "🇫🇷"
            elif "Japan" in country:
                flag = "🇯🇵"
            
            st.markdown(f"""
            <div style="margin: 0.4rem 0;">
                <div style="display: flex; justify-content: space-between; font-size: 0.75rem; margin-bottom: 0.25rem;">
                    <span><span style="font-size: 1rem;">{flag}</span> {country[:25]}</span>
                    <span style="color: #3b82f6; font-weight: 700;">{count}</span>
                </div>
                <div class="progress-bar"><div class="progress-fill" style="width: {percentage}%;"></div></div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("📭 No country data yet. Share your links to see analytics!", icon="🌍")
    
    # Enhanced Recent Clicks Section
    st.markdown("<div style='margin: 1rem 0 0.5rem 0;'><span style='font-size: 0.8rem; font-weight: 700; color: #e5e7eb;'>🔄 Recent Clicks</span></div>", unsafe_allow_html=True)
    recent_clicks = get_recent_clicks(5)
    if recent_clicks:
        for click in recent_clicks[:5]:
            if len(click) >= 5:
                code, click_time_value, country, city, device, browser, os, geo_source = click[:8]
                try:
                    dt = datetime.fromisoformat(click_time_value)
                    time_str = dt.strftime("%H:%M")
                    date_str = dt.strftime("%b %d")
                except:
                    time_str = click_time_value[:5] if len(click_time_value) > 5 else click_time_value
                    date_str = "Today"
                
                flag = "🇺🇸" if "United States" in country else "🇵🇭" if "Philippines" in country else "🌍"
                geo_icon = "🎯" if geo_source == "browser_gps" else "🌐"
                
                st.markdown(f"""
                <div class="recent-click">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <strong style="color: #60a5fa; font-size: 0.8rem; font-family: monospace;">{code}</strong>
                        <div style="display: flex; gap: 0.5rem;">
                            <span style="color: #6b7280; font-size: 0.6rem; background: #2d3748; padding: 0.2rem 0.6rem; border-radius: 20px;">{date_str} {time_str}</span>
                        </div>
                    </div>
                    <div style="font-size: 0.7rem; margin-top: 0.3rem; display: flex; gap: 0.5rem; flex-wrap: wrap;">
                        <span>{flag} {country}</span>
                        {f'<span>• {city[:20]}</span>' if city and city != 'Unknown' else ''}
                        <span>• {geo_icon} {device}</span>
                        <span>• {browser}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("🖱️ No clicks yet. Share your short links to start tracking!", icon="📊")
    
    st.markdown("<div style='margin: 1rem 0 0.5rem 0;'></div>", unsafe_allow_html=True)
    col_refresh, col_status = st.columns([1, 1])
    with col_refresh:
        if st.button("🔄 Refresh Stats", use_container_width=True):
            st.rerun()
    with col_status:
        st.markdown(f"""
        <div style="background: #1e2a3a; border-radius: 10px; padding: 0.5rem; text-align: center;">
            <span style="color: #10b981; font-size: 0.7rem;">● Live</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr style='margin: 1rem 0;'>", unsafe_allow_html=True)
    links_count, clicks_count = get_total_record_count()
    
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 0.4rem; margin-bottom: 0.5rem;">
        <span style="font-size: 0.9rem;">⚠️</span>
        <h4 style="color: #f3f4f6; margin:0; font-size: 0.85rem;">Danger Zone</h4>
    </div>
    """, unsafe_allow_html=True)
    
    if links_count > 0 or clicks_count > 0:
        if 'reset_confirmed' not in st.session_state:
            st.session_state.reset_confirmed = False
        
        if not st.session_state.reset_confirmed:
            if st.button("🗑️ Reset All Data", use_container_width=True):
                st.session_state.reset_confirmed = True
                st.rerun()
        else:
            st.markdown(f"""
            <div class="warning-modal">
                <div class="warning-title">⚠️ DESTRUCTIVE ACTION</div>
                <p style="color: #f3f4f6; font-size: 0.75rem;">This will permanently delete:</p>
                <p style="color: #f59e0b; font-size: 0.9rem; font-weight: 700;">📊 {links_count} link(s) and {clicks_count} click(s)</p>
                <p style="color: #ef4444; font-size: 0.7rem;">⚠️ THIS ACTION CANNOT BE UNDONE! ⚠️</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Yes, Delete Everything", use_container_width=True):
                    if reset_all_data():
                        st.success("✅ All data has been permanently deleted!")
                        st.session_state.reset_confirmed = False
                        st.cache_data.clear()
                        st.rerun()
            with col2:
                if st.button("❌ Cancel", use_container_width=True):
                    st.session_state.reset_confirmed = False
                    st.rerun()
    else:
        st.button("🗑️ Reset All Data", disabled=True, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# ALL LINKS SECTION WITH ENHANCED ANALYTICS DASHBOARD
# ============================================================================
st.markdown("<hr style='margin: 1.5rem 0 1rem 0;'>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 3])
with col1:
    st.markdown("<h3 style='color: #f3f4f6; margin:0; font-size: 1.1rem;'>📋 Analytics Dashboard</h3>", unsafe_allow_html=True)
with col2:
    st.markdown("<p style='color: #6b7280; margin: 0; font-size: 0.75rem;'>Comprehensive insights into your links' performance</p>", unsafe_allow_html=True)

st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)

links = get_all_links()

if links:
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Overview", "🌍 Geographic", "📱 Devices", "📍 Tracking Methods", "🔗 Link Details"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="background: #1a2332; padding: 0.75rem; border-radius: 14px;">
                <span style="color: #f3f4f6; font-size: 0.85rem; font-weight: 600;">📊 Click Activity (Last 7 Days)</span>
            </div>
            """, unsafe_allow_html=True)
            
            click_timeline = get_click_stats(7)
            if click_timeline and any(clicks for _, clicks in click_timeline):
                df_timeline = pd.DataFrame(click_timeline, columns=['Date', 'Clicks'])
                fig = px.line(df_timeline, x='Date', y='Clicks', markers=True)
                fig.update_layout(height=250, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white', size=10))
                fig.update_traces(line_color='#3b82f6', line_width=2.5, marker=dict(size=6, color='#60a5fa'))
                st.plotly_chart(fig, use_container_width=True, key="daily_clicks_chart")
            else:
                st.info("No click data available yet", icon="📊")
        
        with col2:
            st.markdown("""
            <div style="background: #1a2332; padding: 0.75rem; border-radius: 14px;">
                <span style="color: #f3f4f6; font-size: 0.85rem; font-weight: 600;">⏰ Hourly Click Distribution</span>
            </div>
            """, unsafe_allow_html=True)
            
            hourly_stats = get_hourly_stats()
            if hourly_stats:
                df_hourly = pd.DataFrame(hourly_stats, columns=['Hour', 'Clicks'])
                fig = px.bar(df_hourly, x='Hour', y='Clicks')
                fig.update_layout(height=250, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white', size=10))
                fig.update_traces(marker_color='#3b82f6')
                st.plotly_chart(fig, use_container_width=True, key="hourly_clicks_chart")
            else:
                st.info("No hourly data available yet", icon="⏰")
        
        click_data = [(code, clicks) for code, _, clicks, _, _ in links if clicks > 0]
        if click_data:
            df = pd.DataFrame(click_data, columns=['Link', 'Clicks'])
            fig = px.pie(df, values='Clicks', names='Link', hole=0.3)
            fig.update_layout(height=320, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white', size=10))
            st.plotly_chart(fig, use_container_width=True, key="click_distribution_pie")
    
    with tab2:
        country_stats_tab = get_country_stats()
        if country_stats_tab:
            col1, col2 = st.columns(2)
            with col1:
                df_countries = pd.DataFrame(country_stats_tab, columns=['Country', 'Clicks'])
                fig = px.bar(df_countries.head(8), x='Country', y='Clicks', title='Top Countries')
                fig.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white', size=10))
                st.plotly_chart(fig, use_container_width=True, key="country_bar_chart_tab")
            with col2:
                fig = px.pie(df_countries.head(6), values='Clicks', names='Country', title='Distribution', hole=0.3)
                fig.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white', size=10))
                st.plotly_chart(fig, use_container_width=True, key="country_pie_chart_tab")
        else:
            st.info("No geographic data available yet", icon="🌍")
    
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            device_stats = get_device_stats()
            if device_stats:
                df_devices = pd.DataFrame(device_stats, columns=['Device', 'Clicks'])
                fig = px.pie(df_devices, values='Clicks', names='Device', title='Device Distribution', hole=0.3)
                fig.update_layout(height=280, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white', size=10))
                st.plotly_chart(fig, use_container_width=True, key="device_pie_chart_tab")
            
            os_stats = get_os_stats()
            if os_stats:
                df_os = pd.DataFrame(os_stats, columns=['OS', 'Clicks'])
                fig = px.bar(df_os, x='OS', y='Clicks', title='Operating Systems')
                fig.update_layout(height=220, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white', size=9))
                st.plotly_chart(fig, use_container_width=True, key="os_bar_chart_tab")
        
        with col2:
            browser_stats = get_browser_stats()
            if browser_stats:
                df_browsers = pd.DataFrame(browser_stats[:6], columns=['Browser', 'Clicks'])
                fig = px.bar(df_browsers, x='Browser', y='Clicks', title='Browser Distribution')
                fig.update_layout(height=380, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white', size=10))
                st.plotly_chart(fig, use_container_width=True, key="browser_bar_chart_tab")
    
    with tab4:
        col1, col2 = st.columns(2)
        with col1:
            geo_source_stats_tab = get_geo_source_stats()
            if geo_source_stats_tab:
                df_geo_source = pd.DataFrame(geo_source_stats_tab, columns=['Method', 'Count'])
                fig = px.pie(df_geo_source, values='Count', names='Method', title='Geolocation Source', hole=0.3)
                fig.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white', size=10))
                st.plotly_chart(fig, use_container_width=True, key="geo_source_pie_tab")
        
        with col2:
            st.markdown("""
            <div style="background: #1a2332; padding: 0.75rem; border-radius: 14px;">
                <h4 style="color: #f3f4f6; font-size: 0.8rem;">📖 About Tracking Methods</h4>
                <p style="font-size: 0.7rem; color: #9ca3af;"><strong style="color: #10b981;">🎯 GPS</strong> - Most accurate, requires user permission</p>
                <p style="font-size: 0.7rem; color: #9ca3af;"><strong style="color: #3b82f6;">🌐 IP Detection</strong> - Works without permission, less accurate</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab5:
        for idx, (code, url, clicks, created, last_clicked) in enumerate(links[:5]):
            try:
                created_dt = datetime.fromisoformat(created)
                created_str = created_dt.strftime("%Y-%m-%d %H:%M")
            except:
                created_str = created
            
            if last_clicked:
                try:
                    last_dt = datetime.fromisoformat(last_clicked)
                    last_str = last_dt.strftime("%Y-%m-%d %H:%M")
                except:
                    last_str = last_clicked
            else:
                last_str = "Never"
            
            link_full_url = f"{app_domain}/?go={code}"
            
            with st.expander(f"🔗 {code} — {clicks} click{'s' if clicks != 1 else ''}", expanded=False):
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown(f"**Short URL:** {link_full_url}")
                    st.markdown(f"**Original:** {url[:100]}...")
                    st.markdown(f"**Created:** {created_str}")
                    st.markdown(f"**Last Clicked:** {last_str}")
                with col2:
                    st.metric("Total Clicks", clicks)
                    st.link_button("🔗 Open", link_full_url, use_container_width=True)
                
                if clicks > 0:
                    link_countries = get_link_country_stats(code)
                    if link_countries:
                        df_link = pd.DataFrame(link_countries, columns=['Country', 'Clicks'])
                        fig = px.pie(df_link, values='Clicks', names='Country', hole=0.2)
                        fig.update_layout(height=200, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                        st.plotly_chart(fig, use_container_width=True, key=f"link_pie_{code}_{idx}")
        
        if len(links) > 5:
            st.info(f"📊 Showing 5 of {len(links)} links", icon="ℹ️")
else:
    st.markdown("""
    <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #1a2332, #111827); border-radius: 20px; border: 1px dashed #3b82f6;">
        <h3 style="color: #f3f4f6;">No Links Created Yet</h3>
        <p style="color: #9ca3af;">Create your first short link above!</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# ENHANCED COMPACT FOOTER
# ============================================================================
current_year = datetime.now().year

st.markdown(f"""
<div class="footer">
    <div class="footer-stats">
        <div><span style="color: #3b82f6;">{total_links}</span> Links</div>
        <div><span style="color: #10b981;">{total_clicks}</span> Clicks</div>
        <div><span style="color: #f59e0b;">{total_countries}</span> Countries</div>
        <div><span style="color: #ef4444;">{clicks_24h}</span> Last 24h</div>
        <div><span style="color: #8b5cf6;">{gps_clicks}</span> GPS Tracked</div>
    </div>
    <p>🔗 SmartLink URL Shortener • {domain_display} • Real-time Analytics • GPS Geolocation</p>
    <p>© {current_year} SmartLink • Made with ❤️ for the Philippines 🇵🇭</p>
</div>
""", unsafe_allow_html=True)