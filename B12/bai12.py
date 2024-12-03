import sys
import csv
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,
                             QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox, QDialog)


class AddStudentDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Thêm sinh viên")
        self.setGeometry(300, 300, 400, 300)

        # Các trường nhập liệu
        self.class_code_label = QLabel("Mã lớp:")
        self.class_code_input = QLineEdit(self)

        self.num_students_label = QLabel("Số SV:")
        self.num_students_input = QLineEdit(self)

        self.grade_a_plus_label = QLabel("Loại A+:")
        self.grade_a_plus_input = QLineEdit(self)

        self.grade_a_label = QLabel("Loại A:")
        self.grade_a_input = QLineEdit(self)

        self.grade_b_plus_label = QLabel("Loại B+:")
        self.grade_b_plus_input = QLineEdit(self)

        self.grade_b_label = QLabel("Loại B:")
        self.grade_b_input = QLineEdit(self)

        self.grade_c_plus_label = QLabel("Loại C+:")
        self.grade_c_plus_input = QLineEdit(self)

        self.grade_c_label = QLabel("Loại C:")
        self.grade_c_input = QLineEdit(self)

        self.grade_d_plus_label = QLabel("Loại D+:")
        self.grade_d_plus_input = QLineEdit(self)

        self.grade_d_label = QLabel("Loại D:")
        self.grade_d_input = QLineEdit(self)

        self.grade_f_label = QLabel("Loại F:")
        self.grade_f_input = QLineEdit(self)

        self.l1_label = QLabel("L1:")
        self.l1_input = QLineEdit(self)

        self.l2_label = QLabel("L2:")
        self.l2_input = QLineEdit(self)

        self.tx1_label = QLabel("TX1:")
        self.tx1_input = QLineEdit(self)

        self.tx2_label = QLabel("TX2:")
        self.tx2_input = QLineEdit(self)

        self.final_exam_label = QLabel("Cuối kỳ:")
        self.final_exam_input = QLineEdit(self)

        # Nút lưu thông tin
        self.save_button = QPushButton("Lưu", self)
        self.save_button.clicked.connect(self.save_student_info)

        # Layout
        layout = QVBoxLayout()

        input_fields = [
            (self.class_code_label, self.class_code_input),
            (self.num_students_label, self.num_students_input),
            (self.grade_a_plus_label, self.grade_a_plus_input),
            (self.grade_a_label, self.grade_a_input),
            (self.grade_b_plus_label, self.grade_b_plus_input),
            (self.grade_b_label, self.grade_b_input),
            (self.grade_c_plus_label, self.grade_c_plus_input),
            (self.grade_c_label, self.grade_c_input),
            (self.grade_d_plus_label, self.grade_d_plus_input),
            (self.grade_d_label, self.grade_d_input),
            (self.grade_f_label, self.grade_f_input),
            (self.l1_label, self.l1_input),
            (self.l2_label, self.l2_input),
            (self.tx1_label, self.tx1_input),
            (self.tx2_label, self.tx2_input),
            (self.final_exam_label, self.final_exam_input),
        ]

        for label, input_field in input_fields:
            layout.addWidget(label)
            layout.addWidget(input_field)

        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_student_info(self):
        # Kiểm tra nếu file CSV không tồn tại thì tạo mới
        file_exists = os.path.isfile('diem.csv')

        # Thêm dữ liệu mới vào CSV
        row = [
            self.class_code_input.text(),
            self.num_students_input.text(),
            self.grade_a_plus_input.text(),
            self.grade_a_input.text(),
            self.grade_b_plus_input.text(),
            self.grade_b_input.text(),
            self.grade_c_plus_input.text(),
            self.grade_c_input.text(),
            self.grade_d_plus_input.text(),
            self.grade_d_input.text(),
            self.grade_f_input.text(),
            self.l1_input.text(),
            self.l2_input.text(),
            self.tx1_input.text(),
            self.tx2_input.text(),
            self.final_exam_input.text()
        ]

        # Ghi vào file CSV
        with open('diem.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Nếu file chưa tồn tại, ghi tiêu đề cột
            if not file_exists:
                writer.writerow([
                    "Mã lớp", "Số SV", "Loại A+", "Loại A", "Loại B+", "Loại B",
                    "Loại C+", "Loại C", "Loại D+", "Loại D", "Loại F",
                    "L1", "L2", "TX1", "TX2", "Cuối kỳ"
                ])
            writer.writerow(row)

        QMessageBox.information(
            self, "Thông báo", "Đã lưu thông tin sinh viên!")
        self.accept()


class ReportApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Báo cáo học phần")
        self.setGeometry(200, 200, 800, 600)

        # Nút nhấn thêm sinh viên
        self.add_student_button = QPushButton("Thêm sinh viên", self)
        self.show_csv_button = QPushButton("Hiển thị CSV", self)
        self.analyze_button = QPushButton("Phân tích các loại điểm", self)

        # Bảng hiển thị dữ liệu
        self.table_widget = QTableWidget(self)

        # Sắp xếp layout
        layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_student_button)
        button_layout.addWidget(self.show_csv_button)
        button_layout.addWidget(self.analyze_button)
        layout.addLayout(button_layout)
        layout.addWidget(self.table_widget)

        self.setLayout(layout)

        # Kết nối sự kiện cho các nút
        self.add_student_button.clicked.connect(self.open_add_student_dialog)
        self.show_csv_button.clicked.connect(self.show_csv)
        self.analyze_button.clicked.connect(self.analyze_grades)

    def open_add_student_dialog(self):
        # Mở cửa sổ nhập sinh viên mới
        dialog = AddStudentDialog()
        if dialog.exec_():
            QMessageBox.information(
                self, "Thông báo", "Sinh viên mới đã được thêm vào CSV!")

    def show_csv(self):
        # Hiển thị dữ liệu từ CSV lên bảng
        self.table_widget.clear()
        with open('diem.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            data = list(reader)

        if len(data) > 0:
            self.table_widget.setColumnCount(len(data[0]))
            self.table_widget.setRowCount(len(data))

            for row_index, row_data in enumerate(data):
                for column_index, column_data in enumerate(row_data):
                    self.table_widget.setItem(
                        row_index, column_index, QTableWidgetItem(column_data))

    def analyze_grades(self):
        # Phân tích số lượng từng loại điểm từ CSV
        analysis = {}
        with open('diem.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                for grade in ["A+", "A", "B+", "B", "C+", "C", "D+", "D", "F"]:
                    if grade not in analysis:
                        analysis[grade] = 0
                    analysis[grade] += int(row.get(f"Loại {grade}", 0))

        # Hiển thị kết quả phân tích
        analysis_text = "\n".join(
            [f"{grade}: {count}" for grade, count in analysis.items()])
        QMessageBox.information(self, "Phân tích điểm", analysis_text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ReportApp()
    window.show()
    sys.exit(app.exec_())
