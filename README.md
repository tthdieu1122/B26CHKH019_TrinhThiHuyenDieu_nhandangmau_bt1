# Bài tập 1 — Pipeline hồi quy với tiền xử lý và giảm chiều PCA

Môn học: **Nhận dạng mẫu** (Pattern Recognition) — Cao học
Hình thức: làm cá nhân

## Đề bài

Trên một bộ dữ liệu có target liên tục, xây dựng chương trình dự báo, so sánh baseline với các mô hình hồi quy, và kiểm tra tác động của PCA. Mô hình được chọn dựa trên MAE/RMSE, R² và độ ổn định qua cross-validation.

## Bộ dữ liệu

**Diabetes** (built-in trong `sklearn.datasets`) — 442 mẫu, 10 đặc trưng sinh lý, target liên tục (mức độ tiến triển bệnh sau 1 năm). Không cần tải dữ liệu từ mạng ngoài.

## Cấu trúc thư mục

```
baitap1-hoiqui-pca/
├── main.py              # Script chạy toàn bộ pipeline từ đầu đến cuối
├── notebook.ipynb       # Jupyter notebook tương đương, có sẵn output/biểu đồ
├── make_report.py       # Script sinh báo cáo PDF từ kết quả trong outputs/
├── BaoCao_BaiTap1.pdf   # Báo cáo hoàn chỉnh (≥ 14 trang, tiếng Việt có dấu)
├── outputs/             # Hình ảnh (.png), bảng số liệu (.csv) và summary.json sau khi chạy
├── requirements.txt
└── README.md
```

## Cách chạy

```bash
# 1. Tạo môi trường ảo (khuyến nghị)
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Cài thư viện
pip install -r requirements.txt

# 3a. Chạy bằng script (nhanh, tái tạo toàn bộ outputs/)
python main.py

# 3b. Hoặc mở và chạy notebook
jupyter notebook notebook.ipynb   # Kernel → Run All

# 4. (Tuỳ chọn) Sinh lại báo cáo PDF sau khi có outputs/ mới
python make_report.py
```

Không cần kết nối mạng để tải dữ liệu — `load_diabetes()` có sẵn trong scikit-learn.

## Phương pháp tóm tắt

1. Tiền xử lý: `StandardScaler` trong `Pipeline` để tránh rò rỉ dữ liệu khi cross-validate.
2. Baseline: `DummyRegressor(strategy='mean')`.
3. Mô hình so sánh: Linear Regression, Ridge, Lasso, SVR (RBF), Random Forest, Gradient Boosting.
4. Đánh giá: `KFold` 5-fold cross-validation, MAE/RMSE/R² (mean ± std).
5. So sánh có/không PCA (giữ 95% phương sai).
6. Chọn mô hình tốt nhất theo RMSE + độ ổn định, đánh giá cuối trên tập test (20%, giữ lại từ đầu).

## Kết quả chính

Xem chi tiết trong `BaoCao_BaiTap1.pdf` hoặc `outputs/summary.json`. Tóm tắt: các mô hình tuyến tính có điều chuẩn (Ridge/Lasso) vượt trội baseline rõ rệt; PCA không cải thiện hiệu năng trên bộ dữ liệu 10 chiều này.

## Hướng dẫn sử dụng mã nguồn

### 1. Yêu cầu hệ thống
- Python từ 3.9 trở lên (đã kiểm thử với Python 3.12).
- Thư viện trong `requirements.txt`: numpy, pandas, matplotlib, scikit-learn (từ 1.4), jupyter, ipykernel, reportlab, pypdf.
- Không cần mạng khi chạy vì dữ liệu có sẵn trong scikit-learn.

### 2. Cài đặt môi trường
Mở terminal tại thư mục bài tập:

```bash
python -m venv venv
source venv/bin/activate          # macOS/Linux
venv\Scripts\activate             # Windows
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Chạy chương trình

| Mục đích | Lệnh | Kết quả |
|---|---|---|
| Chạy toàn bộ pipeline | `python main.py` | In tiến trình; ghi hình, CSV, `summary.json` vào `outputs/` |
| Sinh lại báo cáo PDF | `python make_report.py` | Tạo lại PDF từ `outputs/` (phải chạy `main.py` trước) |
| Chạy từng bước tương tác | `jupyter notebook` | Mở `notebook.ipynb`, chọn Kernel, Restart & Run All |

Thứ tự khuyến nghị: `main.py` rồi `make_report.py`.

### 4. Tệp kết quả trong `outputs/`

| Tệp | Nội dung |
|---|---|
| `cv_results_no_pca.csv` | MAE, RMSE, R² (trung bình, độ lệch chuẩn qua 5 fold) của 7 mô hình, không PCA |
| `cv_results_pca.csv` | Kết quả tương tự khi thêm PCA giữ 95% phương sai |
| `eda_describe.csv` | Thống kê mô tả dữ liệu |
| `01_eda.png` | Phân phối target và tương quan đặc trưng |
| `02_pca_explained_variance.png` | Phương sai tích luỹ theo số thành phần chính |
| `03_rmse_comparison.png` | So sánh RMSE có và không PCA |
| `04_test_predictions.png` | Thực tế so với dự báo, biểu đồ phần dư |
| `summary.json` | Mô hình được chọn, dùng PCA hay không, chỉ số trên tập kiểm tra |

### 5. Tham số có thể điều chỉnh

| Tham số | Vị trí | Ý nghĩa |
|---|---|---|
| `RANDOM_STATE` | đầu `main.py` | Hạt giống ngẫu nhiên, mặc định 42 |
| `test_size` | `train_test_split` | Tỉ lệ tập kiểm tra, mặc định 0.2 |
| `n_splits` | `KFold` | Số fold cross-validation, mặc định 5 |
| `models` | hàm `main()` | Thêm/bớt mô hình, đổi `alpha`, `C`, `n_estimators` |
| `0.95` | bước PCA | Ngưỡng phương sai PCA cần giữ |

### 6. Các hàm chính trong `main.py`
- `make_pipeline()`: tạo Pipeline gồm StandardScaler, PCA (tuỳ chọn) và mô hình hồi quy.
- `evaluate_cv()`: cross-validation 5 fold, trả về MAE, RMSE, R² (trung bình và độ lệch chuẩn).
- `main()`: điều phối toàn bộ quy trình, từ nạp dữ liệu đến lưu kết quả.

### 7. Lỗi thường gặp

| Hiện tượng | Cách khắc phục |
|---|---|
| `ModuleNotFoundError` | Kích hoạt lại venv và chạy `pip install -r requirements.txt` |
| PowerShell chặn lệnh activate | `Set-ExecutionPolicy -Scope Process RemoteSigned` hoặc dùng Command Prompt |
| `make_report.py` báo thiếu ảnh/CSV | Chạy `python main.py` trước |
| PDF bị ô vuông, mất dấu | Cài matplotlib (kèm font DejaVu Sans) hoặc đặt `DejaVuSans*.ttf` cạnh `make_report.py` |
| Lỗi `root_mean_squared_error` | scikit-learn cũ hơn 1.4, chạy `pip install -U scikit-learn` |
| Jupyter không thấy kernel | `python -m ipykernel install --user` |

## Tác giả

B26CHKH019_TrinhThiHuyenDieu.
