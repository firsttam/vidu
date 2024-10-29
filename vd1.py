import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox

# Hàm để đọc dữ liệu và tính toán thống kê
def read_data():
    global df, in_data, diemA, diemBc
    try:
        df = pd.read_csv('diemPython.csv', index_col=0, header=0)
        in_data = np.array(df)
        diemA = in_data[:, 3]  # Cột thứ 3: số sinh viên đạt điểm A
        diemBc = in_data[:, 4]  # Cột thứ 4: số sinh viên đạt điểm B+
    except FileNotFoundError:
        messagebox.showerror("Lỗi", "Không tìm thấy file diemPython.csv")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")

# Hàm để hiển thị lớp có nhiều điểm A nhất
def show_top_class():
    read_data()
    maxa = diemA.max()
    i, = np.where(diemA == maxa)
    result = f'Lớp có nhiều sinh viên đạt điểm A nhất là {in_data[i, 0][0]} với {maxa} sinh viên đạt điểm A'
    messagebox.showinfo("Thống kê", result)

# Hàm vẽ biểu đồ quạt
def draw_pie_chart():
    labels = ['Điểm A', 'Điểm B+']
    sizes = [diemA.sum(), diemBc.sum()]
    colors = ['lightcoral', 'lightskyblue']
    explode = (0.1, 0)  # Tạo hiệu ứng nổi bật phần A
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.title('Phân bố điểm A và B+')
    plt.show()

# Hàm vẽ biểu đồ đường
def draw_line_chart():
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(diemA)), diemA, 'r-', label="Điểm A")
    plt.plot(range(len(diemBc)), diemBc, 'g-', label="Điểm B+")
    plt.xlabel('Lớp')
    plt.ylabel('Số sinh viên đạt điểm')
    plt.title('Phân bố số sinh viên đạt điểm A và B+ theo lớp')
    plt.legend(loc='upper right')
    plt.show()

# Hàm vẽ biểu đồ cột
def draw_bar_chart():
    x = np.arange(len(diemA))  # Vị trí các lớp
    width = 0.35  # Độ rộng của mỗi cột
    plt.figure(figsize=(10, 6))
    plt.bar(x - width/2, diemA, width, label='Điểm A', color='red')
    plt.bar(x + width/2, diemBc, width, label='Điểm B+', color='green')
    plt.xlabel('Lớp')
    plt.ylabel('Số sinh viên đạt điểm')
    plt.title('Phân bố số sinh viên đạt điểm A và B+ theo lớp')
    plt.xticks(x, [f'Lớp {i+1}' for i in range(len(diemA))], rotation=45)
    plt.legend()
    plt.show()

# Hàm để hiển thị thống kê theo chuẩn đầu ra L1, L2
def show_statistics():
    read_data()
    result = "Thống kê điểm theo chuẩn đầu ra L1 và L2:\n"
    for outcome in ['L1', 'L2']:
        outcome_data = df[df['Outcome_Level'] == outcome]['Grade'].value_counts()
        result += f"\nChuẩn đầu ra {outcome}:\n{outcome_data.to_string()}\n"
    messagebox.showinfo("Thống kê chuẩn đầu ra", result)

# Hàm hiển thị điểm trung bình các bài kiểm tra
def show_average_scores():
    read_data()
    try:
        test_scores = df[['Test1', 'Test2', 'Final']]  # Đảm bảo các cột này có trong file CSV
        average_scores = test_scores.mean()
        result = "Điểm trung bình của các bài kiểm tra:\n" + average_scores.to_string()
        messagebox.showinfo("Điểm trung bình", result)
    except KeyError:
        messagebox.showerror("Lỗi", "Không tìm thấy cột 'Test1', 'Test2', hoặc 'Final' trong dữ liệu CSV")

# Tạo giao diện GUI
root = tk.Tk()
root.title("Chương trình báo cáo thống kê điểm K15")

# Nút bấm cho từng chức năng
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Button(frame, text="Hiển thị lớp có nhiều điểm A nhất", command=show_top_class).grid(row=0, column=0, pady=5)
ttk.Button(frame, text="Vẽ biểu đồ quạt", command=draw_pie_chart).grid(row=1, column=0, pady=5)
ttk.Button(frame, text="Vẽ biểu đồ đường", command=draw_line_chart).grid(row=2, column=0, pady=5)
ttk.Button(frame, text="Vẽ biểu đồ cột", command=draw_bar_chart).grid(row=3, column=0, pady=5)
ttk.Button(frame, text="Hiển thị thống kê L1, L2", command=show_statistics).grid(row=4, column=0, pady=5)
ttk.Button(frame, text="Hiển thị điểm trung bình bài kiểm tra", command=show_average_scores).grid(row=5, column=0, pady=5)

# Bắt đầu giao diện
root.mainloop()
