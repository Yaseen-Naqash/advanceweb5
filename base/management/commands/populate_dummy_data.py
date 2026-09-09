# products/management/commands/populate_dummy_data.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from base.models import Category, Product
import random

class Command(BaseCommand):
    help = 'Populates the database with dummy data for Category and Product models'

    def handle(self, *args, **kwargs):
        # Clear existing data (optional)
        self.stdout.write('Clearing existing data...')
        Product.objects.all().delete()
        Category.objects.all().delete()
        
        # Create categories
        self.stdout.write('Creating categories...')
        category_data = [
            'Electronics',
            'Clothing',
            'Books',
            'Home & Garden',
            'Sports',
            'Toys',
            'Beauty',
            'Food',
            'Automotive',
            'Office Supplies'
        ]
        
        categories = []
        for category_title in category_data:
            category = Category.objects.create(
                title=category_title
            )
            categories.append(category)
            self.stdout.write(f'Created category: {category.title}')
        
        # Product names for dummy data
        product_names = {
            'Electronics': ['Smartphone X10', 'Laptop Pro 15', 'Wireless Earbuds', 'Smart Watch', 'Tablet Air'],
            'Clothing': ['Cotton T-Shirt', 'Denim Jeans', 'Winter Jacket', 'Running Shoes', 'Summer Dress'],
            'Books': ['Python Programming', 'Science Fiction Novel', 'Cookbook', 'Self Help Guide', 'History Book'],
            'Home & Garden': ['Garden Chair', 'Table Lamp', 'Coffee Table', 'Bed Sheets', 'Plant Pot'],
            'Sports': ['Yoga Mat', 'Dumbbells Set', 'Tennis Racket', 'Basketball', 'Fitness Tracker'],
            'Toys': ['Lego Set', 'Board Game', 'Action Figure', 'Puzzle', 'Remote Control Car'],
            'Beauty': ['Face Cream', 'Shampoo', 'Lipstick', 'Perfume', 'Hair Dryer'],
            'Food': ['Organic Coffee', 'Green Tea', 'Chocolate Box', 'Olive Oil', 'Pasta'],
            'Automotive': ['Car Charger', 'Floor Mats', 'Steering Cover', 'Air Freshener', 'Dash Cam'],
            'Office Supplies': ['Desk Organizer', 'Stapler', 'Notebook Set', 'Printer Paper', 'Whiteboard']
        }
        
        # Create products
        self.stdout.write('Creating products...')
        products_created = 0
        
        for category in categories:
            # Get product names for this category
            category_products = product_names.get(category.title, ['Generic Product'])
            
            # Create 5-10 products for each category
            num_products = random.randint(5, 10)
            
            for i in range(num_products):
                # Select a product name (cycle through available names)
                product_title = category_products[i % len(category_products)]
                
                # Add a number to make it unique if needed
                if i >= len(category_products):
                    product_title = f"{product_title} {i // len(category_products) + 1}"
                
                # Generate random price and discount
                price = random.randint(100, 10000)  # Price in cents/dollars
                discount = random.choice([0, 5, 10, 15, 20, 25, 30, 40, 50, None])
                
                # Create product
                product = Product.objects.create(
                    title=product_title,
                    category=category,
                    price=price,
                    discount=discount
                )
                products_created += 1
                
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {len(categories)} categories and {products_created} products!'
            )
        )