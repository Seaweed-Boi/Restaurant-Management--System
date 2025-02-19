import csv
from datetime import datetime
import uuid

class Restaurant:
    def __init__(self, restaurant_id, name, cuisine_type, rating, location,total_tables, table_configuration, opening_hours, closing_hours):
        self.restaurant_id = restaurant_id
        self.name = name
        self.cuisine_type = cuisine_type
        self.rating = float(rating)
        self.location = location
        self.total_tables = int(total_tables)
        self.table_configuration = self._parse_table_config(table_configuration)
        self.opening_hours = opening_hours
        self.closing_hours = closing_hours

    #Convert string table configuration to dictionary
    def _parse_table_config(self, config_str):
        if isinstance(config_str, dict):
            return config_str
        config = {}
        pairs = config_str.split(',')
        for pair in pairs:
            seats, count = pair.split(':')
            config[int(seats)] = int(count)
        return config

    #Check table availability for given date, time and party size
    def get_available_tables(self, date, time, party_size):
        # Read current bookings
        booked_tables = self._get_booked_tables(date, time)
        
        # Find suitable table size for party
        suitable_sizes = [size for size in self.table_configuration.keys() if size >= party_size]
        if not suitable_sizes:
            return []
        
        min_suitable_size = min(suitable_sizes)
        available_tables = []
        
        # Generate available table IDs
        for size in suitable_sizes:
            for i in range(self.table_configuration[size]):
                table_id = f"T{size}_{i+1}"
                if table_id not in booked_tables:
                    available_tables.append({'table_id': table_id,'size': size})
                    
        return available_tables

    #Get list of booked tables for given date and time
    def _get_booked_tables(self, date, time):
        booked_tables = set()
        with open('bookings.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if (row['restaurant_id'] == self.restaurant_id and row['date'] == date and row['time'] == time and row['status'] == 'active'):
                    booked_tables.add(row['table_id'])

        return booked_tables

    #Verify if time is within operating hours
    def check_valid_booking_time(self, time):
        try:
            booking_time = datetime.strptime(time, '%H:%M').time()
            opening = datetime.strptime(self.opening_hours, '%H:%M').time()
            closing = datetime.strptime(self.closing_hours, '%H:%M').time()
            return opening <= booking_time <= closing
        except ValueError:
            return False

    #Format restaurant details for display
    def display_restaurant_info(self):
        return {
            'id': self.restaurant_id,
            'name': self.name,
            'cuisine': self.cuisine_type,
            'rating': self.rating,
            'location': self.location,
            'hours': f"{self.opening_hours} - {self.closing_hours}",
            'tables': self.table_configuration
        }

    def to_csv_format(self):
        """Convert restaurant data to CSV format"""
        table_config_str = ','.join([f"{seats}:{count}" for seats, count in self.table_configuration.items()])
        return [
            self.restaurant_id,
            self.name,
            self.cuisine_type,
            self.rating,
            self.location,
            self.total_tables,
            table_config_str,
            self.opening_hours,
            self.closing_hours
        ]

class User:
    def __init__(self, user_id, name, email, phone_number):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.phone_number = phone_number

    #Create a new reservation
    def make_reservation(self, restaurant_id, date, time, table_id, party_size):
        booking_id = f"B{str(uuid.uuid4())[:8]}"
        booking_data = {
            'booking_id': booking_id,
            'user_id': self.user_id,
            'restaurant_id': restaurant_id,
            'date': date,
            'time': time,
            'table_id': table_id,
            'party_size': party_size,
            'status': 'active'
        }
        
        with open('bookings.csv', 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=booking_data.keys())
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(booking_data)
        
        return booking_id

    #Cancel an existing reservation
    def cancel_reservation(self, booking_id):
        bookings = []
        cancelled = False
        
        with open('bookings.csv', 'r') as file:
            reader = csv.DictReader(file)
            bookings = list(reader)
            
        for booking in bookings:
            if (booking['booking_id'] == booking_id and 
                booking['user_id'] == self.user_id and
                booking['status'] == 'active'):

                booking['status'] = 'cancelled'
                cancelled = True
                
        if cancelled:
            with open('bookings.csv', 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=bookings[0].keys())
                writer.writeheader()
                writer.writerows(bookings)
                
        return cancelled

    #View booking history for user
    def view_booking_history(self):
        bookings = []
        with open('bookings.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['user_id'] == self.user_id:
                    bookings.append(row)
        return bookings

    #Format user details for display
    def to_csv_format(self):
        return [
            self.user_id,
            self.name,
            self.email,
            self.phone_number
        ]