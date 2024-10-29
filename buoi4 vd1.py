import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import tkinter as tk
from tkinter import ttk, messagebox


# Hàm kiểm tra tính hợp lệ của hàm nhập vào
def is_valid_function(func_input):
    try:
        sp.sympify(func_input)
        return True
    except (sp.SympifyError, SyntaxError):
        return False


# Hàm tính toán
def calculate():
    try:
        numerator_input = numerator_entry.get()
        denominator_input = denominator_entry.get()
        x = sp.symbols('x')

        # Kiểm tra tính hợp lệ của tử số và mẫu số
        if not is_valid_function(numerator_input):
            messagebox.showerror("Lỗi", "Tử số không hợp lệ. Vui lòng kiểm tra lại.")
            return

        if not is_valid_function(denominator_input):
            messagebox.showerror("Lỗi", "Mẫu số không hợp lệ. Vui lòng kiểm tra lại.")
            return

        numerator = sp.sympify(numerator_input)
        denominator = sp.sympify(denominator_input)

        # Kiểm tra mẫu số
        if denominator == 0:
            messagebox.showerror("Lỗi", "Mẫu số bằng 0. Không thể thực hiện phép toán.")
            return

        limit_input = limit_entry.get()
        x_value = sp.symbols('x')

        if operation.get() == "Giới hạn":
            if not limit_input:
                messagebox.showerror("Lỗi", "Vui lòng nhập giá trị giới hạn.")
                return

            try:
                limit_value = sp.sympify(limit_input)

                # Kiểm tra mẫu số có phải là 0 hay không
                denominator_value = denominator.subs(x_value, limit_value)
                if denominator_value == 0:
                    messagebox.showerror("Lỗi", "Mẫu số tiến về 0 tại giới hạn. Không thể tính giới hạn.")
                    return

                result = sp.limit(numerator / denominator, x, limit_value)
                result_label.config(text=f"Giới hạn tại {limit_value}: {result}")

            except (sp.SympifyError, ValueError):
                messagebox.showerror("Lỗi", "Giá trị giới hạn không hợp lệ.")

        else:
            # Lấy giá trị từ các lựa chọn
            if operation.get() == "Đạo hàm":
                result = sp.diff(numerator / denominator, x)
                result_label.config(text=f"Đạo hàm: {result}")
                plot_function(numerator / denominator, result)
            elif operation.get() == "Tích phân":
                result = sp.integrate(numerator / denominator, x)
                result_label.config(text=f"Tích phân: {result}")
                plot_function(numerator / denominator, result)
            elif operation.get() == "Vẽ đồ thị":
                plot_function(numerator / denominator)
            else:
                messagebox.showerror("Lỗi", "Vui lòng chọn chức năng!")

    except Exception as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")


# Hàm vẽ đồ thị
def plot_function(func, derivative=None):
    x_vals = np.linspace(-10, 10, 400)
    func_lambdified = sp.lambdify(sp.symbols('x'), func, "numpy")

    plt.figure(figsize=(10, 6))
    plt.plot(x_vals, func_lambdified(x_vals), label=str(func), color='blue')

    if derivative is not None:
        derivative_lambdified = sp.lambdify(sp.symbols('x'), derivative, "numpy")
        plt.plot(x_vals, derivative_lambdified(x_vals), label=f"Đạo hàm: {derivative}", color='red')

    plt.axhline(0, color='black', linewidth=0.5, ls='--')
    plt.axvline(0, color='black', linewidth=0.5, ls='--')
    plt.title('Đồ thị hàm số và đạo hàm')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid()
    plt.legend()
    plt.show()


# Tạo giao diện GUI
root = tk.Tk()
root.title("Ứng dụng Giải tích")

# Nhập hàm số tử số
ttk.Label(root, text="Nhập tử số (vd: x**2 + 3*x + 2):").grid(column=0, row=0, padx=10, pady=10)
numerator_entry = ttk.Entry(root, width=40)
numerator_entry.grid(column=1, row=0, padx=10, pady=10)

# Nhập hàm số mẫu số
ttk.Label(root, text="Nhập mẫu số (vd: x + 1):").grid(column=0, row=1, padx=10, pady=10)
denominator_entry = ttk.Entry(root, width=40)
denominator_entry.grid(column=1, row=1, padx=10, pady=10)

# Lựa chọn chức năng
operation = tk.StringVar(value="Tính toán")
ttk.Label(root, text="Chọn chức năng:").grid(column=0, row=2, padx=10, pady=10)
ttk.Combobox(root, textvariable=operation, values=["Đạo hàm", "Tích phân", "Giới hạn", "Vẽ đồ thị"],
             state="readonly").grid(column=1, row=2, padx=10, pady=10)

# Nhập giá trị giới hạn
limit_entry = ttk.Entry(root, width=20)
limit_entry.grid(column=1, row=3, padx=10, pady=10)
ttk.Label(root, text="Nhập giới hạn (nếu chọn Giới hạn):").grid(column=0, row=3, padx=10, pady=10)

# Nút tính toán
calculate_button = ttk.Button(root, text="Tính toán", command=calculate)
calculate_button.grid(column=0, row=4, columnspan=2, pady=10)

# Kết quả
result_label = ttk.Label(root, text="Kết quả: ")
result_label.grid(column=0, row=5, columnspan=2, pady=5)

# Bắt đầu giao diện
root.mainloop()
