import numpy as np
import tkinter as tk
from tkinter import messagebox

class MatrixOperationsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Phép toán ma trận (n x n)")

        # Nhãn hướng dẫn nhập kích thước ma trận
        self.instructions_label = tk.Label(root, text="Nhập kích thước ma trận (n):")
        self.instructions_label.grid(row=0, column=0, columnspan=2)

        # Ô nhập cho n (kích thước ma trận)
        self.n_entry = tk.Entry(root)
        self.n_entry.grid(row=0, column=2)

        # Nút tạo các ô nhập liệu cho ma trận
        self.generate_button = tk.Button(root, text="Tạo ma trận", command=self.generate_matrix_fields)
        self.generate_button.grid(row=0, column=3)

        # Nút "Reset"
        self.reset_button = tk.Button(root, text="Reset", command=self.reset_fields)
        self.reset_button.grid(row=0, column=4)

        # Nơi lưu các ô nhập liệu cho ma trận
        self.matrix1_entries = []
        self.matrix2_entries = []
        self.result_label = None
        self.label_operations = None
        self.n = 0

    def generate_matrix_fields(self):
        self.reset_fields(clear_n_entry=False)

        try:
            # Lấy kích thước ma trận n
            self.n = int(self.n_entry.get())
            if self.n <= 0:
                raise ValueError("Kích thước ma trận phải là một số nguyên dương.")

            # Tạo các ô nhập liệu cho ma trận A
            tk.Label(self.root, text="Ma trận A:").grid(row=2, column=0, columnspan=self.n)
            for i in range(self.n):
                row_entries = []
                for j in range(self.n):
                    entry = tk.Entry(self.root, width=5)
                    entry.grid(row=i + 3, column=j)
                    row_entries.append(entry)
                self.matrix1_entries.append(row_entries)

            # Tạo các ô nhập liệu cho ma trận B
            tk.Label(self.root, text="Ma trận B:").grid(row=self.n + 3, column=0, columnspan=self.n)
            for i in range(self.n):
                row_entries = []
                for j in range(self.n):
                    entry = tk.Entry(self.root, width=5)
                    entry.grid(row=i + self.n + 4, column=j)
                    row_entries.append(entry)
                self.matrix2_entries.append(row_entries)

            # Nút thực hiện các phép toán ma trận
            self.calculate_button = tk.Button(root, text="Tính toán", command=self.perform_operations)
            self.calculate_button.grid(row=self.n * 2 + 5, column=0, columnspan=6)

        except ValueError:
            messagebox.showerror("Lỗi nhập liệu", "Hãy nhập một số nguyên dương cho kích thước ma trận.")

    def perform_operations(self):
        try:
            # Lấy dữ liệu từ các ô nhập liệu và tạo ma trận A và B
            A = np.array([[float(self.matrix1_entries[i][j].get()) for j in range(self.n)] for i in range(self.n)])
            B = np.array([[float(self.matrix2_entries[i][j].get()) for j in range(self.n)] for i in range(self.n)])

            # Thực hiện các phép toán ma trận
            addition_result = A + B
            subtraction_result = A - B
            multiplication_result = np.dot(A, B)

            # Thực hiện phép chia A / B = A * B^-1 (nếu B khả nghịch)
            if np.linalg.det(B) != 0:
                division_result = np.dot(A, np.linalg.inv(B))
            else:
                division_result = None

            # Tính hạng của ma trận kết quả
            rank_A = np.linalg.matrix_rank(A)
            rank_B = np.linalg.matrix_rank(B)

            # Tính ma trận nghịch đảo nếu có
            if np.linalg.det(A) != 0:
                inverse_A = np.linalg.inv(A)
            else:
                inverse_A = None

            if np.linalg.det(B) != 0:
                inverse_B = np.linalg.inv(B)
            else:
                inverse_B = None

            # Chuẩn bị kết quả hiển thị
            result_text = f"Phép cộng (A + B):\n{addition_result}\n\n" \
                          f"Phép trừ (A - B):\n{subtraction_result}\n\n" \
                          f"Phép nhân (A * B):\n{multiplication_result}\n\n"

            if division_result is not None:
                result_text += f"Phép chia (A / B):\n{division_result}\n\n"
            else:
                result_text += "Phép chia (A / B): Không khả thi (B không khả nghịch)\n\n"

            result_text += f"Hạng của ma trận A: {rank_A}\n"
            result_text += f"Hạng của ma trận B: {rank_B}\n\n"

            if inverse_A is not None:
                result_text += f"Ma trận nghịch đảo của A:\n{inverse_A}\n\n"
            else:
                result_text += "Ma trận A không có nghịch đảo.\n\n"

            if inverse_B is not None:
                result_text += f"Ma trận nghịch đảo của B:\n{inverse_B}\n\n"
            else:
                result_text += "Ma trận B không có nghịch đảo.\n\n"

            # Hiển thị kết quả
            if self.result_label:
                self.result_label.destroy()
            self.result_label = tk.Label(self.root, text=result_text)
            self.result_label.grid(row=self.n * 2 + 6, column=0, columnspan=6)

        except ValueError:
            messagebox.showerror("Lỗi nhập liệu", "Vui lòng nhập các giá trị hợp lệ cho ma trận.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi không mong muốn: {str(e)}")

    def reset_fields(self, clear_n_entry=True):
        # Xóa các ô nhập liệu và đặt lại giao diện
        for row in self.matrix1_entries:
            for entry in row:
                entry.destroy()
        self.matrix1_entries.clear()

        for row in self.matrix2_entries:
            for entry in row:
                entry.destroy()
        self.matrix2_entries.clear()

        # Xóa kết quả nếu có
        if self.result_label:
            self.result_label.destroy()
            self.result_label = None

        # Xóa ô nhập n nếu được chỉ định
        if clear_n_entry:
            self.n_entry.delete(0, tk.END)

# Khởi tạo giao diện
if __name__ == "__main__":
    root = tk.Tk()
    app = MatrixOperationsApp(root)
    root.mainloop()
