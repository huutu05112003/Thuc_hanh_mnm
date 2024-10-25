import tkinter as tk
from tkinter import messagebox
import numpy as np

def solve():
    try:
        n = int(entry_n.get())
        coefficients = []
        constants = []

        # Đọc hệ số từ Entry và tạo ma trận hệ số A
        for i in range(n):
            row = []
            for j in range(n):
                entry_value = entries[i][j].get()
                if entry_value == "":
                    raise ValueError(f"Hệ số a[{i+1}][{j+1}] bị bỏ trống.")
                row.append(float(entry_value))
            coefficients.append(row)

        # Đọc các hằng số từ Entry và tạo ma trận B
        for i in range(n):
            constant_value = constant_entries[i].get()
            if constant_value == "":
                raise ValueError(f"Hằng số b[{i+1}] bị bỏ trống.")
            constants.append(float(constant_value))

        # Giải hệ phương trình
        A = np.array(coefficients)
        B = np.array(constants)
        solutions = np.linalg.solve(A, B)

        # Hiển thị kết quả
        result_text = "Kết quả:\n"
        for i in range(n):
            result_text += f"x{i+1} = {solutions[i]:.2f}\n"
        result_label.config(text=result_text)

    except ValueError as ve:
        messagebox.showerror("Lỗi nhập liệu", f"Đã xảy ra lỗi: {ve}")
    except np.linalg.LinAlgError:
        messagebox.showerror("Lỗi giải hệ", "Hệ phương trình không có nghiệm duy nhất hoặc vô nghiệm.")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi không xác định: {e}")

def create_entries():
    global entries, constant_entries
    for widget in matrix_frame.winfo_children():
        widget.destroy()

    try:
        n = int(entry_n.get())
        if n <= 0:
            raise ValueError("Số phương trình phải là số dương.")

        entries = [[tk.Entry(matrix_frame, width=5) for _ in range(n)] for _ in range(n)]
        constant_entries = [tk.Entry(matrix_frame, width=5) for _ in range(n)]

        for i in range(n):
            for j in range(n):
                entries[i][j].grid(row=i, column=j, padx=2, pady=2)
            constant_entries[i].grid(row=i, column=n+1, padx=5, pady=2)

        tk.Label(matrix_frame, text="=").grid(row=0, column=n, rowspan=n, padx=5, pady=2, sticky="ns")
    
    except ValueError as ve:
        messagebox.showerror("Lỗi nhập liệu", f"Đã xảy ra lỗi: {ve}")

# Giao diện chính
root = tk.Tk()
root.title("Giải hệ phương trình tuyến tính n phương trình n ẩn")

# Frame nhập số phương trình và tạo ma trận
input_frame = tk.Frame(root, padx=10, pady=10)
input_frame.grid(row=0, column=0, sticky="nsew")

tk.Label(input_frame, text="Số phương trình và số ẩn (n):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_n = tk.Entry(input_frame, width=5)
entry_n.grid(row=0, column=1, padx=5, pady=5)

# Nút tạo ma trận
tk.Button(input_frame, text="Tạo ma trận", command=create_entries).grid(row=1, column=0, columnspan=2, pady=10)

# Frame chứa ma trận hệ số và hằng số
matrix_frame = tk.Frame(root, padx=10, pady=10)
matrix_frame.grid(row=1, column=0, sticky="nsew")

# Nút Giải
solve_button = tk.Button(root, text="Giải", command=solve)
solve_button.grid(row=2, column=0, pady=10)

# Frame kết quả
result_frame = tk.Frame(root, padx=10, pady=10)
result_frame.grid(row=3, column=0, sticky="nsew")

result_label = tk.Label(result_frame, text="", font=("Arial", 12), anchor="w", justify="left")
result_label.grid(row=0, column=0, sticky="w")

root.mainloop()
