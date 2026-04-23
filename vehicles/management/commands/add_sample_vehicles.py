# apps/vehicles/management/commands/add_sample_vehicles.py

from django.core.management.base import BaseCommand
from vehicles.models import Vehicle

class Command(BaseCommand):
    help = 'Adds sample Tesla vehicles to the database'
    
    def handle(self, *args, **options):
        vehicles_data = [
            {
                'name': 'Tesla Model 3 Long Range',
                'model': 'model_3',
                'year': 2024,
                'condition': 'new',
                'price': 45990,
                'share_price': 459.90,
                'total_shares': 100,
                'available_shares': 100,
                'color': 'Pearl White',
                'battery_range': 358,
                'acceleration': 4.2,
                'features': 'Autopilot, Premium Audio, Glass Roof, Heated Seats',
                'autopilot': True,
                'premium_audio': True,
                'location': 'Los Angeles, CA'
            },
            {
                'name': 'Tesla Model Y Performance',
                'model': 'model_y',
                'year': 2024,
                'condition': 'new',
                'price': 52490,
                'share_price': 524.90,
                'total_shares': 100,
                'available_shares': 85,
                'color': 'Midnight Silver',
                'battery_range': 303,
                'acceleration': 3.5,
                'features': 'Autopilot, Performance Upgrade, 21" Wheels',
                'autopilot': True,
                'premium_audio': True,
                'location': 'San Francisco, CA'
            },
            {
                'name': 'Tesla Model S Plaid',
                'model': 'model_s',
                'year': 2024,
                'condition': 'new',
                'price': 89990,
                'share_price': 899.90,
                'total_shares': 100,
                'available_shares': 75,
                'color': 'Deep Blue',
                'battery_range': 396,
                'acceleration': 1.99,
                'features': 'Plaid Powertrain, Carbon Fiber Spoiler, Yoke Steering',
                'autopilot': True,
                'premium_audio': True,
                'location': 'Palo Alto, CA'
            },
        ]
        
        for data in vehicles_data:
            Vehicle.objects.create(**data)
            self.stdout.write(f"Added: {data['name']}")
        
        self.stdout.write(self.style.SUCCESS('Sample vehicles added successfully!'))