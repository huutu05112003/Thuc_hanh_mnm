# Import các thư viện cần thiết
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Tạo DataFrame từ dữ liệu đã cho
df = pd.read_csv("Student_Performance.csv")

# Chia tập dữ liệu thành đầu vào (X) và nhãn (y)
X = df.drop("Performance Index", axis=1)  # Các đặc trưng
y = df["Performance Index"]  # Nhãn (chỉ số hiệu quả học tập)

# Chia dữ liệu thành tập huấn luyện và tập kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Khởi tạo mô hình hồi quy tuyến tính
model = LinearRegression()

# Huấn luyện mô hình với dữ liệu huấn luyện
model.fit(X_train, y_train)

# Dự đoán trên tập kiểm tra
y_pred = model.predict(X_test)

# Đánh giá mô hình
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Mean Squared Error (MSE):", mse)
print("R-squared (R²):", r2)

# Hiển thị kết quả dự đoán và giá trị thực
df_results = pd.DataFrame({"Thực tế": y_test, "Dự đoán": y_pred})
print(df_results)
