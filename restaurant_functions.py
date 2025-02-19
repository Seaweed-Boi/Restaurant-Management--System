import csv
from datetime import datetime,timedelta
from restaurant_classes import Restaurant, User

#Load all restaurants from CSV file
def load_restaurants():
    restaurants = {}
    with open('restaurants.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            restaurant = Restaurant(row['restaurant_id'],row['name'],row['cuisine_type'],row['rating'],row['location'],row['total_tables'],row['table_configuration'],row['opening_hours'],row['closing_hours'])

            restaurants[row['restaurant_id']] = restaurant
    return restaurants

#Load all users from CSV file
def load_users():
    users = {}
    with open('users.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            user = User(row['user_id'],row['name'],row['email'],row['phone_number'])
            users[row['user_id']] = user
    return users

#Filter restaurants based on cuisine type and minimum rating
def filter_restaurants(restaurants, cuisine_type=None, min_rating=None):
    filtered = restaurants.values()
    
    if cuisine_type:
        filtered = [r for r in filtered if r.cuisine_type.lower() == cuisine_type.lower()]
    
    if min_rating is not None:
        filtered = [r for r in filtered if r.rating >= float(min_rating)]
        
    return filtered

#Search restaurants by name
def search_restaurants(restaurants, search_term):
    search_term = search_term.lower()
    return [r for r in restaurants.values() if search_term in r.name.lower() or search_term in r.cuisine_type.lower() or search_term in r.location.lower()]

#Retrieve booking details by booking ID
def get_booking_by_id(booking_id):
    with open('bookings.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['booking_id'] == booking_id:
                return row
    return None

#Validate if booking date and time are in the future
def validate_booking_time(date_str, time_str):
    try:
        booking_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        current_datetime = datetime.now()
        return booking_datetime > current_datetime
    except ValueError:
        return False

#Get list of unique cuisine types
def get_cuisine_types(restaurants):
    return sorted(list(set(r.cuisine_type for r in restaurants.values())))

#Get available time slots for a given restaurant and date
def get_available_time_slots(restaurant, date):
    opening = datetime.strptime(restaurant.opening_hours, '%H:%M')
    closing = datetime.strptime(restaurant.closing_hours, '%H:%M')
    
    time_slots = []
    current = opening
    while current <= closing:
        time_slots.append(current.strftime('%H:%M'))
        current = datetime.strptime((datetime.combine(datetime.today(), current.time()) + timedelta(minutes=30)).strftime('%H:%M'),'%H:%M')
    
    return time_slots