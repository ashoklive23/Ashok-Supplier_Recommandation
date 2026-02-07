import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Configuration
num_samples = 15000 # Increased for better statistical significance
suppliers = ['Supplier A', 'Supplier B', 'Supplier C']
parts = [f'PART-{i:04d}' for i in range(1, 101)]

data = []
date_ranges = [
    (datetime(2024, 1, 1), datetime(2024, 12, 31)),
    (datetime(2025, 1, 1), datetime(2025, 12, 31))
]

for i in range(num_samples):
    part_number = random.choice(parts)
    po_number = f'PO-{400000 + i}'
    
    # DETERMINE THE "STRIKE" WINNER FOR THIS PART
    part_id_int = int(part_number.split('-')[1])
    
    # Diversify the winner based on Part ID range
    if part_id_int <= 33:
        winner = 'Supplier A'
    elif part_id_int <= 66:
        winner = 'Supplier B'
    else:
        winner = 'Supplier C'
    
    # Assign supplier for THIS record (random, but winner gets better stats)
    supplier = random.choice(suppliers)
    
    # Pick a random date
    dr = random.choice(date_ranges)
    po_created_dt = dr[0] + timedelta(days=random.randint(0, (dr[1] - dr[0]).days))
    
    # --- DIVERSIFIED PERFORMANCE LOGIC ---
    if supplier == winner:
        # The winner for this part gets the BEST stats across all metrics
        price = random.uniform(50.0, 150.0) # Lower price
        lead_time_promised = random.randint(3, 7) # Faster promise
        actual_delay = random.randint(-5, 0) # Always on time or early
    else:
        # Non-winners get worse stats to ensure they lose the scoring
        price = random.uniform(160.0, 400.0) # Higher price
        lead_time_promised = random.randint(10, 25) # Slower promise
        actual_delay = random.randint(1, 15) # Likely late
        
    promise_dt = po_created_dt + timedelta(days=lead_time_promised)
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
print("SUCCESS: Generated 15,000 diversified records.")
print("Logic: Parts 1-33 > Supplier A | Parts 34-66 > Supplier B | Parts 67-100 > Supplier C")
