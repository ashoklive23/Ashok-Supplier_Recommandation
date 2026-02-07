# 🚛 Strategic Supplier Recommendation System

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ashok-supplier-recommendation.streamlit.app/)

## 📝 Project Overview
This is a **Production-Ready Strategic Sourcing Tool** designed to help procurement teams make data-driven decisions. The system analyzes historical Purchase Order (PO) data to recommend the best supplier for specific parts based on real-time organizational priorities like **Cost**, **Lead Time**, and **On-Time Delivery (OTD) Accuracy**.

Built for enterprise-scale analysis, the system processes **10,000+ transactional records** from 2024-2025 to generate high-confidence procurement recommendations.

## ✨ Key Features
- **Intelligent Decision Conclusion:** Real-time AI recommendation engine identifying the "Optimal Partner" for any selected part.
- **Dynamic Risk Analysis:** Explains not just why a supplier was selected, but specifically why alternate suppliers were rejected (Competitive Disadvantages).
- **Year-over-Year Tracking:** Compare performance metrics specifically for **2024 vs 2025**.
- **Three-Pillar Metrics:**
  - **Unit Price ($):** Tracks cost efficiency.
  - **Lead Time (Days):** Measures logistics agility.
  - **OTD %:** Monitors delivery reliability.
- **Production-Grade UI:** High-contrast Dark Theme designed for executive presentations and clear visibility.

## 🚀 Tech Stack
- **Python 3.x**
- **Streamlit** (Interactive Dashboard)
- **Pandas** (Data Processing)
- **NumPy** (Numerical Logic)
- **Git** (Version Control)

## 📂 Project Structure
- `streamlit_app.py`: The main production dashboard.
- `generate_data_v2.py`: Synthetic data engine creating 10,000+ historical PO records.
- `supplier_history_v2.csv`: The backend transactional database.
- `requirements.txt`: Project dependencies.

## 🛠️ Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/ashoklive23/Ashok-Supplier_Recommandation.git
   cd Ashok-Supplier_Recommandation
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application:**
   ```bash
   streamlit run streamlit_app.py
   ```

## 📊 Business Logic
The system uses a **Weighted Performance Scoring (WPS)** model:
- **Price (40%)**: Calculated as `Min_Price / Supplier_Price`.
- **Logistics (30%)**: Calculated as `Min_LeadTime / Supplier_LeadTime`.
- **Reliability (30%)**: Direct On-Time Delivery percentage.

---
Developed by **Ashok** | 2026 Procurement Intelligence Engine
