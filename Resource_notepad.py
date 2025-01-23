import datetime
import json
import tkinter as tk
from tkinter import messagebox

# Файлы для параметров и логов
params_file = "parameters.json"
log_file = "log.txt"

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

# Функция для сохранения параметров в файл
def save_parameters():
    with open(params_file, "w", encoding="utf-8") as f:
        json.dump(parameters, f, ensure_ascii=False, indent=4)

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
        messagebox.showinfo("Успех", f"Параметр '{param_name}' успешно обновлён.")
        root.destroy()
    else:
        messagebox.showerror("Ошибка", f"Параметр '{param_name}' не найден.")

# Функция для сохранения размера окна изменения параметра
def save_edit_window_size(event, window):
    size = f"{window.winfo_width()}x{window.winfo_height()}"
    if parameters.get("edit_window_size") != size:
        parameters["edit_window_size"] = size
        save_parameters()

# Функция для создания окна изменения параметра
def edit_parameter(param_name):
    edit_window = tk.Toplevel()
    edit_window.title(f"Изменение параметра: {param_name}")
    
    # Устанавливаем размер окна из параметров
    initial_size = parameters.get("edit_window_size", "300x150")
    edit_window.geometry(initial_size)

    tk.Label(edit_window, text=f"Текущее значение: {parameters[param_name]}").pack(pady=5)
    tk.Label(edit_window, text="Новое значение:").pack(pady=5)

    new_value_entry = tk.Entry(edit_window)
    new_value_entry.pack(pady=5)

    tk.Button(edit_window, text="Сохранить", command=lambda: update_parameter(param_name, new_value_entry.get(), edit_window)).pack(pady=10)

    # Событие изменения размера окна
    edit_window.bind("<Configure>", lambda event: save_edit_window_size(event, edit_window))

# Функция для отображения параметров
def display_parameters():
    for widget in frame.winfo_children():
        widget.destroy()

    tk.Label(frame, text="Текущие параметры:", font=("Arial", 14)).pack(pady=10)
    for key, value in parameters.items():
        if key in {"window_size", "edit_window_size"}:
            continue  # Пропускаем параметры размеров окон
        tk.Frame(frame, height=1, bg="black", width=300).pack(pady=5)
        param_frame = tk.Frame(frame)
        param_frame.pack(pady=5)
        tk.Label(param_frame, text=f"{key}: {value}", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        tk.Button(param_frame, text="Изменить", command=lambda k=key: edit_parameter(k)).pack(side=tk.RIGHT, padx=5)

# Функция для сохранения текущего размера главного окна
def save_window_size(event):
    size = f"{root.winfo_width()}x{root.winfo_height()}"
    if parameters.get("window_size") != size:
        parameters["window_size"] = size
        save_parameters()

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
menu.add_command(label="Выйти", command=root.quit)

# Событие изменения размера главного окна
root.bind("<Configure>", save_window_size)

display_parameters()

root.mainloop()
