# Restaurant Seat Booking System

This is a **Restaurant Seat Booking System** built using Python and CSV files for data storage. The system allows users to view restaurants, make table reservations, and manage their bookings through a graphical user interface (GUI). The data is stored in CSV files, making it easy to manage and update.

## Features

- **Restaurant Management**: View restaurant details, including name, cuisine type, rating, location, and operating hours.
- **User Management**: Manage user information and their booking history.
- **Booking Management**: Make, view, and cancel reservations.
- **GUI Interface**: A user-friendly interface to interact with the system.

## CSV Files

The system uses the following CSV files to store data:

1. **restaurants.csv**: Stores restaurant information.
   - Columns: `restaurant_id`, `name`, `cuisine_type`, `rating`, `location`, `total_tables`, `table_configuration`, `opening_hours`, `closing_hours`

2. **users.csv**: Stores user information.
   - Columns: `user_id`, `name`, `email`, `phone_number`

3. **bookings.csv**: Stores booking records.
   - Columns: `booking_id`, `user_id`, `restaurant_id`, `date`, `time`, `table_id`, `party_size`, `status`

## Requirements

- Python 3.x
- `tkinter` (for GUI)
- `csv` (for handling CSV files)
- `tkcalendar` (for date selection)

## GUI Overview

### Main Window

- **Restaurant Display Section**: View and filter restaurants by cuisine type, rating, and search terms.
- **Booking Section**: Make reservations by selecting a date, time, party size, and table.
- **User Management Section**: View and cancel existing bookings for the selected user.

### Restaurant Display

- **List View**: Displays all restaurants with their name, cuisine type, and rating.
- **Filters**: Filter restaurants by cuisine type and minimum rating.
- **Search Bar**: Search for restaurants by name, cuisine type, or location.

### Booking Process

1. **Table Selection**:
   - Select a date and time.
   - Enter the party size.
   - View available tables and select one.
2. **Booking Confirmation**:
   - Review booking details.
   - Confirm the reservation and receive a booking ID.

### Cancellation Process

- **View Current Bookings**: View all active bookings for the selected user.
- **Cancel Booking**: Select a booking to cancel and confirm the cancellation.

## Code Structure

- **gui_component.py**: The main script that launches the GUI.
- **restaurant_classes.py**: Contains the `Restaurant` and `User` classes.
- **restaurant_functions.py**: Contains utility functions for loading data, filtering restaurants, and managing bookings.
- **restaurants.csv**: CSV file storing restaurant data.
- **users.csv**: CSV file storing user data.
- **bookings.csv**: CSV file storing booking records.

**Note**: This is a basic implementation of a Restaurant Seat Booking System. It can be extended with additional features like user authentication, advanced search, and more.
