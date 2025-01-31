import datetime
import json
import tkinter as tk
from tkinter import messagebox

# Файлы для параметров, логов и заметок
params_file = "parameters.json"
log_file = "log.txt"
notes_file = "note.json"

# Загрузка параметров из файла
try:
    with open(params_file, "r", encoding="utf-8") as f:
        parameters = json.load(f)
except FileNotFoundError:
    # Если файл отсутствует, создаём начальные параметры
    parameters = {
        "Палтус": "0/30",
        "Лосось": "0/25",
        "Тунец": "0/30",
        "Прогоны": "0/10",
        "window_size": "400x400",  # Размер главного окна
        "edit_window_size": "300x150"  # Размер окна изменения параметра
    }
    with open(params_file, "w", encoding="utf-8") as f:
        json.dump(parameters, f, ensure_ascii=False, indent=4)

# Загрузка заметок из файла
try:
    with open(notes_file, "r", encoding="utf-8") as f:
        notes = json.load(f)
except FileNotFoundError:
    notes = {"notes": ""}  # Если файл отсутствует, создаём пустую заметку
    with open(notes_file, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=4)

# Сохраняем исходный порядок параметров
parameter_order = list(parameters.keys())

# Функция для сохранения параметров в файл
def save_parameters():
    with open(params_file, "w", encoding="utf-8") as f:
        json.dump(parameters, f, ensure_ascii=False, indent=4)

# Функция для сохранения заметок в файл
def save_notes():
    with open(notes_file, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=4)

# Функция для записи логов
def log_change(param, old_value, new_value):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] Изменён параметр '{param}': {old_value} -> {new_value}\n"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_entry)

# Функция для обновления параметра
def update_parameter(param_name, new_value, root):
    if param_name in parameters:
        old_value = parameters[param_name]
        parameters[param_name] = new_value
        save_parameters()  # Сохранение изменений
        log_change(param_name, old_value, new_value)
        display_parameters()  # Обновление интерфейса
        root.destroy()
    else:
        messagebox.showerror("Ошибка", f"Параметр '{param_name}' не найден.")

# Функция для изменения имени параметра
def rename_parameter(old_name, new_name, root):
    if old_name in parameters:
        if new_name in parameters:
            messagebox.showerror("Ошибка", f"Параметр с именем '{new_name}' уже существует.")
        else:
            index = parameter_order.index(old_name)
            parameter_order[index] = new_name
            parameters[new_name] = parameters.pop(old_name)
            save_parameters()
            log_change("Переименование параметра", old_name, new_name)
            display_parameters()
            root.destroy()
    else:
        messagebox.showerror("Ошибка", f"Параметр '{old_name}' не найден.")

# Функция для создания окна изменения имени параметра
def edit_parameter_name(param_name):
    rename_window = tk.Toplevel()
    rename_window.title(f"Переименование параметра: {param_name}")

    tk.Label(rename_window, text=f"Текущее имя: {param_name}").pack(pady=5)
    tk.Label(rename_window, text="Новое имя:").pack(pady=5)

    new_name_entry = tk.Entry(rename_window)
    new_name_entry.pack(pady=5)

    tk.Button(rename_window, text="Сохранить", command=lambda: rename_parameter(param_name, new_name_entry.get(), rename_window)).pack(pady=10)

# Функция для создания окна изменения значения параметра
def edit_parameter(param_name):
    edit_window = tk.Toplevel()
    edit_window.title(f"Изменение параметра: {param_name}")

    # Устанавливаем размер окна из параметров
    initial_size = parameters.get("edit_window_size", "300x150")
    edit_window.geometry(initial_size)

    tk.Label(edit_window, text=f"Текущее значение: {parameters[param_name]}\nВведите новое значение:").pack(pady=5)

    new_value_entry = tk.Entry(edit_window)
    new_value_entry.pack(pady=5)

    tk.Button(edit_window, text="Сохранить", command=lambda: update_parameter(param_name, new_value_entry.get(), edit_window)).pack(pady=10)

# Функция для отображения параметров
def display_parameters():
    for widget in frame.winfo_children():
        widget.destroy()

    tk.Label(frame, text="Ресурсы:", font=("Arial", 14)).pack(pady=10)
    for key in parameter_order:
        if key in {"window_size", "edit_window_size"}:
            continue  # Пропускаем параметры размеров окон
        value = parameters.get(key, "Удалён")
        tk.Frame(frame, height=1, bg="black", width=300).pack(pady=5)
        param_frame = tk.Frame(frame)
        param_frame.pack(pady=5)
        tk.Label(param_frame, text=f"{key}: {value}", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        tk.Button(param_frame, text="Количество", command=lambda k=key: edit_parameter(k)).pack(side=tk.LEFT, padx=5)
        tk.Button(param_frame, text="Имя", command=lambda k=key: edit_parameter_name(k)).pack(side=tk.LEFT, padx=5)

# Функция для открытия окна с заметками
def open_notes_window():
    notes_window = tk.Toplevel()
    notes_window.title("Заметки")

    # Текстовое поле для заметок
    notes_text = tk.Text(notes_window, wrap=tk.WORD, width=50, height=20)
    notes_text.pack(pady=10, padx=10)

    # Загрузка текущих заметок в текстовое поле
    notes_text.insert(tk.END, notes["notes"])

    # Функция для сохранения заметок
    def save_notes_and_close():
        notes["notes"] = notes_text.get("1.0", tk.END)
        save_notes()
        notes_window.destroy()

    # Кнопка для сохранения заметок
    tk.Button(notes_window, text="Сохранить и закрыть", command=save_notes_and_close).pack(pady=10)

# Основной интерфейс программы
root = tk.Tk()
root.title("Запоминалка ресурсов")

# Устанавливаем размер окна из параметров
initial_size = parameters.get("window_size", "400x400")
root.geometry(initial_size)

frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

menu = tk.Menu(root)
root.config(menu=menu)

menu.add_command(label="Обновить данные", command=display_parameters)
menu.add_command(label="Заметки", command=open_notes_window)
menu.add_command(label="Выйти", command=root.quit)

display_parameters()

root.mainloop()
