"""
Система управления студентами и их оценками.
Поддерживает добавление студентов, ввод оценок, генерацию отчетов
и поиск лучшего студента по среднему баллу.

Автор: [Владислав Мещеряк]
Версия: 1.1
"""

students = []  # Глобальный список для хранения данных о студентах


def calculate_averages():
    """
    Вычисляет средние оценки для всех студентов.

    Returns:
        list: Список средних оценок для каждого студента.
              Если у студента нет оценок, возвращает None.
    """
    averages = []
    for student in students:
        try:
            # Пытаемся вычислить среднюю оценку
            average = sum(student["grades"]) / len(student["grades"])
            averages.append(average)
        except ZeroDivisionError:
            # Обрабатываем случай, когда у студента нет оценок
            averages.append(None)
    return averages


def add_student():
    """
    Добавляет нового студента в систему.

    Запрашивает имя студента и создает новую запись
    с пустым списком оценок.
    """
    name = input("Input student name: ")
    new_student = {
        "name": name,
        "grades": []  # Инициализируем пустой список оценок
    }
    students.append(new_student)
    print(f"Student {name} added successfully.")


def add_grade():
    """
    Добавляет оценки для существующего студента.

    Функция:
    - Запрашивает имя студента
    - Находит студента в системе
    - Позволяет добавлять оценки по одной
    - Проверяет корректность введенных оценок (0-100)
    - Обрабатывает ошибки ввода
    """
    name = input("Input student name: ")

    found = False
    for student in students:
        if student["name"] == name:
            found = True
            # Цикл для добавления нескольких оценок
            while True:
                grade = input("Enter a grade (or 'done' to finish): ")

                if grade == "done":
                    break

                try:
                    grade = int(grade)
                    if 0 <= grade <= 100:
                        student["grades"].append(grade)
                        print("Grade added.")
                    else:
                        print("Grade must be between 0 and 100.")
                except ValueError:
                    print("ERROR: enter a valid number.")
            break

    if not found:
        print("ERROR: student is not found")


def generate_report():
    """
    Генерирует полный отчет по всем студентам.

    Функция:
    - Выводит средние оценки всех студентов
    - Обрабатывает студентов без оценок (выводит N/A)
    - Вычисляет общую статистику:
        * Максимальная средняя оценка
        * Минимальная средняя оценка
        * Общее среднее по всем студентам с оценками
    - Использует try/except для обработки ошибок деления на ноль
    """
    if not students:
        print("No students in the system.")
        return

    print("\n--- Student Report ---")
    averages = calculate_averages()

    valid_averages = []  # Список для валидных средних оценок

    for i, student in enumerate(students):
        avg = averages[i]
        if avg is None:  # Студент без оценок
            print(f"{student['name']}'s average grade is N/A.")
        else:
            # Форматируем вывод с одним знаком после запятой
            print(f"{student['name']}'s average grade is {avg:.1f}.")
            valid_averages.append(avg)

    # Вывод общей статистики (только если есть студенты с оценками)
    if valid_averages:
        print(f"\n--- Summary ---")
        print(f"Max average: {max(valid_averages):.1f}")
        print(f"Min average: {min(valid_averages):.1f}")
        print(f"Overall average: {sum(valid_averages) / len(valid_averages):.1f}")
    else:
        print("\nNo grades available for statistics.")


def find_best():
    """
    Находит студента с наивысшей средней оценкой.

    Функция:
    - Использует max() с lambda-функцией для поиска лучшего студента
    - Lambda-функция вычисляет среднюю оценку для каждого студента
    - Обрабатывает случаи, когда у студентов нет оценок
    - Выводит имя лучшего студента и его среднюю оценку
    """
    if not students:
        print("No students in the system.")
        return

    try:
        # Используем max() с lambda-функцией для поиска лучшего студента
        top_student = max(students,
                          key=lambda student: (
                              sum(student["grades"]) / len(student["grades"])
                              if student["grades"] else -1  # -1 для студентов без оценок
                          ))

        # Проверяем, что у лучшего студента есть оценки
        if top_student["grades"]:
            average = sum(top_student["grades"]) / len(top_student["grades"])
            print(f"Top student: {top_student['name']} with average grade: {average:.1f}")
        else:
            print("No students with grades available.")

    except ValueError:
        # Обрабатываем случай, когда нет студентов с оценками
        print("No students with grades available.")


def main():
    """
    Основная функция программы - главное меню.

    Предоставляет пользователю интерфейс для:
    - Добавления новых студентов
    - Добавления оценок
    - Генерации отчетов
    - Поиска лучшего студента
    - Выхода из программы

    Обрабатывает некорректный ввод и предоставляет
    повторные попытки для пользователя.
    """
    while True:
        print("\nStudents Management System")
        print("1. Add a new student")
        print("2. Add grades for a student")
        print("3. Generate a full report")
        print("4. Find the top student")
        print("5. Exit program")

        try:
            choice = int(input("Your input: "))

            # Обработка выбора пользователя с помощью match-case
            match choice:
                case 1:
                    add_student()
                case 2:
                    add_grade()
                case 3:
                    generate_report()
                case 4:
                    find_best()
                case 5:
                    print("Goodbye!")
                    break
                case _:
                    print("Please enter a number between 1-5.")

        except ValueError:
            print("Invalid input, please enter a number.")


# Запуск программы
if __name__ == "__main__":
    main()