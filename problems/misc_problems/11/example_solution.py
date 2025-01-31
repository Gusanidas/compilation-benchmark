from datetime import datetime

users = {}
cars = {}
user_car_assignments = {}

def add_user(name, user_id, birthdate_str):
    try:
        birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d").date()
        users[user_id] = {"name": name, "birthdate": birthdate}
        return True
    except ValueError:
        return False

def add_car(car_id, make, model, horsepower):
    cars[car_id] = {"make": make, "model": model, "horsepower": horsepower}
    return True

def assign_car_to_user(user_id, car_id):
    if user_id in users and car_id in cars:
        if user_id not in user_car_assignments:
            user_car_assignments[user_id] = set()
        user_car_assignments[user_id].add(car_id)
        return True
    return False

def get_all_cars(user_id):
    if user_id in user_car_assignments:
        car_ids = sorted(list(user_car_assignments[user_id]))
        return ",".join(car_ids)
    return ""

def get_all_users(car_id):
    user_ids = []
    for user_id, car_set in user_car_assignments.items():
        if car_id in car_set:
            user_ids.append(user_id)
    return ",".join(sorted(user_ids))

def get_shared_car_users(user_id):
    if user_id not in user_car_assignments:
        return ""

    shared_users = set()
    user_cars = user_car_assignments[user_id]

    for other_user_id, other_user_cars in user_car_assignments.items():
        if other_user_id != user_id and any(car in user_cars for car in other_user_cars):
            shared_users.add(other_user_id)

    return ",".join(sorted(list(shared_users)))

def get_youngest_user_for_car(car_id):
    youngest_user = None
    youngest_birthdate = None

    for user_id, car_set in user_car_assignments.items():
        if car_id in car_set:
            birthdate = users[user_id]["birthdate"]
            if youngest_user is None or birthdate > youngest_birthdate:
                youngest_user = user_id
                youngest_birthdate = birthdate

    return youngest_user if youngest_user else ""

def get_top_K_powerful_cars(user_id, k):
    if user_id not in user_car_assignments:
        return ""

    user_cars = user_car_assignments[user_id]
    powerful_cars = []

    for car_id in user_cars:
        powerful_cars.append((cars[car_id]["horsepower"], car_id))

    powerful_cars.sort(reverse=True)

    top_k_cars = [car_id for _, car_id in powerful_cars[:k]]
    return ",".join(top_k_cars)

while True:
    try:
        line = input()
        if not line:
            break
        parts = line.split(": ")
        command = parts[0]
        args_str = parts[1]
        args = [arg.strip() for arg in args_str.split(",")]

        if command == "add_user":
            result = add_user(args[0], args[1], args[2])
            print(result)
        elif command == "add_car":
            result = add_car(args[0], args[1], args[2], int(args[3]))
            print(result)
        elif command == "assign_car_to_user":
            result = assign_car_to_user(args[0], args[1])
            print(result)
        elif command == "get_all_cars":
            result = get_all_cars(args[0])
            print(result)
        elif command == "get_all_users":
            result = get_all_users(args[0])
            print(result)
        elif command == "get_shared_car_users":
            result = get_shared_car_users(args[0])
            print(result)
        elif command == "get_youngest_user_for_car":
            result = get_youngest_user_for_car(args[0])
            print(result)
        elif command == "get_top_K_powerful_cars":
            result = get_top_K_powerful_cars(args[0], int(args[1]))
            print(result)


    except EOFError:
        break