import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont

# Файл для хранения данных
DATA_FILE = "movies.json"

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 Movie Library - Личная кинотека")
        self.root.geometry("900x600")
        self.root.resizable(True, True)

        # Список фильмов
        self.movies = []
        self.load_data()

        # Создание интерфейса
        self.create_input_frame()
        self.create_table_frame()
        self.create_filter_frame()

        # Обновление таблицы
        self.refresh_table()

        # Сохранение при закрытии
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    # ==================== ВВОД ДАННЫХ ====================
    def create_input_frame(self):
        """Форма для ввода нового фильма"""
        input_frame = tk.LabelFrame(self.root, text="➕ Добавить новый фильм", font=("Arial", 12, "bold"), padx=10, pady=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        # Поле: Название
        tk.Label(input_frame, text="Название:", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.title_entry = tk.Entry(input_frame, width=30, font=("Arial", 10))
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        # Поле: Жанр
        tk.Label(input_frame, text="Жанр:", font=("Arial", 10)).grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.genre_entry = tk.Entry(input_frame, width=20, font=("Arial", 10))
        self.genre_entry.grid(row=0, column=3, padx=5, pady=5)

        # Поле: Год
        tk.Label(input_frame, text="Год выпуска:", font=("Arial", 10)).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.year_entry = tk.Entry(input_frame, width=10, font=("Arial", 10))
        self.year_entry.grid(row=1, column=1, padx=5, pady=5)

        # Поле: Рейтинг
        tk.Label(input_frame, text="Рейтинг (0-10):", font=("Arial", 10)).grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        self.rating_entry = tk.Entry(input_frame, width=10, font=("Arial", 10))
        self.rating_entry.grid(row=1, column=3, padx=5, pady=5)

        # Кнопка добавления
        self.add_btn = tk.Button(input_frame, text="📀 Добавить фильм", command=self.add_movie,
                                 bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), padx=10)
        self.add_btn.grid(row=2, column=0, columnspan=4, pady=10)

    # ==================== ТАБЛИЦА ====================
    def create_table_frame(self):
        """Таблица для отображения фильмов"""
        table_frame = tk.LabelFrame(self.root, text="📋 Список фильмов", font=("Arial", 12, "bold"), padx=10, pady=10)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Создание Treeview
        columns = ("ID", "Название", "Жанр", "Год", "Рейтинг")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

        # Определение заголовков
        self.tree.heading("ID", text="ID")
        self.tree.heading("Название", text="Название")
        self.tree.heading("Жанр", text="Жанр")
        self.tree.heading("Год", text="Год")
        self.tree.heading("Рейтинг", text="Рейтинг")

        # Настройка ширины колонок
        self.tree.column("ID", width=40, anchor=tk.CENTER)
        self.tree.column("Название", width=250)
        self.tree.column("Жанр", width=150)
        self.tree.column("Год", width=80, anchor=tk.CENTER)
        self.tree.column("Рейтинг", width=80, anchor=tk.CENTER)

        # Полоса прокрутки
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Кнопка удаления
        delete_btn = tk.Button(table_frame, text="🗑 Удалить выбранный фильм", command=self.delete_movie,
                               bg="#f44336", fg="white", font=("Arial", 10), padx=10)
        delete_btn.pack(pady=5)

    # ==================== ФИЛЬТРАЦИЯ ====================
    def create_filter_frame(self):
        """Фильтрация по жанру и году"""
        filter_frame = tk.LabelFrame(self.root, text="🔍 Фильтрация", font=("Arial", 12, "bold"), padx=10, pady=10)
        filter_frame.pack(fill=tk.X, padx=10, pady=5)

        # Фильтр по жанру
        tk.Label(filter_frame, text="Фильтр по жанру:", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5)
        self.filter_genre_var = tk.StringVar()
        self.filter_genre_combo = ttk.Combobox(filter_frame, textvariable=self.filter_genre_var, width=20)
        self.filter_genre_combo.grid(row=0, column=1, padx=5, pady=5)
        self.filter_genre_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_table())

        # Фильтр по году
        tk.Label(filter_frame, text="Фильтр по году:", font=("Arial", 10)).grid(row=0, column=2, padx=5, pady=5)
        self.filter_year_var = tk.StringVar()
        self.filter_year_combo = ttk.Combobox(filter_frame, textvariable=self.filter_year_var, width=10)
        self.filter_year_combo.grid(row=0, column=3, padx=5, pady=5)
        self.filter_year_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_table())

        # Кнопка сброса фильтров
        reset_btn = tk.Button(filter_frame, text="🔄 Сбросить фильтры", command=self.reset_filters,
                              bg="#FF9800", fg="white", font=("Arial", 10), padx=10)
        reset_btn.grid(row=0, column=4, padx=10, pady=5)

        # Статусная строка
        self.status_var = tk.StringVar()
        self.status_var.set("Готово")
        status_label = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_label.pack(side=tk.BOTTOM, fill=tk.X)

    # ==================== ЛОГИКА ====================
    def add_movie(self):
        """Добавление фильма с проверкой данных"""
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        year_str = self.year_entry.get().strip()
        rating_str = self.rating_entry.get().strip()

        # Проверка: все поля заполнены
        if not all([title, genre, year_str, rating_str]):
            messagebox.showwarning("Ошибка ввода", "Заполните все поля!")
            return

        # Проверка года
        try:
            year = int(year_str)
            if year < 1888 or year > 2026:  # Первый фильм - 1888 год
                raise ValueError
        except ValueError:
            messagebox.showwarning("Ошибка ввода", "Год должен быть числом от 1888 до 2026!")
            return

        # Проверка рейтинга
        try:
            rating = float(rating_str)
            if rating < 0 or rating > 10:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Ошибка ввода", "Рейтинг должен быть числом от 0 до 10!")
            return

        # Создание ID (автоинкремент)
        new_id = max([m["id"] for m in self.movies] + [0]) + 1

        # Добавление фильма
        movie = {
            "id": new_id,
            "title": title,
            "genre": genre,
            "year": year,
            "rating": rating
        }
        self.movies.append(movie)
        self.save_data()

        # Очистка полей
        self.title_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)

        # Обновление фильтров и таблицы
        self.update_filter_options()
        self.refresh_table()
        self.status_var.set(f"✅ Добавлен фильм: {title}")

    def delete_movie(self):
        """Удаление выбранного фильма"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Информация", "Выберите фильм для удаления!")
            return

        # Получение ID фильма
        item = self.tree.item(selected[0])
        movie_id = item["values"][0]

        # Удаление
        self.movies = [m for m in self.movies if m["id"] != movie_id]
        self.save_data()
        self.update_filter_options()
        self.refresh_table()
        self.status_var.set("🗑 Фильм удалён")

    def refresh_table(self):
        """Обновление таблицы с учётом фильтров"""
        # Очистка таблицы
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Фильтрация данных
        filtered_movies = self.movies.copy()

        # Фильтр по жанру
        genre_filter = self.filter_genre_var.get()
        if genre_filter and genre_filter != "Все":
            filtered_movies = [m for m in filtered_movies if m["genre"] == genre_filter]

        # Фильтр по году
        year_filter = self.filter_year_var.get()
        if year_filter and year_filter != "Все":
            try:
                year_filter_int = int(year_filter)
                filtered_movies = [m for m in filtered_movies if m["year"] == year_filter_int]
            except:
                pass

        # Вывод в таблицу
        for movie in filtered_movies:
            self.tree.insert("", tk.END, values=(
                movie["id"],
                movie["title"],
                movie["genre"],
                movie["year"],
                f"{movie['rating']:.1f}"
            ))

        self.status_var.set(f"📊 Показано: {len(filtered_movies)} из {len(self.movies)} фильмов")

    def update_filter_options(self):
        """Обновление выпадающих списков фильтров"""
        # Жанры
        genres = sorted(set(m["genre"] for m in self.movies))
        self.filter_genre_combo["values"] = ["Все"] + genres
        if not self.filter_genre_var.get() or self.filter_genre_var.get() not in genres:
            self.filter_genre_var.set("Все")

        # Годы
        years = sorted(set(m["year"] for m in self.movies))
        self.filter_year_combo["values"] = ["Все"] + [str(y) for y in years]
        if not self.filter_year_var.get() or (self.filter_year_var.get() != "Все" and int(self.filter_year_var.get()) not in years):
            self.filter_year_var.set("Все")

    def reset_filters(self):
        """Сброс всех фильтров"""
        self.filter_genre_var.set("Все")
        self.filter_year_var.set("Все")
        self.refresh_table()
        self.status_var.set("🔄 Фильтры сброшены")

    # ==================== РАБОТА С JSON ====================
    def load_data(self):
        """Загрузка данных из JSON файла"""
        if not os.path.exists(DATA_FILE):
            self.movies = []
            return
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                self.movies = json.load(f)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные:\n{e}")
            self.movies = []

    def save_data(self):
        """Сохранение данных в JSON файл"""
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.movies, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные:\n{e}")

    def on_closing(self):
        """Действие при закрытии приложения"""
        self.save_data()
        self.root.destroy()


# ==================== ЗАПУСК ====================
if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()
