import sys  # Import the sys module to exit the program

class Room:
    def __init__(self, room_number, room_type, price, amenities):
        self.room_number = room_number
        self.room_type = room_type
        self.price = price
        self.amenities = amenities  # List of amenities (e.g., Wi-Fi, air conditioning)
        self.is_occupied = False  # Track if the room is booked

    def __repr__(self):
        status = "Occupied" if self.is_occupied else "Available"
        return f"Room {self.room_number}: {self.room_type}, Price: ${self.price}, Amenities: {', '.join(self.amenities)}, Status: {status}"


class Hotel:
    def __init__(self, name):
        self.name = name
        self.rooms = []  # List to store rooms

    def add_room(self, room):
        self.rooms.append(room)

    def get_available_rooms(self):
        return [room for room in self.rooms if not room.is_occupied]

    def mark_room_occupied(self, room_number):
        for room in self.rooms:
            if room.room_number == room_number and not room.is_occupied:
                room.is_occupied = True
                return True
        return False


class Customer:
    def __init__(self, budget, preferred_room_type, required_amenities):
        self.budget = budget
        self.preferred_room_type = preferred_room_type
        self.required_amenities = required_amenities

    def filter_rooms(self, rooms):
        matching_rooms = [
            room for room in rooms
            if room.price <= self.budget
            and (self.preferred_room_type.lower() in room.room_type.lower() or self.preferred_room_type == "")
            and all(amenity.lower() in [a.lower() for a in room.amenities] for amenity in self.required_amenities if amenity)
        ]
        return matching_rooms

    def offer_room(self, hotel):
        while True:
            available_rooms = hotel.get_available_rooms()
            filtered_rooms = self.filter_rooms(available_rooms)

            if filtered_rooms:
                print("\nHere are the rooms that match your preferences:")
                for room in filtered_rooms:
                    print(room)
                self.select_room(hotel, filtered_rooms)
            else:
                print("\nNo rooms match your criteria. Let's try adjusting your preferences.")
                choice = input("Would you like to (1) Increase your budget, (2) Change room type, or (3) Exit? ").strip()

                if choice == "1":
                    try:
                        new_budget = float(input("Enter your new budget: $"))
                        self.budget = new_budget
                    except ValueError:
                        print("Invalid input. Please enter a valid budget amount.")
                elif choice == "2":
                    available_types = set(room.room_type for room in available_rooms)
                    print("Available room types:", available_types)
                    self.preferred_room_type = input("Enter a new preferred room type or leave blank for any: ")
                elif choice == "3":
                    print("Thank you for visiting. Have a great day!")
                    return
                else:
                    print("Invalid choice. Please enter 1, 2, or 3.")

    def select_room(self, hotel, rooms):
        while True:
            try:
                choice = int(input("Enter the room number you would like to book (or 0 to cancel): "))
                if choice == 0:
                    print("No room booked. Returning to the main menu.")
                    return
                for room in rooms:
                    if room.room_number == choice:
                        if hotel.mark_room_occupied(choice):
                            print(f"Congratulations! Room {choice} has been successfully booked.")
                            self.ask_for_more_booking(hotel)
                            return
                print("Invalid room number. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a valid room number.")

    def ask_for_more_booking(self, hotel):
        more_booking = input("Would you like to book another room? (yes/no): ").strip().lower()
        if more_booking == "yes":
            main()  # Restart the booking process
        elif more_booking == "no":
            leave_site = input("Would you like to (1) Exit the booking site or (2) Stay on the booking site? ").strip()
            if leave_site == "1":
                print("Thank you for using the Hotel Room Booking System! Have a great day!")
                sys.exit()  # Exit the program immediately
            elif leave_site == "2":
                print("You can browse more rooms or adjust your preferences.")
                return
            else:
                print("Invalid choice. Exiting the program.")
                sys.exit()  # Exit the program immediately
        else:
            print("Invalid input. Exiting the program.")
            sys.exit()  # Exit the program immediately


def main():
    hotel = Hotel("Grand Hotel")

    hotel.add_room(Room(101, "Single", 100, ["Wi-Fi", "TV"]))
    hotel.add_room(Room(102, "Double", 150, ["Wi-Fi", "TV", "Air Conditioning"]))
    hotel.add_room(Room(103, "Suite", 250, ["Wi-Fi", "TV", "Air Conditioning", "Mini Bar"]))
    hotel.add_room(Room(104, "Single", 90, ["Wi-Fi"]))
    hotel.add_room(Room(105, "Double", 140, ["Wi-Fi", "Air Conditioning"]))

    print("Welcome to the Hotel Room Booking System!\n")

    while True:
        try:
            budget = float(input("Enter your budget in USD: $"))
            if budget <= 0:
                print("Budget must be a positive number. Please try again.")
                continue
            break
        except ValueError:
            print("Invalid input! Please enter a valid number.")

    preferred_room_type = input("Enter your preferred room type (Single, Double, Suite, or leave blank for any): ")
    required_amenities = input("Enter required amenities (comma separated, e.g., Wi-Fi, TV, Air Conditioning, Mini Bar): ").split(',')

    customer = Customer(budget, preferred_room_type.strip(), [amenity.strip() for amenity in required_amenities if amenity.strip()])
    customer.offer_room(hotel)


if __name__ == "__main__":
    main()
