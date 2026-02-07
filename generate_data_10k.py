import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Seed for reproducibility
np.random.seed(42)
random.seed(42)

# Configuration
num_samples = 10000
suppliers = ['Supplier A', 'Supplier B', 'Supplier C']
parts = [f'PART-{i:04d}' for i in range(1, 101)] # 100 unique part numbers

data = []

start_date = datetime(2023, 1, 1)

for i in range(num_samples):
    supplier = random.choice(suppliers)
    part_number = random.choice(parts)
    po_number = f'PO-{100000 + i}'
    
    # Base Price in USD (Part dependent with some supplier variation)
    base_price = random.uniform(50.0, 500.0)
    if supplier == 'Supplier A': 
        price = base_price * 0.95 # Usually cheaper
    elif supplier == 'Supplier B':
        price = base_price * 1.05 # Usually more expensive
    else:
        price = base_price
    
    # Dates
    po_created_dt = start_date + timedelta(days=random.randint(0, 700))
    # Original Promise Date (usually 7-21 days after PO)
    lead_time_promised = random.randint(7, 21)
    promise_dt = po_created_dt + timedelta(days=lead_time_promised)
    
    # Supplier Delivered Date (Performance depends on supplier)
    if supplier == 'Supplier A':
        # Fast but sometimes late
        actual_delay = random.randint(-2, 10)
    elif supplier == 'Supplier B':
        # Reliable and very fast
        actual_delay = random.randint(-5, 2)
    else:
        # Average
        actual_delay = random.randint(-1, 5)
        
    delivered_dt = promise_dt + timedelta(days=actual_delay)
    
    # Delivery Speed Metric (Days taken to deliver from PO creation)
    delivery_speed_days = (delivered_dt - po_created_dt).days
    
    data.append({
        'Supplier_Name': supplier,
        'Part_Number': part_number,
        'Price_USD': round(price, 2),
        'PO_Number': po_number,
        'PO_Created_Date': po_created_dt.strftime('%Y-%m-%d'),
        'Original_Promise_Date': promise_dt.strftime('%Y-%m-%d'),
        'Supplier_Delivered_Date': delivered_dt.strftime('%Y-%m-%d'),
        'Delivery_Speed_Days': delivery_speed_days,
        'Delay_Days': actual_delay
    })

df = pd.DataFrame(data)
df.to_csv('d:/Ashok Project -Kaggle/supplier_history_10k.csv', index=False)
print("Generated 10,000 samples in supplier_history_10k.csv")
