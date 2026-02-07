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
parts = [f'PART-{i:04d}' for i in range(1, 101)]

data = []

# Define date ranges for 2024 and 2025
date_ranges = [
    (datetime(2024, 1, 1), datetime(2024, 12, 31)),
    (datetime(2025, 1, 1), datetime(2025, 12, 31))
]

for i in range(num_samples):
    supplier = random.choice(suppliers)
    part_number = random.choice(parts)
    po_number = f'PO-{200000 + i}'
    
    # Pick a random date in 2024 or 2025
    dr = random.choice(date_ranges)
    po_created_dt = dr[0] + timedelta(days=random.randint(0, (dr[1] - dr[0]).days))
    
    # Base Price logic
    base_price = random.uniform(50.0, 500.0)
    if supplier == 'Supplier A': 
        price = base_price * 0.92 # Cheapest
    elif supplier == 'Supplier B':
        price = base_price * 1.08 # Premium
    else:
        price = base_price
    
    # Promise Date
    lead_time_promised = random.randint(7, 21)
    promise_dt = po_created_dt + timedelta(days=lead_time_promised)
    
    # Actual delivery performance
    if supplier == 'Supplier A':
        # Often late
        actual_delay = random.randint(-1, 12)
    elif supplier == 'Supplier B':
        # Usually early/on-time
        actual_delay = random.randint(-5, 1)
    else:
        # Average
        actual_delay = random.randint(-2, 5)
        
    delivered_dt = promise_dt + timedelta(days=actual_delay)
    on_time = 1 if (delivered_dt <= promise_dt) else 0
    
    data.append({
        'Supplier_Name': supplier,
        'Part_Number': part_number,
        'Price_USD': round(price, 2),
        'PO_Number': po_number,
        'PO_Created_Date': po_created_dt.strftime('%Y-%m-%d'),
        'Original_Promise_Date': promise_dt.strftime('%Y-%m-%d'),
        'Supplier_Delivered_Date': delivered_dt.strftime('%Y-%m-%d'),
        'Delivery_Speed_Days': (delivered_dt - po_created_dt).days,
        'Delay_Days': actual_delay,
        'On_Time_Delivery': on_time,
        'Year': po_created_dt.year
    })

df = pd.DataFrame(data)
df.to_csv('d:/Ashok Project -Kaggle/supplier_history_v2.csv', index=False)
print("Generated 10,000 samples for 2024-2025.")
