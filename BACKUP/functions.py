import pandas as pd
import random
from faker import Faker

# Initialize Faker
fake = Faker()

# Constants for the clothing and accessories e-shop
CATEGORIES = [
    "Tops", "Bottoms", "Dresses", "Outerwear", 
    "Shoes", "Accessories", "Sportswear"
]

BRANDS = [
    "Nike", "Adidas", "Puma", "Zara", "H&M", 
    "Gucci", "Prada", "Levi's", "Ralph Lauren", 
    "Under Armour", "Calvin Klein", "New Balance", 
    "Tommy Hilfiger", "Versace", "Burberry"
]

ADJECTIVES = ["Classic", "Modern", "Stylish", "Luxury", "Casual", "Comfortable", "Premium"]
COLORS = ["Red", "Blue", "Black", "White", "Green", "Beige", "Pink", "Grey"]

def generate_behavioral_data(num_customers=2000):
    """
    Generates a behavioral dataset with customer purchase information, including deliberate errors.
    Returns:
        pandas.DataFrame: Dataset with customer behavioral data
    """
    behavioral_data = {
        "customer_id": [i for i in range(1, num_customers + 1)],
        "email": [fake.email() for _ in range(num_customers)],
        "total_spent": [round(random.uniform(20, 800), 2) for _ in range(num_customers)],
        "total_orders": [random.randint(1, 50) for _ in range(num_customers)],
        "avg_order_value": [],
        "last_purchase_days_ago": [random.randint(0, 365) for _ in range(num_customers)],
        "categories_bought": [random.randint(1, 6) for _ in range(num_customers)],
        "brands_bought": [random.randint(1, 6) for _ in range(num_customers)]
    }

    # Calculate average order value
    for i in range(num_customers):
        total_orders = behavioral_data["total_orders"][i]
        total_spent = behavioral_data["total_spent"][i]
        avg_value = total_spent / total_orders if total_orders > 0 else 0
        behavioral_data["avg_order_value"].append(round(avg_value, 2))

    # Generate invalid emails (10 random records)
    for _ in range(10):
        idx = random.randint(0, num_customers - 1)
        behavioral_data["email"][idx] = "invalid_email.com" if random.random() < 0.5 else "user@@example.com"

    # Missing average order values (5 random records)
    for _ in range(5):
        idx = random.randint(0, num_customers - 1)
        behavioral_data["avg_order_value"][idx] = None

    # Negative values (2 records)
    for _ in range(2):
        idx = random.randint(0, num_customers - 1)
        behavioral_data["total_spent"][idx] = -random.uniform(100, 500)
        behavioral_data["avg_order_value"][idx] = -random.uniform(50, 200)

    # Empty records (3 random records)
    for _ in range(3):
        idx = random.randint(0, num_customers - 1)
        behavioral_data["total_spent"][idx] = None
        behavioral_data["total_orders"][idx] = 0
        behavioral_data["avg_order_value"][idx] = None
        behavioral_data["categories_bought"][idx] = None
        behavioral_data["brands_bought"][idx] = None
        behavioral_data["last_purchase_days_ago"][idx] = None

    return pd.DataFrame(behavioral_data)

def generate_preference_data(num_customers=2000):
    """
    Generates a preference dataset for customers.
    Returns:
        pandas.DataFrame: Dataset with customer preferences
    """
    preference_data = {
        "customer_id": [i for i in range(1, num_customers + 1)],
        "top_category": [random.choice(CATEGORIES) for _ in range(num_customers)],
        "top_brand": [random.choice(BRANDS) for _ in range(num_customers)],
        "price_preference_range": [random.randint(1, 3) for _ in range(num_customers)],
        "discount_sensitivity": [round(random.uniform(0.0, 1.0), 2) for _ in range(num_customers)],
        "luxury_preference_score": [random.randint(1, 5) for _ in range(num_customers)]
    }
    return pd.DataFrame(preference_data)

def check_data_consistency(df):
    """
    Checks data consistency and returns a list of found problems.
    Args:
        df (pandas.DataFrame): Input dataset to check
    Returns:
        tuple: (list of problems, list of problem indices)
    """
    problems = []
    problem_indices = set()

    # Check emails
    invalid_emails = df[~df['email'].str.contains(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', regex=True)]
    if not invalid_emails.empty:
        problems.append(f"Found {len(invalid_emails)} invalid email addresses")
        problem_indices.update(invalid_emails.index)

    # Check null values
    null_records = df[df.isnull().any(axis=1)]
    if not null_records.empty:
        problems.append(f"Found {len(null_records)} records with missing values")
        problem_indices.update(null_records.index)

    # Check negative values
    negative_values = df[
        (df['total_spent'] < 0) |
        (df['total_orders'] < 0) |
        (df['avg_order_value'] < 0) |
        (df['last_purchase_days_ago'] < 0)
    ]
    if not negative_values.empty:
        problems.append(f"Found {len(negative_values)} records with negative values")
        problem_indices.update(negative_values.index)

    # Check average order value consistency
    mask = (df['total_orders'] > 0) & (df['total_spent'].notna()) & (df['avg_order_value'].notna())
    inconsistent_avg = df[mask].apply(
        lambda row: abs(row['total_spent'] / row['total_orders'] - row['avg_order_value']) > 0.01,
        axis=1
    )
    inconsistent_records = df[mask & inconsistent_avg]
    if not inconsistent_records.empty:
        problems.append(f"Found {len(inconsistent_records)} records with inconsistent average order value")
        problem_indices.update(inconsistent_records.index)

    return problems, list(problem_indices)

def generate_unique_product_name(unique_product_names):
    """Generates a unique product name."""
    while True:
        brand = random.choice(BRANDS)
        category = random.choice(CATEGORIES)
        adjective = random.choice(ADJECTIVES)
        color = random.choice(COLORS)
        product_name = f"{brand} {color} {adjective} {category}"
        if product_name not in unique_product_names:
            unique_product_names.add(product_name)
            return product_name

def generate_inventory_data(num_products=1000):
    """
    Generates an inventory dataset.
    Returns:
        pandas.DataFrame: Dataset with product inventory data
    """
    unique_product_names = set()
    
    inventory_data = {
        "product_id": [i for i in range(1, num_products + 1)],
        "product_name": [generate_unique_product_name(unique_product_names) for _ in range(num_products)],
        "category": [],
        "brand": [],
        "stock_quantity": [random.randint(0, 100) for _ in range(num_products)],
        "retail_price": [round(random.uniform(300, 5000), 2) for _ in range(num_products)],
        "cost_price": [],
        "profit_margin": []
    }

    # Populate category and brand based on product_name
    for product_name in inventory_data["product_name"]:
        split_name = product_name.split(" ")
        inventory_data["brand"].append(split_name[0])
        inventory_data["category"].append(split_name[-1])

    # Calculate cost_price and profit_margin
    for i in range(num_products):
        retail_price = inventory_data["retail_price"][i]
        profit_margin = round(random.uniform(50, 100), 2) / 100
        cost_price = round(retail_price * (1 - profit_margin), 2)
        inventory_data["cost_price"].append(cost_price)
        inventory_data["profit_margin"].append(round(profit_margin * 100, 2))

    return pd.DataFrame(inventory_data)
    