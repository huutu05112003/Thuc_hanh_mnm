import sys
import numpy as np
import matplotlib.pyplot as plotter
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtCore import Qt

class SignalApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Signal Generator")
        self.setGeometry(100, 100, 400, 200)

        # Layout chính
        layout = QVBoxLayout()

        # Layout nhập tần số
        freq_layout = QHBoxLayout()
        self.freq1_input = QLineEdit(self)
        self.freq1_input.setPlaceholderText("Nhập tần số 1 (Hz)")
        self.freq2_input = QLineEdit(self)
        self.freq2_input.setPlaceholderText("Nhập tần số 2 (Hz)")

        # Thêm các widget nhập liệu vào layout
        freq_layout.addWidget(QLabel("Tần số 1: "))
        freq_layout.addWidget(self.freq1_input)
        freq_layout.addWidget(QLabel("Tần số 2: "))
        freq_layout.addWidget(self.freq2_input)

        # Nút vẽ biểu đồ
        self.plot_button = QPushButton("Vẽ biểu đồ", self)
        self.plot_button.clicked.connect(self.plot_signals)

        # Thêm layout vào giao diện chính
        layout.addLayout(freq_layout)
        layout.addWidget(self.plot_button)

        self.setLayout(layout)

    def plot_signals(self):
        try:
            # Lấy giá trị tần số từ giao diện người dùng
            signal1Frequency = float(self.freq1_input.text())
            signal2Frequency = float(self.freq2_input.text())
        except ValueError:
            # Hiển thị cảnh báo nếu giá trị nhập không hợp lệ
            print("Vui lòng nhập tần số hợp lệ!")
            return

        # Các tham số khác
        samplingFrequency = 100
        samplingInterval = 1 / samplingFrequency
        beginTime = 0
        endTime = 10
        time = np.arange(beginTime, endTime, samplingInterval)

        # Tạo hai tín hiệu sine
        amplitude1 = np.sin(2 * np.pi * signal1Frequency * time)
        amplitude2 = np.sin(2 * np.pi * signal2Frequency * time)

        # Tổng hai tín hiệu
        amplitude = amplitude1 + amplitude2

        # Vẽ biểu đồ
        figure, axis = plotter.subplots(4, 1)
        plotter.subplots_adjust(hspace=1)

        # Biểu đồ thời gian cho sóng sine
        axis[0].set_title(f'Sóng sine tần số {signal1Frequency} Hz')
        axis[0].plot(time, amplitude1)
        axis[0].set_xlabel('Thời gian')
        axis[0].set_ylabel('Biên độ')

        axis[1].set_title(f'Sóng sine tần số {signal2Frequency} Hz')
        axis[1].plot(time, amplitude2)
        axis[1].set_xlabel('Thời gian')
        axis[1].set_ylabel('Biên độ')

        # Tín hiệu kết hợp
        axis[2].set_title('Tín hiệu kết hợp (cả hai tần số)')
        axis[2].plot(time, amplitude)
        axis[2].set_xlabel('Thời gian')
        axis[2].set_ylabel('Biên độ')

        # Chuyển đổi Fourier và lọc
        fourierTransform = np.fft.fft(amplitude) / len(amplitude)
        frequencies = np.fft.fftfreq(len(amplitude), d=samplingInterval)

        # Lọc cao tần (chỉ giữ lại tần số trên tần số thứ hai)
        cutoff = signal2Frequency
        fourierTransform[np.abs(frequencies) < cutoff] = 0

        # Inverse FFT để lấy tín hiệu đã lọc
        filtered_amplitude = np.fft.ifft(fourierTransform * len(amplitude))

        # Biểu đồ Fourier sau khi lọc
        axis[3].set_title(f'Fourier Transform đã lọc (tần số cắt {cutoff} Hz)')
        axis[3].plot(frequencies[:len(frequencies)//2], np.abs(fourierTransform[:len(fourierTransform)//2]))
        axis[3].set_xlabel('Tần số (Hz)')
        axis[3].set_ylabel('Biên độ')

        plotter.show()

# Chạy ứng dụng PyQt6
app = QApplication(sys.argv)
window = SignalApp()
window.show()
sys.exit(app.exec())
