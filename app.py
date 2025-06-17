import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
from typing import Dict, List, Any
import uuid

# Configuration de la page
st.set_page_config(
    page_title="Outil PDCA Numérique",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS pour un meilleur design
st.markdown("""
<style>
    .pdca-header {
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #45B7D1, #96CEB4);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        color: white;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    
    .phase-card {
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid;
    }
    
    .plan-card { border-left-color: #FF6B
