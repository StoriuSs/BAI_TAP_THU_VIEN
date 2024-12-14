import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import csv
import os
import datetime
import pandas as pd  

def add_placeholder(entry, placeholder_text):
    entry.insert(0, placeholder_text)
    entry.config(fg="grey")
    
    def on_focus_in(event):
        if entry.get() == placeholder_text:
            entry.delete(0, tk.END)
            entry.config(fg="black")
    
    def on_focus_out(event):
        if not entry.get():
            entry.insert(0, placeholder_text)
            entry.config(fg="grey")
    
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

def save_data():
    data = {
        "Employee ID": entry_id.get().strip(),
        "Name": entry_name.get().strip(),
        "Department": combobox_unit.get().strip(),
        "Position": entry_role.get().strip() or None,
        "Date of Birth": entry_dob.get().strip() if entry_dob.get().strip() != "DD/MM/YYYY" else None,
        "Gender": gender_var.get().strip(),
        "ID Number": entry_id_number.get().strip() or None,
        "Place of Issue": entry_id_place.get().strip() or None,
        "Date of Issue": entry_id_date.get().strip() if entry_id_date.get().strip() != "DD/MM/YYYY" else None,
        "Is Customer": "Yes" if customer_var.get() else "No",
        "Is Supplier": "Yes" if supplier_var.get() else "No"
    }

    if not data["Employee ID"] or not data["Name"] or not data["Department"]:
        status_label.config(text="Vui lòng điền đầy đủ các trường có dấu *", fg="red")
        return

    file_exists = os.path.isfile("employees.csv")
    with open("employees.csv", mode="a", newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

    status_label.config(text="Dữ liệu đã được lưu!", fg="green")
    clear_fields()

def clear_fields():
    entry_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    combobox_unit.set("Phân xưởng que hàn")
    entry_role.delete(0, tk.END)
    entry_dob.delete(0, tk.END)
    entry_id_number.delete(0, tk.END)
    entry_id_date.delete(0, tk.END)
    entry_id_place.delete(0, tk.END)
    gender_var.set("Nam")
    customer_var.set(0)
    supplier_var.set(0)

    add_placeholder(entry_dob, "DD/MM/YYYY")
    add_placeholder(entry_id_date, "DD/MM/YYYY")

def show_today_birthdays():
    today = datetime.datetime.now().strftime("%d/%m")
    if not os.path.isfile("employees.csv"):
        messagebox.showinfo("Thông báo", "Không tìm thấy file employees.csv!")
        return

    with open("employees.csv", mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        birthdays_today = [
            row for row in reader if row["Date of Birth"] and today in row["Date of Birth"]
        ]

    if birthdays_today:
        birthday_list = "\n".join([f"{emp['Name']} ({emp['Date of Birth']})" for emp in birthdays_today])
        messagebox.showinfo("Sinh nhật hôm nay", f"Các nhân viên có sinh nhật hôm nay:\n\n{birthday_list}")
    else:
        messagebox.showinfo("Sinh nhật hôm nay", "Không có nhân viên nào có sinh nhật hôm nay.")


def export_all_employees():
    if not os.path.isfile("employees.csv"):
        messagebox.showinfo("Thông báo", "Không tìm thấy file employees.csv!")
        return

    with open("employees.csv", mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        employees = list(reader)

    if not employees:
        messagebox.showinfo("Thông báo", "Danh sách nhân viên rỗng!")
        return

    df = pd.DataFrame(employees)

    df["Date of Birth"] = pd.to_datetime(df["Date of Birth"], format="%d/%m/%Y", errors="coerce").dt.strftime("%d/%m/%Y")

    df = df.sort_values(by="Date of Birth", ascending=True)

    output_file = "employees_sorted.xlsx"
    df.to_excel(output_file, index=False)

    messagebox.showinfo("Xuất danh sách", f"Danh sách nhân viên đã được xuất ra file {output_file}!")


root = tk.Tk()
root.title("Thông tin nhân viên")
root.geometry("800x400")

tk.Label(root, text="Thông tin nhân viên", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=4, pady=10)

customer_var = tk.IntVar()
supplier_var = tk.IntVar()
tk.Checkbutton(root, text="Là khách hàng", variable=customer_var).grid(row=1, column=0, padx=10, pady=5, sticky="w")
tk.Checkbutton(root, text="Là nhà cung cấp", variable=supplier_var).grid(row=1, column=1, padx=10, pady=5, sticky="w")

tk.Label(root, text="Mã *").grid(row=2, column=0, sticky="w", padx=10, pady=5)
entry_id = tk.Entry(root)
entry_id.grid(row=2, column=1, sticky="ew", padx=10)

tk.Label(root, text="Tên *").grid(row=2, column=2, sticky="w", padx=10, pady=5)
entry_name = tk.Entry(root)
entry_name.grid(row=2, column=3, sticky="ew", padx=10)

tk.Label(root, text="Đơn vị *").grid(row=3, column=0, sticky="w", padx=10, pady=5)
combobox_unit = ttk.Combobox(
    root, 
    values=["Phân xưởng que hàn", "Kế toán", "Sales", "Ăn không ngồi rồi ;)"], 
    state="readonly"
)
combobox_unit.grid(row=3, column=1, sticky="ew", padx=10)
combobox_unit.set("Phân xưởng que hàn")

tk.Label(root, text="Chức danh").grid(row=3, column=2, sticky="w", padx=10, pady=5)
entry_role = tk.Entry(root)
entry_role.grid(row=3, column=3, sticky="ew", padx=10)

tk.Label(root, text="Ngày sinh").grid(row=4, column=0, sticky="w", padx=10, pady=5)
entry_dob = tk.Entry(root)
entry_dob.grid(row=4, column=1, sticky="ew", padx=10)
add_placeholder(entry_dob, "DD/MM/YYYY")

tk.Label(root, text="Giới tính").grid(row=4, column=2, sticky="w", padx=10, pady=5)
gender_var = tk.StringVar(value="Nam")
tk.Radiobutton(root, text="Nam", variable=gender_var, value="Nam").grid(row=4, column=3, sticky="w", padx=10)
tk.Radiobutton(root, text="Nữ", variable=gender_var, value="Nữ").grid(row=4, column=3, sticky="e", padx=10)

tk.Label(root, text="Số CMND").grid(row=5, column=0, sticky="w", padx=10, pady=5)
entry_id_number = tk.Entry(root)
entry_id_number.grid(row=5, column=1, sticky="ew", padx=10)

tk.Label(root, text="Ngày cấp").grid(row=5, column=2, sticky="w", padx=10, pady=5)
entry_id_date = tk.Entry(root)
entry_id_date.grid(row=5, column=3, sticky="ew", padx=10)
add_placeholder(entry_id_date, "DD/MM/YYYY")

tk.Label(root, text="Nơi cấp").grid(row=6, column=0, sticky="w", padx=10, pady=5)
entry_id_place = tk.Entry(root)
entry_id_place.grid(row=6, column=1, sticky="ew", padx=10)

save_button = tk.Button(root, text="Lưu", command=save_data, bg="blue", fg="white")
save_button.grid(row=7, column=0, columnspan=2, pady=10)

today_birthdays_button = tk.Button(root, text="Sinh nhật hôm nay", command=show_today_birthdays, bg="green", fg="white")
today_birthdays_button.grid(row=7, column=2, pady=10)

export_button = tk.Button(root, text="Xuất toàn bộ danh sách", command=export_all_employees, bg="orange", fg="white")
export_button.grid(row=7, column=3, pady=10)

status_label = tk.Label(root, text="")
status_label.grid(row=8, column=0, columnspan=4, pady=5)

root.mainloop()
