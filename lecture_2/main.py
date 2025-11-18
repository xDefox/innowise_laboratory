def generate_profile(age: int) -> str:
    if 0 < age <= 12:
        return "Child"
    elif 13 <= age <= 19:
        return "Teenager"
    elif age >= 20:
        return "Adult"
    else:
        return "Invalid age"

# Сбор данных
user_name = input("Enter your full name: ")
birthday_year = int(input("Enter your birth year: "))
current_age = 2025 - birthday_year

# Сбор хобби
hobbies = []
while True:
    hobby = input("Enter a favorite hobby or type 'stop' to finish: ")
    if hobby.lower() == "stop":
        break
    if hobby not in hobbies:
        hobbies.append(hobby)
    else:
        print("You just said that.")

# Генерация стадии жизни
life_stage = generate_profile(current_age)

# Создание словаря профиля
user_profile = {
    "Name": user_name,
    "Age": current_age,
    "Life Stage": life_stage,
    "Hobbies": hobbies
}

# Вывод профиля
print("\n---")
print("Profile Summary:")
print(f"Name: {user_profile['Name']}")
print(f"Age: {user_profile['Age']}")
print(f"Life Stage: {user_profile['Life Stage']}")

if not user_profile["Hobbies"]:
    print("You didn't mention any hobbies.")
else:
    print(f"Favorite Hobbies ({len(user_profile['Hobbies'])}):")
    for h in user_profile["Hobbies"]:
        print(f"- {h}")
print("---")
