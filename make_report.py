# -*- coding: utf-8 -*-
"""Tao bao cao PDF (tieng Viet co dau, toi thieu 10 trang) cho Bai tap 1."""
import json
import os

import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak,
    ListFlowable, ListItem,
)

BASE = os.path.dirname(__file__)
OUT = os.path.join(BASE, "outputs")
REPORT_PATH = os.path.join(BASE, "BaoCao_BaiTap1.pdf")

# --- Dang ky font Unicode ho tro tieng Viet co dau ---
# Uu tien font DejaVu Sans di kem san trong goi matplotlib (co san tren moi he dieu hanh
# vi matplotlib da la mot dependency bat buoc), sau do moi thu cac duong dan he thong pho bien.
def _find_vn_font():
    candidates = []
    try:
        import matplotlib
        mpl_font_dir = os.path.join(os.path.dirname(matplotlib.__file__), "mpl-data", "fonts", "ttf")
        candidates.append(mpl_font_dir)
    except Exception:
        pass
    candidates += [
        "/usr/share/fonts/truetype/dejavu",                       # Debian/Ubuntu
        "/usr/share/fonts/dejavu",                                 # Fedora/RHEL
        "/usr/local/share/fonts",
        "C:/Windows/Fonts",                                        # Windows (co the dung Arial/Tahoma thay the)
    ]
    for d in candidates:
        reg = os.path.join(d, "DejaVuSans.ttf")
        bold = os.path.join(d, "DejaVuSans-Bold.ttf")
        italic = os.path.join(d, "DejaVuSans-Oblique.ttf")
        if os.path.exists(reg) and os.path.exists(bold):
            return reg, bold, italic if os.path.exists(italic) else reg
    raise FileNotFoundError(
        "Khong tim thay font DejaVu Sans. Hay cai dat matplotlib (pip install matplotlib) "
        "hoac dat DejaVuSans.ttf / DejaVuSans-Bold.ttf vao cung thu muc voi script nay."
    )


FONT_REGULAR, FONT_BOLD, FONT_ITALIC = _find_vn_font()
pdfmetrics.registerFont(TTFont("VN", FONT_REGULAR))
pdfmetrics.registerFont(TTFont("VN-Bold", FONT_BOLD))
pdfmetrics.registerFont(TTFont("VN-Italic", FONT_ITALIC))

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CoverTitle", fontName="VN-Bold", fontSize=22, leading=28, alignment=TA_CENTER, spaceAfter=10))
styles.add(ParagraphStyle(name="CoverSub", fontName="VN", fontSize=13, leading=18, alignment=TA_CENTER, textColor=colors.HexColor("#444444"), spaceAfter=6))
styles.add(ParagraphStyle(name="CoverInfo", fontName="VN", fontSize=11, leading=16, alignment=TA_CENTER, spaceAfter=4))
styles.add(ParagraphStyle(name="H1", fontName="VN-Bold", fontSize=14, leading=18, spaceBefore=16, spaceAfter=8, textColor=colors.HexColor("#1a2734")))
styles.add(ParagraphStyle(name="H2", fontName="VN-Bold", fontSize=11.5, leading=15, spaceBefore=10, spaceAfter=6, textColor=colors.HexColor("#1a2734")))
styles.add(ParagraphStyle(name="BodyVN", fontName="VN", fontSize=10.3, leading=15, alignment=TA_JUSTIFY, spaceAfter=8))
styles.add(ParagraphStyle(name="Caption", fontName="VN-Italic", fontSize=8.7, leading=11, alignment=TA_CENTER, textColor=colors.grey, spaceAfter=12))
styles.add(ParagraphStyle(name="TOC", fontName="VN", fontSize=10.5, leading=20, alignment=TA_LEFT))
styles.add(ParagraphStyle(name="Mono", fontName="VN", fontSize=9, leading=15, backColor=colors.HexColor("#f5f5f5"), borderPadding=8, spaceAfter=10))
styles.add(ParagraphStyle(name="Cell", fontName="VN", fontSize=8.8, leading=12, alignment=TA_LEFT))
styles.add(ParagraphStyle(name="Cmd", fontName="Courier", fontSize=9, leading=14, backColor=colors.HexColor("#f5f5f5"), borderPadding=8, spaceAfter=10))


def P(text, style="BodyVN"):
    return Paragraph(text, styles[style])

def bullets(items):
    return ListFlowable(
        [ListItem(P(it), bulletColor=colors.HexColor("#1a2734")) for it in items],
        bulletType="bullet", start="•", leftIndent=14, spaceBefore=2, spaceAfter=10,
    )

with open(os.path.join(OUT, "summary.json"), encoding="utf-8") as f:
    summary = json.load(f)

story = []

# ===================== TRANG BIA =====================
story.append(Spacer(1, 4 * cm))
story.append(P("BÁO CÁO BÀI TẬP 1", "CoverTitle"))
story.append(P("XÂY DỰNG PIPELINE HỒI QUY VỚI TIỀN XỬ LÝ", "CoverTitle"))
story.append(P("VÀ GIẢM CHIỀU PCA", "CoverTitle"))
story.append(Spacer(1, 1 * cm))
story.append(P("Môn học: Nhận dạng mẫu (Pattern Recognition)", "CoverSub"))
story.append(P("Chương trình đào tạo Thạc sĩ", "CoverSub"))
story.append(Spacer(1, 3 * cm))
story.append(P("Học viên thực hiện: ......................................................", "CoverInfo"))
story.append(P("Mã học viên: ......................................................", "CoverInfo"))
story.append(P("Lớp / Khoá: ......................................................", "CoverInfo"))
story.append(P("Giảng viên hướng dẫn: ......................................................", "CoverInfo"))
story.append(Spacer(1, 2 * cm))
story.append(P("Hình thức thực hiện: Cá nhân", "CoverInfo"))
story.append(P("Bộ dữ liệu sử dụng: Diabetes (scikit-learn)", "CoverInfo"))
story.append(PageBreak())

# ===================== MUC LUC =====================
story.append(P("MỤC LỤC", "H1"))
toc_items = [
    "1. Đặt vấn đề",
    "2. Tổng quan lý thuyết",
    "   2.1. Hồi quy tuyến tính và các biến thể có điều chuẩn",
    "   2.2. Các mô hình phi tuyến dùng để so sánh",
    "   2.3. Phân tích thành phần chính (PCA)",
    "3. Mô tả và khảo sát bộ dữ liệu",
    "4. Phương pháp thực nghiệm",
    "   4.1. Quy trình tiền xử lý và pipeline",
    "   4.2. Chiến lược đánh giá bằng Cross-Validation",
    "   4.3. Thiết lập baseline",
    "5. Kết quả thực nghiệm",
    "   5.1. Kết quả Cross-Validation không dùng PCA",
    "   5.2. Khảo sát và tác động của PCA",
    "   5.3. Lựa chọn mô hình cuối cùng",
    "   5.4. Đánh giá trên tập kiểm tra (test set)",
    "6. Thảo luận và phân tích sâu",
    "7. Hạn chế và hướng phát triển",
    "8. Kết luận",
    "Tài liệu tham khảo",
    "Phụ lục A: Mô tả chi tiết các đặc trưng đầu vào",
    "Phụ lục B: Siêu tham số của các mô hình",
    "Phụ lục C: Quy trình tái lập kết quả",
    "Phụ lục D: Cấu trúc mã nguồn",
    "Phụ lục E: Hướng dẫn sử dụng mã nguồn",
]
story.append(ListFlowable(
    [ListItem(Paragraph(t, styles["TOC"]), leftIndent=10, spaceAfter=2) for t in toc_items],
    bulletType="bullet", start="",
))
story.append(PageBreak())

# ===================== 1. DAT VAN DE =====================
story.append(P("1. Đặt vấn đề", "H1"))
story.append(P(
    "Bài toán hồi quy (regression) là một trong hai nhóm bài toán học có giám sát cơ bản nhất "
    "trong lĩnh vực nhận dạng mẫu và học máy, bên cạnh bài toán phân loại (classification). Mục "
    "tiêu của hồi quy là xây dựng một hàm ánh xạ từ không gian đặc trưng đầu vào sang một biến "
    "mục tiêu liên tục, sao cho sai số dự báo trên dữ liệu chưa từng thấy là nhỏ nhất có thể. Trong "
    "thực tế, chất lượng của một mô hình hồi quy không chỉ phụ thuộc vào thuật toán học được lựa "
    "chọn, mà còn phụ thuộc rất nhiều vào bước tiền xử lý dữ liệu, bao gồm chuẩn hoá đặc trưng, xử "
    "lý dữ liệu thiếu, và các kỹ thuật giảm chiều dữ liệu như phân tích thành phần chính (Principal "
    "Component Analysis — PCA).", "BodyVN"))
story.append(P(
    "Báo cáo này trình bày quá trình xây dựng một pipeline hồi quy hoàn chỉnh trên bộ dữ liệu "
    "Diabetes, bao gồm các bước: khảo sát dữ liệu ban đầu (EDA), tiền xử lý bằng chuẩn hoá đặc "
    "trưng, huấn luyện và so sánh nhiều mô hình hồi quy khác nhau với một mô hình cơ sở (baseline), "
    "đánh giá độ ổn định của các mô hình bằng phương pháp kiểm định chéo (cross-validation), và "
    "cuối cùng là khảo sát cụ thể tác động của PCA đến chất lượng dự báo. Mục tiêu cuối cùng là lựa "
    "chọn được một mô hình phù hợp nhất dựa trên các tiêu chí định lượng khách quan, đồng thời rút "
    "ra những nhận định có cơ sở khoa học về vai trò của giảm chiều dữ liệu trong bài toán hồi quy "
    "cụ thể này.", "BodyVN"))
story.append(P(
    "Các câu hỏi nghiên cứu chính mà báo cáo hướng đến trả lời bao gồm: (i) Mức độ cải thiện của "
    "các mô hình hồi quy so với baseline là bao nhiêu? (ii) Mô hình tuyến tính có điều chuẩn hay mô "
    "hình phi tuyến phức tạp hơn phù hợp hơn với bộ dữ liệu này? (iii) Việc áp dụng PCA trước khi "
    "huấn luyện mô hình có cải thiện được chất lượng dự báo hay không, và tại sao?", "BodyVN"))

# ===================== 2. TONG QUAN LY THUYET =====================
story.append(P("2. Tổng quan lý thuyết", "H1"))

story.append(P("2.1. Hồi quy tuyến tính và các biến thể có điều chuẩn", "H2"))
story.append(P(
    "Hồi quy tuyến tính (Linear Regression) tìm một siêu phẳng y = Xw + b sao cho tổng bình "
    "phương sai số giữa giá trị dự báo và giá trị thực tế trên tập huấn luyện là nhỏ nhất "
    "(phương pháp bình phương tối thiểu — Ordinary Least Squares). Nhược điểm của hồi quy tuyến "
    "tính thông thường là dễ bị overfitting khi số chiều đặc trưng lớn hoặc khi các đặc trưng có "
    "tương quan mạnh với nhau (đa cộng tuyến). Để khắc phục, hai kỹ thuật điều chuẩn (regularization) "
    "phổ biến được sử dụng:", "BodyVN"))
story.append(bullets([
    "<b>Ridge Regression (điều chuẩn L2):</b> thêm vào hàm mất mát một số hạng phạt tỉ lệ với "
    "tổng bình phương các trọng số (λ·‖w‖²), giúp co các trọng số về gần 0 mà không triệt tiêu "
    "hoàn toàn, làm giảm phương sai của mô hình.",
    "<b>Lasso Regression (điều chuẩn L1):</b> thêm số hạng phạt tỉ lệ với tổng trị tuyệt đối các "
    "trọng số (λ·‖w‖₁), có xu hướng đưa một số trọng số về đúng 0, qua đó thực hiện đồng thời việc "
    "chọn đặc trưng (feature selection).",
]))

story.append(P("2.2. Các mô hình phi tuyến dùng để so sánh", "H2"))
story.append(P(
    "Bên cạnh các mô hình tuyến tính, báo cáo còn thử nghiệm ba mô hình phi tuyến phổ biến: "
    "Support Vector Regression (SVR) với kernel RBF, cho phép học các quan hệ phi tuyến thông qua "
    "phép biến đổi ngầm định vào không gian đặc trưng có số chiều cao hơn; Random Forest, một "
    "phương pháp tổng hợp (ensemble) dựa trên nhiều cây quyết định huấn luyện trên các mẫu con "
    "ngẫu nhiên (bagging); và Gradient Boosting, một phương pháp ensemble khác xây dựng tuần tự "
    "các cây quyết định yếu, mỗi cây sau được huấn luyện để sửa lỗi của tổ hợp các cây trước đó "
    "(boosting). Các mô hình phi tuyến này thường có khả năng biểu diễn tốt hơn nhưng cũng có nguy "
    "cơ overfitting cao hơn, đặc biệt với các bộ dữ liệu có số lượng mẫu nhỏ.", "BodyVN"))

story.append(P("2.3. Phân tích thành phần chính (PCA)", "H2"))
story.append(P(
    "PCA là một kỹ thuật giảm chiều dữ liệu không giám sát, hoạt động bằng cách tìm một hệ trục "
    "toạ độ mới (các thành phần chính) sao cho trục đầu tiên nằm dọc theo hướng có phương sai lớn "
    "nhất của dữ liệu, trục thứ hai trực giao với trục thứ nhất và có phương sai lớn thứ hai, và "
    "cứ tiếp tục như vậy. Về mặt toán học, các thành phần chính chính là các véc-tơ riêng (eigenvector) "
    "của ma trận hiệp phương sai của dữ liệu, sắp xếp theo thứ tự giảm dần của giá trị riêng tương ứng "
    "(explained variance). Khi giữ lại k thành phần chính đầu tiên (k nhỏ hơn số chiều gốc), ta thu "
    "được một biểu diễn dữ liệu có số chiều thấp hơn nhưng vẫn giữ lại phần lớn thông tin về phương "
    "sai của dữ liệu gốc.", "BodyVN"))
story.append(P(
    "Điều quan trọng cần lưu ý là PCA là một kỹ thuật <i>không giám sát</i>: nó tối ưu hoá việc giữ "
    "lại phương sai của các đặc trưng đầu vào X, mà hoàn toàn không sử dụng thông tin về biến mục "
    "tiêu y. Do đó, không có gì đảm bảo rằng các thành phần chính có phương sai lớn nhất cũng là "
    "những thành phần có khả năng dự báo tốt nhất cho y. Trong nhiều trường hợp — đặc biệt khi số "
    "chiều dữ liệu gốc đã thấp và ít dư thừa — việc áp dụng PCA có thể làm mất đi những thông tin "
    "hữu ích cho việc dự báo, dẫn đến hiệu năng mô hình giảm nhẹ so với khi không dùng PCA. Đây "
    "chính là một trong những giả thuyết được kiểm chứng thực nghiệm trong báo cáo này.", "BodyVN"))
story.append(PageBreak())

# ===================== 3. MO TA DU LIEU =====================
story.append(P("3. Mô tả và khảo sát bộ dữ liệu", "H1"))
story.append(P(
    "Bộ dữ liệu được sử dụng trong bài tập này là <b>Diabetes</b>, một bộ dữ liệu chuẩn có sẵn "
    "trong thư viện scikit-learn (được lưu kèm theo trong thư mục <font face='Courier'>data/</font> "
    "của mã nguồn dưới dạng tệp <font face='Courier'>diabetes.csv</font> để đảm bảo khả năng tái lập "
    "mà không phụ thuộc kết nối mạng). Bộ dữ liệu gồm 442 bệnh nhân, mỗi bệnh nhân được mô tả bởi "
    "10 đặc trưng sinh lý cơ bản: tuổi (age), giới tính (sex), chỉ số khối cơ thể (bmi), huyết áp "
    "trung bình (bp), và sáu chỉ số đo huyết thanh (s1 đến s6). Biến mục tiêu (target) là một chỉ "
    "số định lượng liên tục thể hiện mức độ tiến triển của bệnh tiểu đường sau một năm theo dõi kể "
    "từ thời điểm đo các đặc trưng ban đầu.", "BodyVN"))
story.append(P(
    "Các đặc trưng đầu vào trong bộ dữ liệu gốc đã được các tác giả chuẩn hoá sẵn (mean-centered "
    "và scale theo độ lệch chuẩn), tuy nhiên trong pipeline của báo cáo này, bước "
    "<font face='Courier'>StandardScaler</font> vẫn được áp dụng lại một cách tường minh nhằm đảm "
    "bảo tính tổng quát của mã nguồn khi áp dụng cho các bộ dữ liệu khác trong tương lai, đồng thời "
    "đây cũng là bước bắt buộc để PCA hoạt động chính xác, do PCA rất nhạy cảm với thang đo của các "
    "đặc trưng đầu vào.", "BodyVN"))

img = Image(os.path.join(OUT, "01_eda.png"), width=16 * cm, height=16 * cm * 0.33)
story.append(img)
story.append(P("Hình 1. Phân phối của biến mục tiêu (bên trái) và mức độ tương quan tuyến tính "
               "giữa từng đặc trưng với biến mục tiêu (bên phải).", "Caption"))

story.append(P(
    "Quan sát Hình 1 cho thấy biến mục tiêu có phân phối tương đối liên tục và không quá lệch, "
    "phù hợp để áp dụng trực tiếp các mô hình hồi quy mà không cần biến đổi (transform) thêm. Về "
    "mức độ tương quan, đặc trưng <font face='Courier'>bmi</font> và <font face='Courier'>s5</font> "
    "có tương quan dương mạnh nhất với biến mục tiêu, phù hợp với hiểu biết y khoa rằng chỉ số khối "
    "cơ thể và một số chỉ số huyết thanh có liên quan chặt chẽ đến sự tiến triển của bệnh tiểu đường. "
    "Không phát hiện giá trị thiếu (missing values) trong toàn bộ bộ dữ liệu.", "BodyVN"))

# ===================== 4. PHUONG PHAP =====================
story.append(P("4. Phương pháp thực nghiệm", "H1"))

story.append(P("4.1. Quy trình tiền xử lý và pipeline", "H2"))
story.append(P(
    "Toàn bộ dữ liệu được chia thành hai tập theo tỉ lệ 80/20: tập huấn luyện (train, 353 mẫu) "
    "dùng để huấn luyện mô hình và thực hiện cross-validation, và tập kiểm tra (test, 89 mẫu) chỉ "
    "được sử dụng một lần duy nhất ở bước đánh giá cuối cùng, nhằm đảm bảo tính khách quan của kết "
    "quả đánh giá. Việc chia dữ liệu được cố định bằng <font face='Courier'>random_state=42</font> "
    "để đảm bảo khả năng tái lập kết quả.", "BodyVN"))
story.append(P(
    "Mỗi mô hình được đặt bên trong một đối tượng <font face='Courier'>Pipeline</font> của "
    "scikit-learn, gồm các bước tuần tự: (1) <font face='Courier'>StandardScaler</font> để chuẩn "
    "hoá đặc trưng về trung bình 0, phương sai 1; (2) (tuỳ chọn) <font face='Courier'>PCA</font> để "
    "giảm chiều dữ liệu; (3) mô hình hồi quy cụ thể. Việc đóng gói toàn bộ quy trình tiền xử lý vào "
    "trong Pipeline là bắt buộc về mặt phương pháp luận: nếu chuẩn hoá hoặc PCA được thực hiện trước "
    "khi chia fold trong cross-validation, thông tin từ tập validation sẽ bị rò rỉ (data leakage) vào "
    "quá trình huấn luyện, dẫn đến đánh giá lạc quan sai lệch so với thực tế.", "BodyVN"))

story.append(P("4.2. Chiến lược đánh giá bằng Cross-Validation", "H2"))
story.append(P(
    "Trên tập huấn luyện, phương pháp <font face='Courier'>KFold</font> với k = 5 được sử dụng để "
    "đánh giá từng mô hình. Với mỗi fold, mô hình được huấn luyện trên 4 phần còn lại và đánh giá "
    "trên phần được giữ lại, sau đó lặp lại 5 lần để mỗi mẫu đều được dùng làm dữ liệu đánh giá đúng "
    "một lần. Ba chỉ số được tính toán trên mỗi fold:", "BodyVN"))
story.append(bullets([
    "<b>MAE (Mean Absolute Error):</b> trung bình trị tuyệt đối của sai số dự báo, đơn vị cùng đơn "
    "vị với biến mục tiêu, ít nhạy cảm với các giá trị ngoại lai (outlier).",
    "<b>RMSE (Root Mean Squared Error):</b> căn bậc hai của trung bình bình phương sai số, phạt "
    "nặng hơn đối với các sai số lớn, thường được dùng làm tiêu chí chính để so sánh mô hình.",
    "<b>R² (hệ số xác định):</b> tỉ lệ phương sai của biến mục tiêu được giải thích bởi mô hình, "
    "giá trị càng gần 1 càng tốt, giá trị 0 tương đương với việc luôn dự báo bằng giá trị trung bình.",
]))
story.append(P(
    "Ngoài giá trị trung bình của mỗi chỉ số qua 5 fold, độ lệch chuẩn (standard deviation) qua các "
    "fold cũng được ghi nhận nhằm đánh giá độ ổn định của mô hình: một mô hình có RMSE trung bình "
    "thấp nhưng độ lệch chuẩn cao có thể chỉ đang \"may mắn\" tốt trên một vài fold cụ thể, chứ chưa "
    "chắc là lựa chọn đáng tin cậy khi triển khai thực tế.", "BodyVN"))

story.append(P("4.3. Thiết lập baseline", "H2"))
story.append(P(
    "Mô hình cơ sở (baseline) được sử dụng là <font face='Courier'>DummyRegressor</font> với chiến "
    "lược <font face='Courier'>strategy='mean'</font>, tức luôn luôn dự báo bằng giá trị trung bình "
    "của biến mục tiêu trên tập huấn luyện, bất kể giá trị đầu vào là gì. Đây là ngưỡng tối thiểu mà "
    "bất kỳ mô hình học máy nào có ý nghĩa thực tiễn cũng cần phải vượt qua; một mô hình có RMSE gần "
    "hoặc cao hơn baseline được xem là không học được thông tin hữu ích từ dữ liệu.", "BodyVN"))
story.append(PageBreak())

# ===================== 5. KET QUA =====================
story.append(P("5. Kết quả thực nghiệm", "H1"))

story.append(P("5.1. Kết quả Cross-Validation không dùng PCA", "H2"))
df1 = pd.read_csv(os.path.join(OUT, "cv_results_no_pca.csv"), index_col=0).round(3)
table_data = [["Mô hình", "MAE", "RMSE", "R²"]]
for name, row in df1.iterrows():
    table_data.append([
        name,
        f"{row['MAE_mean']:.2f} ± {row['MAE_std']:.2f}",
        f"{row['RMSE_mean']:.2f} ± {row['RMSE_std']:.2f}",
        f"{row['R2_mean']:.3f} ± {row['R2_std']:.3f}",
    ])
t = Table(table_data, colWidths=[5 * cm, 4 * cm, 4 * cm, 4 * cm])
t.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (-1, -1), "VN"),
    ("FONTNAME", (0, 0), (-1, 0), "VN-Bold"),
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a2734")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f2f2")]),
    ("ALIGN", (1, 0), (-1, -1), "CENTER"),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story.append(t)
story.append(P("Bảng 1. Kết quả cross-validation 5-fold trên tập huấn luyện (không dùng PCA); "
               "giá trị trình bày theo dạng trung bình ± độ lệch chuẩn qua 5 fold.", "Caption"))
story.append(P(
    "Kết quả ở Bảng 1 cho thấy tất cả các mô hình hồi quy đều vượt trội rõ rệt so với baseline "
    "(RMSE của baseline xấp xỉ 78, trong khi các mô hình tốt nhất đạt RMSE khoảng 55). Nhóm mô hình "
    "tuyến tính có điều chuẩn nhẹ (Lasso, Ridge) và Linear Regression cho kết quả tốt nhất và khá "
    "tương đồng nhau, với độ lệch chuẩn qua các fold ở mức thấp, thể hiện tính ổn định cao. Các mô "
    "hình phi tuyến phức tạp hơn (SVR, Random Forest, Gradient Boosting) có RMSE cao hơn, cho thấy "
    "dấu hiệu chưa tận dụng được ưu thế biểu diễn phi tuyến, thậm chí có nguy cơ overfitting nhẹ do "
    "số lượng mẫu huấn luyện tương đối hạn chế (353 mẫu) so với độ phức tạp của mô hình.", "BodyVN"))

story.append(P("5.2. Khảo sát và tác động của PCA", "H2"))
story.append(P(
    f"Kết quả phân tích PCA cho thấy cần giữ lại {summary['n_components_95']}/10 thành phần chính "
    "để bảo toàn 95% tổng phương sai của dữ liệu đầu vào (xem Hình 2), cho thấy 10 đặc trưng gốc "
    "vốn đã tương đối độc lập với nhau và ít dư thừa thông tin — đây là dấu hiệu ban đầu cho thấy "
    "PCA có thể không mang lại nhiều lợi ích trên bộ dữ liệu này.", "BodyVN"))

img2 = Image(os.path.join(OUT, "02_pca_explained_variance.png"), width=10.5 * cm, height=10.5 * cm * 0.66)
img2.hAlign = "CENTER"
story.append(img2)
story.append(P("Hình 2. Phương sai tích luỹ (explained variance) theo số lượng thành phần chính "
               "được giữ lại.", "Caption"))

df_pca = pd.read_csv(os.path.join(OUT, "cv_results_pca.csv"), index_col=0).round(3)
table_data2 = [["Mô hình", "RMSE (không PCA)", f"RMSE (PCA, {summary['n_components_95']} PC)", "Chênh lệch"]]
for name in df1.index:
    r0 = df1.loc[name, "RMSE_mean"]
    r1 = df_pca.loc[name, "RMSE_mean"]
    table_data2.append([name, f"{r0:.2f}", f"{r1:.2f}", f"{r1 - r0:+.2f}"])
t2 = Table(table_data2, colWidths=[5 * cm, 3.7 * cm, 3.9 * cm, 3.4 * cm])
t2.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (-1, -1), "VN"),
    ("FONTNAME", (0, 0), (-1, 0), "VN-Bold"),
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a2734")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f2f2")]),
    ("ALIGN", (1, 0), (-1, -1), "CENTER"),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story.append(t2)
story.append(P("Bảng 2. So sánh trực tiếp RMSE (trung bình CV) giữa hai trường hợp có và không "
               "dùng PCA cho từng mô hình. Chênh lệch dương nghĩa là PCA làm RMSE tăng (kết quả xấu đi).", "Caption"))

story.append(PageBreak())

img3 = Image(os.path.join(OUT, "03_rmse_comparison.png"), width=16 * cm, height=16 * cm * 0.56)
story.append(img3)
story.append(P("Hình 3. Biểu đồ cột so sánh RMSE (kèm khoảng sai số ± độ lệch chuẩn) giữa hai "
               "trường hợp có và không dùng PCA, cho từng mô hình.", "Caption"))
story.append(P(
    "Số liệu ở Bảng 2 và Hình 3 xác nhận giả thuyết đã đặt ra ở Mục 2.3: việc áp dụng PCA trên bộ "
    "dữ liệu Diabetes không cải thiện được RMSE của bất kỳ mô hình nào, và với hầu hết các mô hình "
    "tuyến tính, PCA thậm chí làm RMSE tăng nhẹ. Nguyên nhân chính là do PCA tối ưu hoá theo tiêu "
    "chí giữ lại phương sai của X mà không quan tâm đến mối quan hệ giữa X và y; trên một bộ dữ liệu "
    "vốn đã có số chiều thấp (10 đặc trưng) và ít dư thừa thông tin (thể hiện qua việc cần tới 8/10 "
    "thành phần chính mới đạt 95% phương sai), việc loại bỏ dù chỉ một phần nhỏ thông tin cũng có "
    "thể làm mất đi tín hiệu hữu ích cho dự báo.", "BodyVN"))

story.append(P("5.3. Lựa chọn mô hình cuối cùng", "H2"))
story.append(P(
    f"Dựa trên tiêu chí RMSE trung bình CV thấp nhất kết hợp với độ ổn định qua các fold (độ lệch "
    f"chuẩn thấp), mô hình tốt nhất khi không dùng PCA là <b>{summary['best_model_no_pca']}</b>, còn "
    f"mô hình tốt nhất khi dùng PCA là <b>{summary['best_model_pca']}</b>. Vì phương án dùng PCA "
    f"không mang lại cải thiện nào, báo cáo quyết định chọn phương án "
    f"{'có' if summary['use_pca_final'] else 'không'} sử dụng PCA, với mô hình cuối cùng là "
    f"<b>{summary['final_model']}</b>. Việc không sử dụng PCA còn mang lại lợi ích phụ là giữ được "
    "khả năng diễn giải trực tiếp ý nghĩa của từng đặc trưng gốc trong mô hình cuối cùng, điều này "
    "có giá trị thực tiễn quan trọng trong lĩnh vực y tế.", "BodyVN"))

story.append(P("5.4. Đánh giá trên tập kiểm tra (test set)", "H2"))
story.append(P(
    "Mô hình được chọn ở bước trên được huấn luyện lại trên toàn bộ 353 mẫu của tập huấn luyện, "
    "sau đó được đánh giá đúng một lần duy nhất trên 89 mẫu của tập kiểm tra — tập dữ liệu này "
    "hoàn toàn chưa được sử dụng ở bất kỳ bước nào trước đó (kể cả cross-validation), nhằm đảm bảo "
    "kết quả phản ánh trung thực khả năng tổng quát hoá của mô hình.", "BodyVN"))

test_table = [
    ["Chỉ số", "Giá trị trên tập kiểm tra"],
    ["MAE", f"{summary['test_MAE']:.3f}"],
    ["RMSE", f"{summary['test_RMSE']:.3f}"],
    ["R²", f"{summary['test_R2']:.3f}"],
]
t3 = Table(test_table, colWidths=[6 * cm, 6 * cm])
t3.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (-1, -1), "VN"),
    ("FONTNAME", (0, 0), (-1, 0), "VN-Bold"),
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a2734")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTSIZE", (0, 0), (-1, -1), 9.5),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
    ("ALIGN", (1, 0), (-1, -1), "CENTER"),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story.append(t3)
story.append(P("Bảng 3. Hiệu năng của mô hình cuối cùng trên tập kiểm tra (test set).", "Caption"))

img4 = Image(os.path.join(OUT, "04_test_predictions.png"), width=16 * cm, height=16 * cm * 0.375)
story.append(img4)
story.append(P("Hình 4. Bên trái: giá trị thực tế so với giá trị dự báo trên tập kiểm tra (đường "
               "chấm đỏ thể hiện dự báo hoàn hảo). Bên phải: biểu đồ phần dư (residual) theo giá "
               "trị dự báo.", "Caption"))
story.append(P(
    "Quan sát Hình 4 cho thấy các điểm dữ liệu phân bố tương đối đều quanh đường chéo dự báo hoàn "
    "hảo, không có xu hướng lệch hệ thống rõ rệt. Biểu đồ phần dư cũng không cho thấy cấu trúc bất "
    "thường (ví dụ hình phễu thể hiện phương sai không đồng nhất — heteroscedasticity), củng cố "
    "thêm độ tin cậy của giả định tuyến tính trong mô hình được chọn.", "BodyVN"))
story.append(PageBreak())

# ===================== 6. THAO LUAN =====================
story.append(P("6. Thảo luận và phân tích sâu", "H1"))
story.append(P(
    "Kết quả thực nghiệm cho thấy ba nhận định chính. Thứ nhất, khoảng cách hiệu năng giữa baseline "
    "và các mô hình học máy thực sự là rất lớn (RMSE giảm từ khoảng 78 xuống còn khoảng 54–58 tuỳ "
    "mô hình), khẳng định rằng các đặc trưng đầu vào mang thông tin dự báo có ý nghĩa thống kê rõ "
    "ràng đối với biến mục tiêu.", "BodyVN"))
story.append(P(
    "Thứ hai, trái với kỳ vọng thông thường rằng các mô hình phức tạp hơn (ensemble, phi tuyến) sẽ "
    "cho kết quả tốt hơn, trên bộ dữ liệu Diabetes với kích thước mẫu khiêm tốn (chỉ 353 mẫu huấn "
    "luyện), các mô hình tuyến tính đơn giản với điều chuẩn nhẹ lại cho kết quả tốt và ổn định nhất. "
    "Đây là một minh hoạ thực nghiệm rõ ràng cho nguyên lý \"dao cạo Occam\" (Occam's razor) trong "
    "học máy: khi dữ liệu có kích thước hạn chế, mô hình đơn giản với độ phức tạp (capacity) phù hợp "
    "thường tổng quát hoá tốt hơn mô hình phức tạp, vốn dễ overfitting vào nhiễu của tập huấn luyện.", "BodyVN"))
story.append(P(
    "Thứ ba, kết quả về PCA cho thấy một bài học phương pháp luận quan trọng: PCA không phải là một "
    "bước tiền xử lý \"luôn luôn có lợi\" mà cần được áp dụng có chọn lọc, dựa trên đặc điểm cụ thể "
    "của bộ dữ liệu. Với các bộ dữ liệu có số chiều lớn (hàng trăm đến hàng nghìn đặc trưng) và tồn "
    "tại đa cộng tuyến mạnh, PCA thường mang lại lợi ích rõ rệt về cả tốc độ huấn luyện lẫn khả năng "
    "tổng quát hoá. Ngược lại, với các bộ dữ liệu có số chiều thấp và các đặc trưng đã tương đối độc "
    "lập — như trường hợp Diabetes — việc áp dụng PCA có thể phản tác dụng, do loại bỏ đi thông tin "
    "hữu ích mà không thực sự giải quyết được vấn đề đa cộng tuyến (vốn không tồn tại đáng kể trong "
    "bộ dữ liệu này).", "BodyVN"))
story.append(P(
    "Một điểm đáng lưu ý khác là độ lệch chuẩn qua các fold của các mô hình phi tuyến (đặc biệt SVR "
    "và Gradient Boosting) cao hơn rõ rệt so với các mô hình tuyến tính, cho thấy hiệu năng của các "
    "mô hình này nhạy cảm hơn với cách chia dữ liệu — một dấu hiệu gián tiếp khác của việc mô hình "
    "chưa thực sự ổn định trên bộ dữ liệu kích thước nhỏ này.", "BodyVN"))

# ===================== 7. HAN CHE VA HUONG PHAT TRIEN =====================
story.append(P("7. Hạn chế và hướng phát triển", "H1"))
story.append(P("Báo cáo còn tồn tại một số hạn chế có thể là hướng cải thiện trong các nghiên cứu tiếp theo:", "BodyVN"))
story.append(bullets([
    "<b>Chưa tinh chỉnh siêu tham số (hyperparameter tuning) một cách hệ thống:</b> các mô hình "
    "hiện dùng tham số mặc định hoặc giá trị được chọn thủ công (ví dụ alpha của Ridge/Lasso, C và "
    "gamma của SVR). Áp dụng GridSearchCV hoặc RandomizedSearchCV kết hợp nested cross-validation "
    "có thể giúp khai thác tốt hơn tiềm năng của từng mô hình, đặc biệt là các mô hình phi tuyến.",
    "<b>Kích thước mẫu còn hạn chế:</b> 442 mẫu là tương đối nhỏ đối với các mô hình ensemble phức "
    "tạp; kết luận về việc mô hình tuyến tính vượt trội có thể không còn đúng nếu áp dụng trên bộ "
    "dữ liệu lớn hơn.",
    "<b>Chưa khảo sát các phương pháp giảm chiều khác:</b> báo cáo mới chỉ dừng lại ở PCA tuyến "
    "tính; các phương pháp phi tuyến như Kernel PCA, t-SNE (cho trực quan hoá), hoặc các phương pháp "
    "chọn đặc trưng có giám sát (supervised feature selection như Recursive Feature Elimination) có "
    "thể mang lại góc nhìn bổ sung.",
    "<b>Chưa phân tích độ quan trọng đặc trưng (feature importance) một cách sâu sắc:</b> việc phân "
    "tích hệ số hồi quy của mô hình Lasso/Ridge hoặc feature importance của Random Forest có thể "
    "cung cấp thêm hiểu biết y khoa về các yếu tố ảnh hưởng mạnh nhất đến tiến triển bệnh.",
    "<b>Chưa kiểm định thống kê ý nghĩa của sự khác biệt giữa các mô hình:</b> các so sánh hiện tại "
    "dựa trên giá trị trung bình và độ lệch chuẩn của CV; việc áp dụng kiểm định thống kê (ví dụ "
    "paired t-test hoặc Wilcoxon signed-rank test giữa các fold) sẽ giúp khẳng định chắc chắn hơn "
    "liệu sự khác biệt về RMSE giữa các mô hình có ý nghĩa thống kê hay chỉ là nhiễu ngẫu nhiên.",
]))

# ===================== 8. KET LUAN =====================
story.append(P("8. Kết luận", "H1"))
story.append(P(
    "Báo cáo đã xây dựng thành công một pipeline hồi quy hoàn chỉnh trên bộ dữ liệu Diabetes, bao "
    "gồm đầy đủ các bước từ khảo sát dữ liệu, tiền xử lý, huấn luyện và so sánh nhiều mô hình, đến "
    "đánh giá bằng cross-validation và kiểm tra trên tập test độc lập. Kết quả thực nghiệm cho thấy "
    "các mô hình hồi quy tuyến tính có điều chuẩn nhẹ (Lasso, Ridge) đạt hiệu năng tốt nhất và ổn "
    "định nhất, vượt trội rõ rệt so với baseline. PCA không mang lại lợi ích trên bộ dữ liệu này do "
    "đặc điểm số chiều thấp và ít dư thừa thông tin của các đặc trưng gốc, minh hoạ rõ ràng cho "
    "nguyên lý rằng các kỹ thuật tiền xử lý cần được lựa chọn dựa trên đặc điểm cụ thể của từng bộ "
    "dữ liệu, chứ không nên áp dụng một cách máy móc.", "BodyVN"))
story.append(Spacer(1, 0.3 * cm))

story.append(P("Tài liệu tham khảo", "H1"))
story.append(bullets([
    "Pedregosa, F. và cộng sự (2011). \"Scikit-learn: Machine Learning in Python\". Journal of "
    "Machine Learning Research, 12, 2825–2830.",
    "Hastie, T., Tibshirani, R., Friedman, J. (2009). <i>The Elements of Statistical Learning: Data "
    "Mining, Inference, and Prediction</i>, 2nd Edition. Springer.",
    "Jolliffe, I. T. (2002). <i>Principal Component Analysis</i>, 2nd Edition. Springer Series in "
    "Statistics.",
    "Tài liệu chính thức bộ dữ liệu Diabetes: scikit-learn.org/stable/datasets/toy_dataset.html"
    "#diabetes-dataset",
]))

story.append(PageBreak())
story.append(P("Phụ lục A: Mô tả chi tiết các đặc trưng đầu vào", "H1"))
story.append(P(
    "Bảng dưới đây mô tả ý nghĩa của 10 đặc trưng đầu vào trong bộ dữ liệu Diabetes, giúp việc "
    "diễn giải mô hình hồi quy tuyến tính (hệ số của từng đặc trưng) có ý nghĩa thực tiễn rõ ràng "
    "hơn trong bối cảnh y khoa.", "BodyVN"))

feature_desc = [
    ("age", "Tuổi của bệnh nhân (đã được chuẩn hoá)."),
    ("sex", "Giới tính của bệnh nhân (đã được mã hoá số và chuẩn hoá)."),
    ("bmi", "Chỉ số khối cơ thể (Body Mass Index) — liên quan trực tiếp đến nguy cơ tiểu đường."),
    ("bp", "Huyết áp trung bình (average blood pressure)."),
    ("s1", "Tổng cholesterol trong huyết thanh (TC)."),
    ("s2", "Lipoprotein tỉ trọng thấp (LDL — low-density lipoproteins)."),
    ("s3", "Lipoprotein tỉ trọng cao (HDL — high-density lipoproteins)."),
    ("s4", "Tỉ lệ cholesterol toàn phần trên HDL (TCH)."),
    ("s5", "Logarit của nồng độ triglyceride trong huyết thanh (LTG)."),
    ("s6", "Nồng độ đường huyết (glucose level)."),
]
feat_table = [["Đặc trưng", "Ý nghĩa"]] + [[c, d] for c, d in feature_desc]
tf = Table(feat_table, colWidths=[3 * cm, 13 * cm])
tf.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (-1, -1), "VN"),
    ("FONTNAME", (0, 0), (-1, 0), "VN-Bold"),
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a2734")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTSIZE", (0, 0), (-1, -1), 9.3),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f2f2")]),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story.append(tf)
story.append(P("Bảng A1. Mô tả ý nghĩa của 10 đặc trưng đầu vào trong bộ dữ liệu Diabetes.", "Caption"))

story.append(P("Phụ lục B: Siêu tham số của các mô hình", "H1"))
story.append(P(
    "Bảng dưới đây liệt kê siêu tham số cụ thể được sử dụng cho từng mô hình trong thực nghiệm. "
    "Các giá trị này được chọn dựa trên kinh nghiệm thực nghiệm phổ biến; như đã đề cập ở Mục 7, "
    "việc tinh chỉnh siêu tham số một cách hệ thống bằng GridSearchCV là một hướng cải thiện quan "
    "trọng cho các nghiên cứu tiếp theo.", "BodyVN"))
hyper_table = [
    ["Mô hình", "Siêu tham số chính"],
    ["Baseline (mean)", "strategy='mean'"],
    ["Linear Regression", "Mặc định (không điều chuẩn)"],
    ["Ridge", "alpha = 1.0"],
    ["Lasso", "alpha = 0.1"],
    ["SVR (RBF)", "kernel='rbf', C = 10, gamma='scale'"],
    ["Random Forest", "n_estimators = 300, random_state = 42"],
    ["Gradient Boosting", "Mặc định của scikit-learn, random_state = 42"],
]
th = Table(hyper_table, colWidths=[5 * cm, 11 * cm])
th.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (-1, -1), "VN"),
    ("FONTNAME", (0, 0), (-1, 0), "VN-Bold"),
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a2734")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTSIZE", (0, 0), (-1, -1), 9.3),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f2f2")]),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story.append(th)
story.append(P("Bảng B1. Siêu tham số cụ thể của từng mô hình dùng trong thực nghiệm.", "Caption"))

story.append(P(
    "Ngoài các siêu tham số riêng của từng mô hình, một số cấu hình chung được áp dụng thống nhất "
    "cho toàn bộ thực nghiệm nhằm đảm bảo khả năng so sánh công bằng và tái lập được kết quả:", "BodyVN"))
story.append(bullets([
    "<b>random_state = 42</b> cho mọi bước có yếu tố ngẫu nhiên (chia train/test, KFold, khởi tạo "
    "trọng số của Random Forest/Gradient Boosting), đảm bảo kết quả không đổi giữa các lần chạy lại.",
    "<b>Tỉ lệ chia dữ liệu:</b> 80% huấn luyện / 20% kiểm tra, với tập kiểm tra chỉ được sử dụng "
    "đúng một lần ở bước đánh giá cuối cùng.",
    "<b>Số fold cross-validation:</b> k = 5, cân bằng giữa độ tin cậy thống kê của ước lượng và chi "
    "phí tính toán.",
    "<b>Ngưỡng phương sai PCA:</b> 95%, một ngưỡng phổ biến trong thực hành giúp giữ lại phần lớn "
    "thông tin của dữ liệu gốc trong khi vẫn giảm được số chiều.",
]))

story.append(P("Phụ lục C: Quy trình tái lập kết quả", "H1"))
story.append(P(
    "Để đảm bảo tính minh bạch khoa học, dưới đây là trình tự các bước chính xác để tái lập toàn bộ "
    "kết quả trong báo cáo này từ đầu, sử dụng mã nguồn đi kèm:", "BodyVN"))
story.append(bullets([
    "Cài đặt các thư viện liệt kê trong <font face='Courier'>requirements.txt</font> vào một môi "
    "trường Python (khuyến nghị dùng môi trường ảo riêng để tránh xung đột phiên bản).",
    "Chạy tệp <font face='Courier'>main.py</font> — chương trình sẽ tự động tải bộ dữ liệu Diabetes "
    "từ scikit-learn (không cần kết nối mạng ngoài do dữ liệu được đóng gói sẵn trong thư viện), "
    "thực hiện toàn bộ pipeline (EDA, chia dữ liệu, cross-validation có/không PCA, chọn mô hình, "
    "đánh giá trên test set), và ghi toàn bộ hình ảnh, bảng số liệu, tệp tóm tắt "
    "<font face='Courier'>summary.json</font> vào thư mục <font face='Courier'>outputs/</font>.",
    "Chạy tệp <font face='Courier'>make_report.py</font> để sinh lại chính báo cáo PDF này từ dữ "
    "liệu mới nhất trong <font face='Courier'>outputs/</font> — đảm bảo báo cáo luôn phản ánh đúng "
    "kết quả thực nghiệm gần nhất, tránh tình trạng số liệu trong báo cáo không khớp với mã nguồn.",
    "(Tuỳ chọn) Mở <font face='Courier'>notebook.ipynb</font> bằng Jupyter để xem lại từng bước một "
    "cách trực quan, tương tác, kèm theo diễn giải chi tiết cho từng ô lệnh.",
]))
story.append(P(
    "Do toàn bộ quy trình đều cố định <font face='Courier'>random_state = 42</font>, việc chạy lại "
    "mã nguồn trên bất kỳ máy tính nào có cùng phiên bản thư viện sẽ cho ra kết quả số học giống hệt "
    "như trình bày trong báo cáo, đảm bảo tính tái lập (reproducibility) — một tiêu chí quan trọng "
    "của nghiên cứu khoa học nói chung và các bài tập thực hành học máy nói riêng.", "BodyVN"))


story.append(P("Phụ lục D: Cấu trúc mã nguồn", "H1"))
story.append(P(
    "Toàn bộ mã nguồn và kết quả của bài tập được tổ chức trong repository đi kèm báo cáo này, với "
    "cấu trúc như sau:", "BodyVN"))
story.append(Paragraph(
    "baitap1-hoiqui-pca/<br/>"
    "├── main.py&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# script chính, chạy toàn bộ pipeline từ đầu đến cuối<br/>"
    "├── notebook.ipynb&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# notebook tương đương, có sẵn output<br/>"
    "├── make_report.py&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# script tự sinh lại báo cáo PDF từ outputs/<br/>"
    "├── BaoCao_BaiTap1.pdf&nbsp;&nbsp;&nbsp;# báo cáo này<br/>"
    "├── outputs/&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# hình ảnh, bảng CSV, summary.json sau khi chạy<br/>"
    "├── requirements.txt<br/>"
    "└── README.md",
    styles["Mono"],
))
story.append(P(
    "Chi tiết hướng dẫn cài đặt môi trường và cách chạy lại toàn bộ thực nghiệm được trình bày đầy "
    "đủ trong tệp <font face='Courier'>README.md</font> đi kèm.", "BodyVN"))


# ===================== PHU LUC: HUONG DAN SU DUNG MA NGUON =====================
story.append(PageBreak())
story.append(P("Phụ lục E: Hướng dẫn sử dụng mã nguồn", "H1"))

story.append(P("1. Yêu cầu hệ thống", "H2"))
story.append(bullets([
    "Python từ 3.9 trở lên (đã kiểm thử với Python 3.12).",
    "Các thư viện trong <font face='Courier'>requirements.txt</font>: numpy, pandas, matplotlib, "
    "scikit-learn (từ 1.4 trở lên), jupyter, ipykernel, reportlab, pypdf.",
    "Không cần kết nối mạng khi chạy vì bộ dữ liệu được đóng gói sẵn trong scikit-learn.",
]))

story.append(P("2. Cài đặt môi trường", "H2"))
story.append(P("Mở terminal (hoặc Command Prompt / PowerShell trên Windows) tại thư mục "
               "<font face='Courier'>baitap1</font> và thực hiện lần lượt:", "BodyVN"))
story.append(Paragraph(
    "python -m venv venv<br/>"
    "source venv/bin/activate&nbsp;&nbsp;&nbsp;&nbsp;(macOS/Linux)<br/>"
    "venv\\Scripts\\activate&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(Windows)<br/>"
    "pip install --upgrade pip<br/>"
    "pip install -r requirements.txt",
    styles["Cmd"]))

story.append(P("3. Chạy chương trình", "H2"))
cmd_rows = [
    [P("<b>Mục đích</b>", "Cell"), P("<b>Lệnh</b>", "Cell"), P("<b>Kết quả</b>", "Cell")],
    [P("Chạy toàn bộ pipeline", "Cell"), P("<font face='Courier'>python main.py</font>", "Cell"),
     P("In tiến trình ra màn hình; ghi hình, bảng CSV và summary.json vào <font face='Courier'>outputs/</font>.", "Cell")],
    [P("Sinh lại báo cáo PDF", "Cell"), P("<font face='Courier'>python make_report.py</font>", "Cell"),
     P("Tạo lại tệp PDF từ dữ liệu trong <font face='Courier'>outputs/</font> (phải chạy main.py trước).", "Cell")],
    [P("Chạy từng bước tương tác", "Cell"), P("<font face='Courier'>jupyter notebook</font>", "Cell"),
     P("Mở <font face='Courier'>notebook.ipynb</font>, chọn Kernel → Restart &amp; Run All.", "Cell")],
]
tc = Table(cmd_rows, colWidths=[3.8 * cm, 4.6 * cm, 7.6 * cm])
tc.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8edf3")),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
]))
story.append(tc)
story.append(P("Bảng E1. Các lệnh chạy chính của bài tập.", "Caption"))

story.append(P("4. Các tệp kết quả trong thư mục outputs/", "H2"))
out_rows = [[P("<b>Tệp</b>", "Cell"), P("<b>Nội dung</b>", "Cell")]] + [
    [P("<font face='Courier'>%s</font>" % a, "Cell"), P(b, "Cell")] for a, b in [('cv_results_no_pca.csv', 'MAE, RMSE, R² (trung bình và độ lệch chuẩn qua 5 fold) của 7 mô hình khi không dùng PCA.'), ('cv_results_pca.csv', 'Kết quả tương tự khi thêm PCA giữ 95% phương sai.'), ('eda_describe.csv', 'Thống kê mô tả các đặc trưng và biến mục tiêu.'), ('01_eda.png', 'Hình phân phối target và tương quan đặc trưng với target.'), ('02_pca_explained_variance.png', 'Đường phương sai tích luỹ theo số thành phần chính.'), ('03_rmse_comparison.png', 'Biểu đồ cột so sánh RMSE có và không PCA.'), ('04_test_predictions.png', 'Thực tế so với dự báo và biểu đồ phần dư trên tập kiểm tra.'), ('summary.json', 'Mô hình được chọn, có dùng PCA hay không, MAE/RMSE/R² trên tập kiểm tra.')]
]
to = Table(out_rows, colWidths=[6 * cm, 10 * cm])
to.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8edf3")),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
]))
story.append(to)
story.append(P("Bảng E2. Danh sách tệp sinh ra sau khi chạy main.py.", "Caption"))

story.append(P("5. Các tham số có thể điều chỉnh", "H2"))
par_rows = [[P("<b>Tham số</b>", "Cell"), P("<b>Vị trí</b>", "Cell"), P("<b>Ý nghĩa</b>", "Cell")]] + [
    [P("<font face='Courier'>%s</font>" % a, "Cell"), P(b, "Cell"), P(c, "Cell")]
    for a, b, c in [('RANDOM_STATE', 'main.py (đầu tệp)', 'Hạt giống ngẫu nhiên, mặc định 42; đổi để kiểm tra độ ổn định của kết quả.'), ('test_size', 'train_test_split', 'Tỉ lệ tập kiểm tra, mặc định 0.2.'), ('n_splits', 'KFold', 'Số fold của cross-validation, mặc định 5.'), ('models', 'hàm main()', 'Từ điển các mô hình; thêm hoặc bớt mô hình, đổi alpha, C, n_estimators tại đây.'), ('0.95', 'n_components_95', 'Ngưỡng phương sai PCA cần giữ; đổi sang 0.90 hoặc 0.99 để khảo sát.')]
]
tp = Table(par_rows, colWidths=[3.8 * cm, 4.2 * cm, 8 * cm])
tp.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8edf3")),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
]))
story.append(tp)
story.append(P("Bảng E3. Các tham số thường được thay đổi khi thử nghiệm.", "Caption"))

story.append(P("6. Các hàm và lớp chính trong main.py", "H2"))
fn_rows = [[P("<b>Tên</b>", "Cell"), P("<b>Chức năng</b>", "Cell")]] + [
    [P("<font face='Courier'>%s</font>" % a, "Cell"), P(b, "Cell")] for a, b in [('make_pipeline()', 'Tạo Pipeline gồm StandardScaler, PCA (tuỳ chọn) và mô hình hồi quy.'), ('evaluate_cv()', 'Chạy cross-validation 5 fold, trả về MAE, RMSE, R² dạng trung bình và độ lệch chuẩn.'), ('main()', 'Điều phối toàn bộ quy trình: nạp dữ liệu, EDA, CV có và không PCA, chọn mô hình, đánh giá test, lưu kết quả.')]
]
tf2 = Table(fn_rows, colWidths=[5.2 * cm, 10.8 * cm])
tf2.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8edf3")),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
]))
story.append(tf2)
story.append(P("Bảng E4. Các thành phần chính của mã nguồn.", "Caption"))

story.append(P("7. Xử lý một số lỗi thường gặp", "H2"))
er_rows = [[P("<b>Hiện tượng</b>", "Cell"), P("<b>Nguyên nhân và cách khắc phục</b>", "Cell")]] + [
    [P(a, "Cell"), P(b, "Cell")] for a, b in [("ModuleNotFoundError: No module named 'sklearn' (hoặc numpy, pandas...)", 'Chưa cài thư viện hoặc chưa kích hoạt môi trường ảo. Kích hoạt lại venv rồi chạy pip install -r requirements.txt.'), ('Lệnh activate bị chặn trên PowerShell (Windows)', 'Chạy Set-ExecutionPolicy -Scope Process RemoteSigned trong cửa sổ PowerShell đó, hoặc dùng Command Prompt.'), ('make_report.py báo FileNotFoundError khi mở ảnh hoặc CSV', 'Chưa có thư mục outputs/ đầy đủ. Chạy python main.py trước rồi mới chạy make_report.py.'), ('Chữ trong PDF bị ô vuông hoặc mất dấu tiếng Việt', 'Không tìm thấy font DejaVu Sans. Cài matplotlib (đã kèm font này) hoặc đặt DejaVuSans.ttf và DejaVuSans-Bold.ttf cạnh make_report.py.'), ('Jupyter không tìm thấy kernel', 'Chạy python -m ipykernel install --user rồi mở lại notebook và chọn kernel Python tương ứng.'), ('Lỗi khi gọi root_mean_squared_error', 'Phiên bản scikit-learn cũ hơn 1.4. Nâng cấp bằng pip install -U scikit-learn.')]
]
te = Table(er_rows, colWidths=[5.6 * cm, 10.4 * cm])
te.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8edf3")),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
]))
story.append(te)
story.append(P("Bảng E5. Lỗi thường gặp và cách khắc phục.", "Caption"))


doc = SimpleDocTemplate(
    REPORT_PATH, pagesize=A4,
    leftMargin=2.2 * cm, rightMargin=2.2 * cm, topMargin=2 * cm, bottomMargin=2 * cm,
    title="Bao cao Bai tap 1 - Hoi quy va PCA",
)
doc.build(story)

from pypdf import PdfReader
n = len(PdfReader(REPORT_PATH).pages)
print(f"Da tao: {REPORT_PATH} | So trang: {n}")
