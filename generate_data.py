import pandas as pd
import numpy as np
import random

# Seed for reproducibility
np.random.seed(42)

# Configuration
num_samples = 1000
parts = ['Leafy Greens', 'Root Veggies', 'Cardboard Box', 'Plastic Wrap', 'Arabica Beans', 'Robusta Beans', 'Specialty Blend']
categories = ['Sayur', 'Sayur', 'Packaging', 'Packaging', 'Biji Kopi', 'Biji Kopi', 'Biji Kopi']
suppliers = ['Supplier A', 'Supplier B', 'Supplier C']

data = []

for i in range(num_samples):
    part_idx = random.randint(0, len(parts)-1)
    part_name = parts[part_idx]
    category = categories[part_idx]
    
    # Randomly assign a supplier (simulating past history)
    supplier = random.choice(suppliers)
    
    # Generate performance metrics for this specific order
    # Delivery Speed (1 = Fast, 3 = Slow)
    delivery_days = random.randint(1, 7)
    
    # Price per unit (randomly varies)
    price = round(random.uniform(10.0, 100.0), 2)
    
    # Quality score (1-10)
    quality_score = random.randint(5, 10)
    
    data.append({
        'Order_ID': f'ORD-{1000 + i}',
        'Part_Name': part_name,
        'Category': category,
        'Supplier': supplier,
        'Delivery_Days': delivery_days,
        'Price_Unit': price,
        'Quality_Score': quality_score
    })

df = pd.DataFrame(data)
df.to_csv('d:/Ashok Project -Kaggle/supplier_data.csv', index=False)
print("Generated 1000 samples in supplier_data.csv")
