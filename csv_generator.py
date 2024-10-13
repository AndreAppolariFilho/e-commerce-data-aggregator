import csv
import random
import datetime
import os


# Function to generate a random date between start and end dates
def random_date(start, end):
    return start + datetime.timedelta(
        seconds=random.randint(0, int((end - start).total_seconds()))
    )


# Parameters
file_name = 'sales_data.csv'
target_size_mb = 10  # Target size in megabytes
target_size_bytes = target_size_mb * 1024 * 1024  # Convert to bytes

# Random product names
products = ['Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Monitor',
            'Keyboard', 'Mouse', 'Printer', 'Camera', 'Smartwatch']

# Open a CSV file for writing
with open(file_name, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['sale_id', 'product_name', 'quantity', 'price', 'date'])  # Write headers

    sale_id = 1
    start_date = datetime.datetime(2020, 1, 1)
    end_date = datetime.datetime(2024, 12, 31)

    # Keep writing rows until file size reaches the target size
    while os.path.getsize(file_name) < target_size_bytes:
        product_name = random.choice(products)
        quantity = random.randint(1, 100)
        price = round(random.uniform(5.0, 100.0), 2)
        sale_date = random_date(start_date, end_date).strftime('%Y-%m-%d')

        # Write row to CSV
        writer.writerow([sale_id, product_name, quantity, price, sale_date])
        sale_id += 1

print(f"{file_name} has been generated with approximately {target_size_mb} MB of data.")