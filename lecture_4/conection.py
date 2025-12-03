"""
Файл для создания, редактирования базы данных, создание SQL запросов с выводом для выполнения заданий

Автор: [Владислав Мещеряк]
Версия: 1.0
"""


import sqlite3
from typing import List, Tuple, Dict, Any


class SchoolDatabase:
    """Класс для работы с базой данных школы"""

    def __init__(self, db_name: str = 'school.db') -> None:
        """Инициализация подключения к базе данных"""
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def create_tables(self) -> None:
        """Создание таблиц студентов и оценок"""
        # Таблица студентов
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL UNIQUE,
                birth_year INTEGER
            )
        ''')

        # Таблица оценок
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS grades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                subject TEXT,
                grade INTEGER CHECK (grade >= 1 AND grade <= 100),
                FOREIGN KEY(student_id) REFERENCES students(id),
                UNIQUE(student_id, subject)
            )
        ''')

    def clear_existing_data(self) -> None:
        """Очистка существующих данных"""
        self.cursor.execute('DELETE FROM grades')
        self.cursor.execute('DELETE FROM students')

        # Сброс счетчиков AUTOINCREMENT
        self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='sqlite_sequence'"
        )
        if self.cursor.fetchone():
            self.cursor.execute('DELETE FROM sqlite_sequence WHERE name IN ("students", "grades")')

    def insert_students(self, students_data: List[Tuple[str, int]]) -> Dict[str, int]:
        """
        Вставка студентов и возврат словаря {имя: id}

        Args:
            students_data: Список кортежей (имя, год_рождения)

        Returns:
            Словарь с соответствием имен и ID студентов
        """
        student_ids = {}

        for full_name, birth_year in students_data:
            self.cursor.execute(
                'INSERT INTO students (full_name, birth_year) VALUES (?, ?)',
                (full_name, birth_year)
            )
            student_ids[full_name] = self.cursor.lastrowid

        return student_ids

    def insert_grades(self, grades_data: List[Tuple[str, str, int]],
                      student_ids: Dict[str, int]) -> None:
        """
        Вставка оценок студентов

        Args:
            grades_data: Список кортежей (имя_студента, предмет, оценка)
            student_ids: Словарь соответствия имен и ID студентов
        """
        for student_name, subject, grade in grades_data:
            student_id = student_ids.get(student_name)
            if student_id is None:
                print(f"⚠️  Предупреждение: Студент {student_name} не найден")
                continue

            self.cursor.execute(
                'INSERT INTO grades (student_id, subject, grade) VALUES (?, ?, ?)',
                (student_id, subject, grade)
            )

    def execute_query(self, query: str, params: Tuple = ()) -> List[Tuple]:
        """Выполнение SQL запроса с возвратом результатов"""
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def print_results(self, title: str, headers: List[str],
                      data: List[Tuple], format_str: str = None) -> None:
        """Красивый вывод результатов в табличном формате"""
        print(f"\n{'=' * 60}")
        print(f"{title.upper()}")
        print('-' * 60)

        # Вывод заголовков
        header_line = ' | '.join(f'{h:<20}' for h in headers)
        print(header_line)
        print('-' * 60)

        # Вывод данных
        for row in data:
            if format_str:
                print(format_str.format(*row))
            else:
                print(' | '.join(f'{str(col):<20}' for col in row))

    def close(self) -> None:
        """Закрытие соединения с базой данных"""
        self.connection.commit()
        self.connection.close()


def main() -> None:
    """Основная функция программы"""
    # Инициализация базы данных
    db = SchoolDatabase('school.db')

    try:
        # 1. Создание таблиц
        db.create_tables()

        # 2. Очистка старых данных
        db.clear_existing_data()

        # 3. Данные для вставки
        students_data = [
            ('Alice Johnson', 2005),
            ('Brian Smith', 2004),
            ('Carla Reyes', 2006),
            ('Daniel Kim', 2005),
            ('Eva Thompson', 2003),
            ('Felix Nguyen', 2007),
            ('Grace Patel', 2005),
            ('Henry Lopez', 2004),
            ('Isabella Martinez', 2006)
        ]

        grades_data = [
            ('Alice Johnson', 'Math', 88),
            ('Alice Johnson', 'English', 92),
            ('Alice Johnson', 'Science', 85),
            ('Brian Smith', 'Math', 75),
            ('Brian Smith', 'History', 83),
            ('Brian Smith', 'English', 79),
            ('Carla Reyes', 'Science', 95),
            ('Carla Reyes', 'Math', 91),
            ('Carla Reyes', 'Art', 89),
            ('Daniel Kim', 'Math', 84),
            ('Daniel Kim', 'Science', 88),
            ('Daniel Kim', 'Physical Education', 93),
            ('Eva Thompson', 'English', 90),
            ('Eva Thompson', 'History', 85),
            ('Eva Thompson', 'Math', 88),
            ('Felix Nguyen', 'Science', 72),
            ('Felix Nguyen', 'Math', 78),
            ('Felix Nguyen', 'English', 81),
            ('Grace Patel', 'Art', 94),
            ('Grace Patel', 'Science', 87),
            ('Grace Patel', 'Math', 90),
            ('Henry Lopez', 'History', 77),
            ('Henry Lopez', 'Math', 83),
            ('Henry Lopez', 'Science', 80),
            ('Isabella Martinez', 'English', 96),
            ('Isabella Martinez', 'Math', 89),
            ('Isabella Martinez', 'Art', 92)
        ]

        # 4. Вставка данных
        print("ЗАГРУЗКА ДАННЫХ В БАЗУ")
        print("-" * 40)

        student_ids = db.insert_students(students_data)
        print(f"✅ Добавлено {len(student_ids)} студентов")

        db.insert_grades(grades_data, student_ids)
        print(f"✅ Добавлено {len(grades_data)} оценок")

        # 5. ВЫПОЛНЕНИЕ ЗАПРОСОВ

        # 3.1 Все оценки Alice Johnson
        query_1 = '''
            SELECT g.subject, g.grade
            FROM students s
            JOIN grades g ON s.id = g.student_id
            WHERE s.full_name = 'Alice Johnson'
            ORDER BY g.subject
        '''
        results_1 = db.execute_query(query_1)
        db.print_results(
            "Оценки Alice Johnson",
            ["Предмет", "Оценка"],
            results_1,
            "{:<20} | {:>10}"
        )

        # 3.2 Средний балл каждого ученика
        query_2 = '''
            SELECT 
                s.full_name,
                COUNT(g.grade) as grade_count,
                ROUND(AVG(g.grade), 2) as average_grade
            FROM students s
            LEFT JOIN grades g ON s.id = g.student_id
            GROUP BY s.id, s.full_name
            ORDER BY average_grade DESC
        '''
        results_2 = db.execute_query(query_2)
        db.print_results(
            "Средний балл студентов",
            ["Студент", "Кол-во оценок", "Средний балл"],
            results_2,
            "{:<20} | {:>15} | {:>15}"
        )

        # 3.3 Студенты, родившиеся после 2004
        query_3 = '''
            SELECT full_name, birth_year
            FROM students
            WHERE birth_year > 2004
            ORDER BY birth_year
        '''
        results_3 = db.execute_query(query_3)
        db.print_results(
            "Студенты, родившиеся после 2004 года",
            ["Студент", "Год рождения"],
            results_3
        )

        # 3.4 Все предметы и их средние оценки
        query_4 = '''
            SELECT 
                subject,
                COUNT(*) as grade_count,
                ROUND(AVG(grade), 2) as average_grade
            FROM grades
            GROUP BY subject
            ORDER BY average_grade DESC
        '''
        results_4 = db.execute_query(query_4)
        db.print_results(
            "Средние оценки по предметам",
            ["Предмет", "Кол-во оценок", "Средняя оценка"],
            results_4,
            "{:<25} | {:>15} | {:>15}"
        )

        # 3.5 Топ-3 студентов с самым высоким средним баллом
        query_5 = '''
            SELECT 
                s.full_name,
                ROUND(AVG(g.grade), 2) as average_grade
            FROM students s
            JOIN grades g ON s.id = g.student_id
            GROUP BY s.id, s.full_name
            ORDER BY average_grade DESC
            LIMIT 3
        '''
        results_5 = db.execute_query(query_5)
        db.print_results(
            "Топ-3 студентов по успеваемости",
            ["Студент", "Средний балл"],
            results_5,
            "🏆 {:<20} | {:>15}"
        )

        # Студенты с оценками ниже 80
        query_6 = '''
            SELECT DISTINCT s.full_name
            FROM students s
            JOIN grades g ON s.id = g.student_id
            WHERE g.grade < 80
            ORDER BY s.full_name
        '''
        results_6 = db.execute_query(query_6)
        db.print_results(
            "Студенты с оценками ниже 80",
            ["Студент"],
            results_6
        )

        print(f"\n{'=' * 60}")
        print("ВСЕ ЗАПРОСЫ ВЫПОЛНЕНЫ УСПЕШНО")

    except sqlite3.Error as e:
        print(f"Ошибка базы данных: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    main()