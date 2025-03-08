import pandas as pd

# Class representing a single car with various attributes
class Car:
    def __init__(self, model, price, fuel_efficiency, brand, horsepower, safety_rating, color):
        self.model = model
        self.price = price
        self.fuel_efficiency = fuel_efficiency
        self.brand = brand
        self.horsepower = horsepower
        self.safety_rating = safety_rating
        self.color = color

    def __repr__(self):
        return f"{self.model} ({self.brand}): ${self.price}, {self.fuel_efficiency} MPG, Safety: {self.safety_rating} Stars"

# Class representing the car shop with available cars
class CarShop:
    def __init__(self):
        self.cars = []
    
    def add_car(self, car):
        self.cars.append(car)
    
    def get_available_cars(self):
        return self.cars

    def get_available_brands(self):
        return list(set(car.brand for car in self.cars))

# Class representing a car buyer and their preferences
class CarBuyer:
    def __init__(self, budget):
        self.budget = budget
        self.min_fuel_efficiency = 0
        self.brand_preference = ""
        self.min_safety_rating = 0

    def filter_cars(self, cars):
        # Filter available cars based on user preferences
        return [car for car in cars if car.price <= self.budget and
                (self.min_fuel_efficiency == 0 or car.fuel_efficiency >= self.min_fuel_efficiency) and
                (self.brand_preference == "" or self.brand_preference.lower() in car.brand.lower()) and
                (self.min_safety_rating == 0 or car.safety_rating >= self.min_safety_rating)]

    def recommend_car(self, car_shop):
        available_cars = car_shop.get_available_cars()
        available_brands = car_shop.get_available_brands()
        
        # Check if budget is too low and ask for increase
        min_price = min(car.price for car in available_cars)
        if self.budget < min_price:
            print(f"\nYour budget is too low. The cheapest available car starts at ${min_price}.")
            while True:
                choice = input("Would you like to increase your budget? (yes/no): ").strip().lower()
                if choice == "yes":
                    self.budget = float(input("Enter your new budget: $"))
                    self.get_preferences()
                    self.recommend_car(car_shop)
                    return
                elif choice == "no":
                    print("Exiting the car selection system.")
                    return
                else:
                    print("Invalid choice. Please type 'yes' or 'no'.")
        
        # Validate brand preference
        if self.brand_preference and self.brand_preference.lower() not in [brand.lower() for brand in available_brands]:
            print(f"\nThe brand '{self.brand_preference}' is not available. Available brands: {', '.join(available_brands)}")
            self.brand_preference = input("Please choose an available brand or leave blank for any: ").strip()
        
        filtered_cars = self.filter_cars(available_cars)
        
        # If no exact match, show all cars within budget
        if not filtered_cars:
            print("\nNo cars match your criteria. Showing all available cars within your budget:")
            filtered_cars = [car for car in available_cars if car.price <= self.budget]
        
        print("\nHere are the best-matching cars:")
        for car in filtered_cars:
            print(car)
        
        self.book_car(filtered_cars)
    
    def get_preferences(self):
        # Get additional buyer preferences
        self.min_fuel_efficiency = input("Enter the minimum fuel efficiency (in MPG) or press Enter to skip: ")
        self.brand_preference = input("Enter your preferred brand (leave blank for any): ")
        self.min_safety_rating = input("Enter the minimum safety rating (out of 5) or press Enter to skip: ")
        
        self.min_fuel_efficiency = float(self.min_fuel_efficiency) if self.min_fuel_efficiency else 0
        self.min_safety_rating = float(self.min_safety_rating) if self.min_safety_rating else 0

    def book_car(self, cars):
        # Allow user to book a car
        if cars:
            while True:
                choice = input("Would you like to book a car? (yes/no): ").strip().lower()
                if choice == "yes":
                    print("Please type the exact name of the car model from the list below:")
                    for car in cars:
                        print(f"- {car.model}")
                    selected_model = input("Enter the model name of the car you want to book: ").strip()
                    for car in cars:
                        if car.model.lower() == selected_model.lower():
                            print(f"\nCongratulations! You have successfully booked {car.model} ({car.brand}).")
                            return
                    print("Car not found in the matching list. Please enter the correct model name.")
                elif choice == "no":
                    print("No car booked. Returning to main menu.")
                    return
                else:
                    print("Invalid choice. Please type 'yes' or 'no'.")

# Create car shop and add car listings
car_shop = CarShop()
car_shop.add_car(Car('Honda Civic', 22000, 30, 'Honda', 158, 4.5, 'Red'))
car_shop.add_car(Car('Toyota Corolla', 21000, 32, 'Toyota', 139, 4.7, 'Blue'))
car_shop.add_car(Car('BMW 3 Series', 35000, 25, 'BMW', 255, 4.2, 'Black'))
car_shop.add_car(Car('Ford Focus', 20000, 28, 'Ford', 160, 4.3, 'White'))
car_shop.add_car(Car('Chevrolet Malibu', 23000, 26, 'Chevrolet', 160, 4.4, 'Silver'))
car_shop.add_car(Car('Nissan Altima', 25000, 27, 'Nissan', 182, 4.6, 'Grey'))
car_shop.add_car(Car('Mercedes C-Class', 40000, 24, 'Mercedes', 255, 4.8, 'Black'))
car_shop.add_car(Car('Audi A4', 39000, 26, 'Audi', 261, 4.7, 'White'))
car_shop.add_car(Car('Hyundai Elantra', 19500, 33, 'Hyundai', 147, 4.4, 'Blue'))
car_shop.add_car(Car('Mazda 3', 21000, 30, 'Mazda', 186, 4.5, 'Red'))

# Start the car selection process
print("Welcome to the Car Shop!\n")
try:
    budget = float(input("Enter your maximum budget (in USD): $"))
    buyer = CarBuyer(budget)
    buyer.get_preferences()
    buyer.recommend_car(car_shop)
except ValueError:
    print("Invalid input! Please enter valid numbers for budget, fuel efficiency, and safety rating.")
