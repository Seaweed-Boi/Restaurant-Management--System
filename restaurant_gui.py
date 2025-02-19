import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import restaurant_functions as rf

# Global variables to maintain state
restaurants = {}
users = {}
current_user = None
table_mapping = {}
 
# Main GUI elements that need to be accessed by multiple functions
root = None
restaurant_list = None
bookings_list = None
date_picker = None
time_combo = None
party_size_var = None
table_combo = None
search_var = None
cuisine_var = None
rating_var = None
user_var = None
table_var = None

def init_gui():
    global root, restaurants, users
    root = tk.Tk()
    root.title("Restaurant Booking System")
    root.geometry("1200x800")
    
    # Load data
    restaurants = rf.load_restaurants()
    users = rf.load_users()
    
    setup_main_interface()
    return root

def setup_main_interface():
    # Create main frames
    left_frame = ttk.Frame(root, padding="10")
    right_frame = ttk.Frame(root, padding="10")
    
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    setup_search_filters(left_frame)
    setup_restaurant_list(left_frame)
    setup_booking_form(right_frame)
    setup_user_section(right_frame)

def setup_search_filters(parent):
    global search_var, cuisine_var, rating_var
    
    # Search bar
    search_frame = ttk.Frame(parent)
    search_frame.pack(fill=tk.X, pady=5)
    
    ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
    search_var = tk.StringVar()
    search_var.trace('w', on_search)
    ttk.Entry(search_frame, textvariable=search_var).pack(
        side=tk.LEFT, fill=tk.X, expand=True, padx=5
    )
    
    # Filters
    filter_frame = ttk.Frame(parent)
    filter_frame.pack(fill=tk.X, pady=5)
    
    ttk.Label(filter_frame, text="Cuisine:").pack(side=tk.LEFT)
    cuisine_var = tk.StringVar(value="All")
    cuisine_types = ["All"] + rf.get_cuisine_types(restaurants)
    ttk.Combobox(filter_frame, textvariable=cuisine_var, 
                 values=cuisine_types).pack(side=tk.LEFT, padx=5)
    
    ttk.Label(filter_frame, text="Min Rating:").pack(side=tk.LEFT)
    rating_var = tk.StringVar(value="All")
    ttk.Combobox(filter_frame, textvariable=rating_var,
                 values=["All", "3+", "4+", "4.5+"]).pack(side=tk.LEFT, padx=5)
    
    # Bind filter changes
    cuisine_var.trace('w', apply_filters)
    rating_var.trace('w', apply_filters)

def setup_restaurant_list(parent):
    global restaurant_list
    
    list_frame = ttk.Frame(parent)
    list_frame.pack(fill=tk.BOTH, expand=True)
    
    restaurant_list = ttk.Treeview(list_frame, columns=('Name', 'Cuisine', 'Rating'),show='headings')
    restaurant_list.heading('Name', text='Name')
    restaurant_list.heading('Cuisine', text='Cuisine')
    restaurant_list.heading('Rating', text='Rating')
    
    scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=restaurant_list.yview)
    restaurant_list.configure(yscrollcommand=scrollbar.set)
    
    restaurant_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    restaurant_list.bind('<<TreeviewSelect>>', on_restaurant_select)
    update_restaurant_list()

def setup_booking_form(parent):
    global date_picker, time_combo, party_size_var, table_combo, table_var
    
    booking_frame = ttk.LabelFrame(parent, text="Make a Reservation", padding="10")
    booking_frame.pack(fill=tk.X, pady=10)
    
    # Date selection
    date_frame = ttk.Frame(booking_frame)
    date_frame.pack(fill=tk.X, pady=5)
    ttk.Label(date_frame, text="Date:").pack(side=tk.LEFT)
    date_picker = DateEntry(date_frame, width=12, background='darkblue',
                           foreground='white', borderwidth=2)
    date_picker.pack(side=tk.LEFT, padx=5)
    
    # Time selection
    time_frame = ttk.Frame(booking_frame)
    time_frame.pack(fill=tk.X, pady=5)
    ttk.Label(time_frame, text="Time:").pack(side=tk.LEFT)
    time_var = tk.StringVar()
    time_combo = ttk.Combobox(time_frame, textvariable=time_var)
    time_combo.pack(side=tk.LEFT, padx=5)
    
    # Party size
    party_frame = ttk.Frame(booking_frame)
    party_frame.pack(fill=tk.X, pady=5)
    ttk.Label(party_frame, text="Party Size:").pack(side=tk.LEFT)
    party_size_var = tk.StringVar(value="1")
    ttk.Spinbox(party_frame, from_=1, to=20, textvariable=party_size_var).pack(
        side=tk.LEFT, padx=5
    )
    
    # Table selection
    table_frame = ttk.Frame(booking_frame)
    table_frame.pack(fill=tk.X, pady=5)
    ttk.Label(table_frame, text="Available Tables:").pack(side=tk.LEFT)
    table_var = tk.StringVar()
    table_combo = ttk.Combobox(table_frame, textvariable=table_var)
    table_combo.pack(side=tk.LEFT, padx=5)
    
    # Add bindings
    date_picker.bind('<<DateEntrySelected>>', update_available_tables)
    time_combo.bind('<<ComboboxSelected>>', update_available_tables)
    party_size_var.trace('w', update_available_tables)
    
    # Book button
    ttk.Button(booking_frame, text="Make Reservation", 
               command=make_reservation).pack(pady=10)

def setup_user_section(parent):
    global bookings_list, user_var
    
    user_frame = ttk.LabelFrame(parent, text="User Management", padding="10")
    user_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    
    # User selection
    user_select_frame = ttk.Frame(user_frame)
    user_select_frame.pack(fill=tk.X, pady=5)
    ttk.Label(user_select_frame, text="Select User:").pack(side=tk.LEFT)
    user_var = tk.StringVar()
    user_combo = ttk.Combobox(user_select_frame, textvariable=user_var,
                             values=[user.name for user in users.values()])
    user_combo.pack(side=tk.LEFT, padx=5)
    user_combo.bind('<<ComboboxSelected>>', on_user_select)
    
    # Bookings list
    bookings_frame = ttk.Frame(user_frame)
    bookings_frame.pack(fill=tk.BOTH, expand=True, pady=5)
    
    bookings_list = ttk.Treeview(bookings_frame, 
                                columns=('Date', 'Time', 'Restaurant', 'Status'),
                                show='headings')
    bookings_list.heading('Date', text='Date')
    bookings_list.heading('Time', text='Time')
    bookings_list.heading('Restaurant', text='Restaurant')
    bookings_list.heading('Status', text='Status')
    
    scrollbar = ttk.Scrollbar(bookings_frame, orient=tk.VERTICAL, 
                             command=bookings_list.yview)
    bookings_list.configure(yscrollcommand=scrollbar.set)
    
    bookings_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Cancel booking button
    ttk.Button(user_frame, text="Cancel Selected Booking", 
               command=cancel_booking).pack(pady=5)

def on_search(*args):
    update_restaurant_list()

def apply_filters(*args):
    update_restaurant_list()

def update_restaurant_list():
    # Clear current list
    for item in restaurant_list.get_children():
        restaurant_list.delete(item)
    
    # Apply filters
    filtered_restaurants = list(restaurants.values())
    
    # Apply cuisine filter
    if cuisine_var.get() != "All":
        filtered_restaurants = [r for r in filtered_restaurants 
                             if r.cuisine_type == cuisine_var.get()]
    
    # Apply rating filter
    rating_filter = rating_var.get()
    if rating_filter != "All":
        min_rating = float(rating_filter.replace("+", ""))
        filtered_restaurants = [r for r in filtered_restaurants 
                             if r.rating >= min_rating]
    
    # Apply search
    search_term = search_var.get().lower()
    if search_term:
        filtered_restaurants = [r for r in filtered_restaurants 
                             if search_term in r.name.lower() or 
                             search_term in r.cuisine_type.lower()]
    
    # Update list
    for restaurant in filtered_restaurants:
        restaurant_list.insert('', 'end', values=(
            restaurant.name,
            restaurant.cuisine_type,
            f"{restaurant.rating:.1f}"
        ))

def on_restaurant_select(event):
    selection = restaurant_list.selection()
    if not selection:
        return
    
    restaurant_name = restaurant_list.item(selection[0])['values'][0]
    selected_restaurant = next(r for r in restaurants.values() 
                            if r.name == restaurant_name)
    
    update_time_slots(selected_restaurant)
    update_available_tables()

def update_time_slots(restaurant):
    time_slots = rf.get_available_time_slots(restaurant, date_picker.get_date())
    time_combo['values'] = time_slots

def update_available_tables(*args):
    global table_mapping
    
    selection = restaurant_list.selection()
    if not selection or not party_size_var.get():
        return
    
    restaurant_name = restaurant_list.item(selection[0])['values'][0]
    restaurant = next(r for r in restaurants.values() if r.name == restaurant_name)
    
    date_str = date_picker.get_date().strftime('%Y-%m-%d')
    time_str = time_combo.get()
    party_size = int(party_size_var.get())
    
    available_tables = restaurant.get_available_tables(date_str, time_str, party_size)
    
    # Store table_id mapping
    table_mapping = {f"Table {t['table_id']} ({t['size']} seats)": t['table_id'] 
                    for t in available_tables}
    
    table_combo['values'] = list(table_mapping.keys())

def make_reservation():
    global current_user
    
    if not current_user:
        messagebox.showerror("Error", "Please select a user first")
        return
        
    selection = restaurant_list.selection()
    if not selection:
        messagebox.showerror("Error", "Please select a restaurant")
        return
        
    if not all([date_picker.get(), time_combo.get(), 
               party_size_var.get(), table_var.get()]):
        messagebox.showerror("Error", "Please fill all booking details")
        return
        
    restaurant_name = restaurant_list.item(selection[0])['values'][0]
    restaurant = next(r for r in restaurants.values() if r.name == restaurant_name)
    
    # Get table_id from mapping
    table_id = table_mapping.get(table_var.get())
    if not table_id:
        messagebox.showerror("Error", "Invalid table selection")
        return
    
    # Make reservation
    booking_id = current_user.make_reservation(
        restaurant.restaurant_id,
        date_picker.get_date().strftime('%Y-%m-%d'),
        time_combo.get(),
        table_id,
        int(party_size_var.get())
    )
    
    messagebox.showinfo("Success", f"Booking confirmed! Booking ID: {booking_id}")
    update_bookings_list()

def on_user_select(event):
    global current_user
    user_name = user_var.get()
    current_user = next(u for u in users.values() if u.name == user_name)
    update_bookings_list()

def update_bookings_list():
    # Clear current list
    for item in bookings_list.get_children():
        bookings_list.delete(item)
        
    if not current_user:
        return
        
    # Get user's bookings
    bookings = current_user.view_booking_history()
    
    # Update list
    for booking in bookings:
        restaurant = restaurants[booking['restaurant_id']]
        bookings_list.insert('', 'end', values=(
            booking['date'],
            booking['time'],
            restaurant.name,
            booking['status']
        ), tags=(booking['booking_id'],))

def cancel_booking():
    global current_user
    
    selection = bookings_list.selection()
    if not selection:
        messagebox.showerror("Error", "Please select a booking to cancel")
        return
        
    if not current_user:
        messagebox.showerror("Error", "Please select a user first")
        return
        
    booking_id = bookings_list.item(selection[0])['tags'][0]
    
    if current_user.cancel_reservation(booking_id):
        messagebox.showinfo("Success", "Booking cancelled successfully")
        update_bookings_list()
    else:
        messagebox.showerror("Error", "Failed to cancel booking")

if __name__ == "__main__":
    root = init_gui()
    root.mainloop()