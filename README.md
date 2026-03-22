# 🚗 BMW Sales Forecast — ML Deployment Project

ระบบพยากรณ์ยอดขายรถยนต์ BMW รายรุ่น โดยใช้ Machine Learning (Gradient Boosting Regression)  
พัฒนาด้วย Python + Scikit-learn และ Deploy ผ่าน Streamlit

---

## 📌 ปัญหาที่เลือกและเหตุผล

อุตสาหกรรมยานยนต์มีต้นทุนการผลิตและสต็อกสูงมาก การพยากรณ์ยอดขายล่วงหน้าที่แม่นยำช่วยให้  
ผู้ผลิตวางแผนการผลิต จัดการ inventory และตัดสินใจเชิงธุรกิจได้ดีขึ้น  

โปรเจคนี้ตอบคำถามว่า: **"รุ่น BMW รุ่นนี้ ในภูมิภาคนี้ เดือนหน้าจะขายได้กี่คัน?"**

---

## 📂 โครงสร้างไฟล์

```
bmw-predictor/
│
├── app.py                          # Streamlit web application
├── requirements.txt                # Python dependencies
├── BMW_Sales_Forecast_Lab.ipynb    # Jupyter Notebook (training pipeline)
│
└── bmw_artifacts/                  # Model artifacts (สร้างหลังรัน notebook)
    ├── bmw_sales_model.pkl         # Trained GradientBoostingRegressor pipeline
    ├── le_model.pkl                # LabelEncoder สำหรับ Model
    ├── le_region.pkl               # LabelEncoder สำหรับ Region
    ├── le_fuel_type.pkl            # LabelEncoder สำหรับ Fuel_Type
    ├── le_transmission.pkl         # LabelEncoder สำหรับ Transmission
    └── model_metadata.json         # Model metrics + feature mappings
```

---

## 📊 Dataset

- **ที่มา:** BMW Sales Dataset 2010–2024
- **ขนาด:** 50,000 records
- **Features:**

| Feature | ประเภท | คำอธิบาย |
|---------|--------|----------|
| Model | Categorical | รุ่นรถ BMW (23 รุ่น เช่น 3 Series, X5, i4) |
| Region | Categorical | ภูมิภาค (Asia, Europe, North America, ฯลฯ) |
| Fuel_Type | Categorical | ประเภทเชื้อเพลิง (Petrol, Diesel, Hybrid, Electric) |
| Transmission | Categorical | ระบบเกียร์ (Automatic, Manual) |
| Year | Numerical | ปีของข้อมูล (2010–2024) |
| Engine_Size_L | Numerical | ขนาดเครื่องยนต์ (ลิตร) |
| Mileage_KM | Numerical | ระยะทางสะสม (กิโลเมตร) |
| Price_USD | Numerical | ราคารถ (USD) |
| **Sales_Volume** | **Target** | **ยอดขายต่อเดือน (units)** |

---

## 🤖 Machine Learning Pipeline

### Algorithm ที่เลือก: Gradient Boosting Regressor

เลือก GBR เพราะ:
- จัดการ non-linear relationships ได้ดี
- ทนต่อ outliers มากกว่า Linear Regression
- ให้ feature importance ที่ตีความได้

### Pipeline

```
Input Features
    ↓
LabelEncoder (Categorical Features)
    ↓
StandardScaler
    ↓
GradientBoostingRegressor
    ↓
Sales Volume Prediction
```

### Hyperparameter Tuning (GridSearchCV)

```python
param_grid = {
    'regressor__n_estimators': [100, 200, 300],
    'regressor__max_depth':    [3, 5, 7],
    'regressor__learning_rate':[0.05, 0.1, 0.2],
    'regressor__subsample':    [0.8, 1.0]
}
```

### Model Performance

| Metric | Value |
|--------|-------|
| R² Score | ~0.88 |
| MAE | ~748 units |
| RMSE | ~950 units |
| Cross-validation | 5-Fold K-Fold |

---

## 🚀 วิธีติดตั้งและรัน

### 1. Clone repository

```bash
git clone https://github.com/<your-username>/bmw-predictor.git
cd bmw-predictor
```

### 2. ติดตั้ง dependencies

```bash
pip install -r requirements.txt
```

### 3. Train โมเดล (รัน Notebook)

เปิด `BMW_Sales_Forecast_Lab.ipynb` ใน Jupyter หรือ Google Colab  
แล้วรัน cell ทั้งหมดตามลำดับ → จะได้โฟลเดอร์ `bmw_artifacts/`

### 4. รัน Streamlit App

```bash
streamlit run app.py
```

เปิด browser ที่ `http://localhost:8501`

---

## 🌐 Deployed App

> 🔗 **[BMW Sales Intelligence Dashboard](#)**  
> *(แทนที่ด้วย URL จริงหลัง deploy บน Streamlit Cloud)*

---

## 📱 Features ของ App

- **KPI Dashboard** — แสดงค่าสถิติสำคัญของ model และ dataset
- **Vehicle Specification Input** — เลือกรุ่น ภูมิภาค เชื้อเพลิง เกียร์ และขนาดเครื่องยนต์
- **Fuel Type Dynamic** — ตัวเลือกเชื้อเพลิงเปลี่ยนตามรุ่นที่เลือก (เช่น i3 มีแค่ Electric)
- **Forecast Result** — แสดงยอดขายที่พยากรณ์ + เทียบกับค่าเฉลี่ย + Tier (HIGH/MID/LOW)
- **Historical Chart** — กราฟแนวโน้มยอดขายย้อนหลัง 2010–2024 พร้อม forecast point
- **All Models Comparison** — ตารางเปรียบเทียบพยากรณ์ทุกรุ่นด้วยเงื่อนไขเดียวกัน
- **Forecast Insights** — insight อัตโนมัติจาก model metrics

---

## 📦 Dependencies

```
streamlit>=1.32.0
scikit-learn>=1.5.0
pandas>=2.1.4
numpy>=1.26.3
joblib>=1.3.2
plotly>=5.18.0
```

---

## ⚠️ Disclaimer

ผลการพยากรณ์นี้สร้างจากโมเดล Machine Learning เพื่อวัตถุประสงค์ทางการศึกษาเท่านั้น  
ไม่ใช่ยอดขายจริงของ BMW Group AG และไม่ควรนำไปใช้ตัดสินใจเชิงธุรกิจจริง

---

## 👤 ผู้พัฒนา

| | |
|--|--|
| **ชื่อ** | *(ใส่ชื่อของคุณ)* |
| **รหัสนิสิต** | *(ใส่รหัสนิสิต)* |
| **วิชา** | ML Deployment Project |

---

*Last updated: March 2026*
