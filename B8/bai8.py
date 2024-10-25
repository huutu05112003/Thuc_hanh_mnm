import sys
import cv2
import numpy as np
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QComboBox, QSlider
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt

class ImageFilterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ứng dụng Lọc và Làm Mịn Ảnh")
        self.resize(1200, 600)  # Điều chỉnh kích thước cửa sổ lớn hơn
        self.image = None  # Ảnh gốc
        self.smooth_value = 5  # Giá trị mặc định cho độ mịn (kernel size)

        # Layout chính
        self.main_layout = QVBoxLayout()

        # Tạo layout ngang cho ảnh gốc và ảnh đã qua xử lý
        self.image_layout = QHBoxLayout()

        # Nhãn hiển thị ảnh gốc
        self.original_label = QLabel("Ảnh gốc")
        self.original_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.original_label.setFixedSize(600, 400)  # Điều chỉnh kích thước nhãn lớn hơn
        self.image_layout.addWidget(self.original_label)
        
        # Nhãn hiển thị ảnh sau khi lọc
        self.filtered_label = QLabel("Ảnh đã qua xử lý")
        self.filtered_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.filtered_label.setFixedSize(600, 400)  # Điều chỉnh kích thước nhãn lớn hơn
        self.image_layout.addWidget(self.filtered_label)

        # Thêm layout ảnh vào layout chính
        self.main_layout.addLayout(self.image_layout)
        
        # Nút chọn ảnh
        self.btn_select_image = QPushButton("Chọn ảnh")
        self.btn_select_image.clicked.connect(self.load_image)
        self.main_layout.addWidget(self.btn_select_image)
        
        # ComboBox chọn bộ lọc
        self.filter_box = QComboBox(self)
        self.filter_box.addItem("Lọc Trung Bình")
        self.filter_box.addItem("Lọc Gaussian")
        self.filter_box.addItem("Lọc Median")
        self.filter_box.addItem("Lọc Bilateral")
        self.filter_box.currentTextChanged.connect(self.apply_filter)
        self.main_layout.addWidget(self.filter_box)

        # Thêm thanh trượt để điều chỉnh độ mịn của ảnh
        self.smooth_slider = QSlider(Qt.Orientation.Horizontal)
        self.smooth_slider.setMinimum(1)  # Đặt giá trị nhỏ nhất cho kernel size
        self.smooth_slider.setMaximum(15)  # Đặt giá trị lớn nhất cho kernel size
        self.smooth_slider.setValue(self.smooth_value)  # Giá trị mặc định
        self.smooth_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.smooth_slider.setTickInterval(2)
        self.smooth_slider.valueChanged.connect(self.update_smooth_value)
        self.main_layout.addWidget(self.smooth_slider)

        # Đặt layout chính cho cửa sổ
        self.setLayout(self.main_layout)
    
    def load_image(self):
        # Chọn file ảnh từ máy tính
        image_path, _ = QFileDialog.getOpenFileName(self, "Chọn hình ảnh", "", "Image Files (*.png *.jpg *.bmp)")
        if image_path:
            self.image = cv2.imread(image_path)
            self.display_image(self.image, self.original_label)
            self.apply_filter()  # Áp dụng bộ lọc mặc định
    
    def display_image(self, img, label):
        # Chuyển đổi ảnh từ OpenCV (BGR) sang QImage (RGB)
        height, width, channel = img.shape
        bytes_per_line = 3 * width
        qimg = QImage(img.data, width, height, bytes_per_line, QImage.Format.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(qimg)
        label.setPixmap(pixmap.scaled(label.width(), label.height(), Qt.AspectRatioMode.KeepAspectRatio))  # Điều chỉnh kích thước ảnh để vừa với nhãn

    def update_smooth_value(self):
        # Cập nhật giá trị độ mịn khi thanh trượt thay đổi
        self.smooth_value = self.smooth_slider.value()
        self.apply_filter()  # Áp dụng lại bộ lọc với giá trị độ mịn mới

    def apply_filter(self):
        if self.image is None:
            return
        
        # Lấy bộ lọc từ ComboBox
        selected_filter = self.filter_box.currentText()
        
        # Áp dụng các bộ lọc khác nhau dựa trên lựa chọn
        if selected_filter == "Lọc Trung Bình":
            filtered_image = cv2.blur(self.image, (self.smooth_value, self.smooth_value))
        elif selected_filter == "Lọc Gaussian":
            filtered_image = cv2.GaussianBlur(self.image, (self.smooth_value * 2 + 1, self.smooth_value * 2 + 1), 0)
        elif selected_filter == "Lọc Median":
            filtered_image = cv2.medianBlur(self.image, self.smooth_value * 2 + 1)
        elif selected_filter == "Lọc Bilateral":
            filtered_image = cv2.bilateralFilter(self.image, self.smooth_value * 2 + 1, 75, 75)
        
        # Hiển thị ảnh đã qua xử lý
        self.display_image(filtered_image, self.filtered_label)

# Khởi chạy ứng dụng
app = QApplication(sys.argv)
window = ImageFilterApp()
window.show()
sys.exit(app.exec())
