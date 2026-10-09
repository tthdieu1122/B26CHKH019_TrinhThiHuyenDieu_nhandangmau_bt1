"""
Bai tap 1 - Pipeline hoi quy voi tien xu ly va giam chieu PCA
Mon: Nhan dang mau (Pattern Recognition) - Cao hoc

Chay:
    python main.py

Dau ra: cac hinh (.png) va bang ket qua (.csv) trong thu muc outputs/
"""
import json
import os

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split, KFold, cross_validate
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error

RANDOM_STATE = 42
OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs")
os.makedirs(OUT_DIR, exist_ok=True)

np.random.seed(RANDOM_STATE)


def make_pipeline(model, use_pca=False, n_components=None):
    steps = [("scaler", StandardScaler())]
    if use_pca:
        steps.append(("pca", PCA(n_components=n_components, random_state=RANDOM_STATE)))
    steps.append(("model", model))
    return Pipeline(steps)


def evaluate_cv(model, X_train, y_train, cv, scoring, use_pca=False, n_components=None):
    pipe = make_pipeline(model, use_pca=use_pca, n_components=n_components)
    res = cross_validate(pipe, X_train, y_train, cv=cv, scoring=scoring)
    return {
        "MAE_mean": -res["test_MAE"].mean(), "MAE_std": res["test_MAE"].std(),
        "RMSE_mean": -res["test_RMSE"].mean(), "RMSE_std": res["test_RMSE"].std(),
        "R2_mean": res["test_R2"].mean(), "R2_std": res["test_R2"].std(),
    }


def main():
    # 1. Du lieu
    data = load_diabetes(as_frame=True)
    X, y = data.data, data.target
    print(f"[1] Du lieu: {X.shape[0]} mau, {X.shape[1]} dac trung")

    df = X.copy()
    df["target"] = y
    df.describe().T.to_csv(os.path.join(OUT_DIR, "eda_describe.csv"))

    fig, ax = plt.subplots(1, 2, figsize=(12, 4))
    ax[0].hist(y, bins=30, color="steelblue", edgecolor="white")
    ax[0].set_title("Phân phối biến mục tiêu")
    corr = df.corr()["target"].drop("target").sort_values()
    ax[1].barh(corr.index, corr.values, color="indianred")
    ax[1].set_title("Tương quan đặc trưng với mục tiêu")
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "01_eda.png"), dpi=150)
    plt.close(fig)

    # 2. Chia train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE
    )
    print(f"[2] Train: {X_train.shape}, Test: {X_test.shape}")

    # 3. Mo hinh
    models = {
        "Baseline (mean)": DummyRegressor(strategy="mean"),
        "Linear Regression": LinearRegression(),
        "Ridge": Ridge(alpha=1.0, random_state=RANDOM_STATE),
        "Lasso": Lasso(alpha=0.1, random_state=RANDOM_STATE),
        "SVR (RBF)": SVR(kernel="rbf", C=10, gamma="scale"),
        "Random Forest": RandomForestRegressor(n_estimators=300, random_state=RANDOM_STATE),
        "Gradient Boosting": GradientBoostingRegressor(random_state=RANDOM_STATE),
    }

    cv = KFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    scoring = {"MAE": "neg_mean_absolute_error", "RMSE": "neg_root_mean_squared_error", "R2": "r2"}

    # 4. CV khong PCA
    print("[3] Cross-validation (khong PCA)...")
    results_no_pca = {name: evaluate_cv(m, X_train, y_train, cv, scoring) for name, m in models.items()}
    df_no_pca = pd.DataFrame(results_no_pca).T[["MAE_mean", "MAE_std", "RMSE_mean", "RMSE_std", "R2_mean", "R2_std"]]
    df_no_pca.to_csv(os.path.join(OUT_DIR, "cv_results_no_pca.csv"))
    print(df_no_pca.sort_values("RMSE_mean"))

    # 5. PCA explained variance + CV co PCA
    pca_full = PCA(random_state=RANDOM_STATE).fit(StandardScaler().fit_transform(X_train))
    explained = np.cumsum(pca_full.explained_variance_ratio_)
    n_components_95 = int(np.argmax(explained >= 0.95) + 1)
    print(f"[4] So thanh phan PCA de dat 95% phuong sai: {n_components_95}/{X.shape[1]}")

    fig, ax = plt.subplots()
    ax.plot(range(1, len(explained) + 1), explained, marker="o")
    ax.axhline(0.95, color="red", linestyle="--", label="95% phương sai")
    ax.set_xlabel("Số thành phần chính"); ax.set_ylabel("Phương sai tích luỹ")
    ax.set_title("Phương sai tích luỹ theo số thành phần PCA")
    ax.legend(); ax.grid(alpha=0.3)
    fig.savefig(os.path.join(OUT_DIR, "02_pca_explained_variance.png"), dpi=150)
    plt.close(fig)

    print("[5] Cross-validation (co PCA)...")
    results_pca = {
        name: evaluate_cv(m, X_train, y_train, cv, scoring, use_pca=True, n_components=n_components_95)
        for name, m in models.items()
    }
    df_pca = pd.DataFrame(results_pca).T[["MAE_mean", "MAE_std", "RMSE_mean", "RMSE_std", "R2_mean", "R2_std"]]
    df_pca.to_csv(os.path.join(OUT_DIR, "cv_results_pca.csv"))
    print(df_pca.sort_values("RMSE_mean"))

    fig, ax = plt.subplots(figsize=(9, 5))
    x = np.arange(len(models))
    width = 0.35
    ax.bar(x - width / 2, df_no_pca["RMSE_mean"], width, yerr=df_no_pca["RMSE_std"], label="Không PCA", capsize=4)
    ax.bar(x + width / 2, df_pca["RMSE_mean"], width, yerr=df_pca["RMSE_std"], label=f"PCA ({n_components_95} PC)", capsize=4)
    ax.set_xticks(x); ax.set_xticklabels(models.keys(), rotation=30, ha="right")
    ax.set_ylabel("RMSE (trung bình CV ± độ lệch chuẩn)")
    ax.set_title("So sánh RMSE: có PCA và không PCA")
    ax.legend()
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "03_rmse_comparison.png"), dpi=150)
    plt.close(fig)

    # 6. Chon mo hinh tot nhat
    best_name_no_pca = df_no_pca["RMSE_mean"].idxmin()
    best_name_pca = df_pca["RMSE_mean"].idxmin()
    use_pca_final = df_pca.loc[best_name_pca, "RMSE_mean"] < df_no_pca.loc[best_name_no_pca, "RMSE_mean"]
    final_model_name = best_name_pca if use_pca_final else best_name_no_pca
    print(f"[6] Mo hinh duoc chon: {final_model_name} | Dung PCA: {use_pca_final}")

    # 7. Danh gia tren test
    final_pipe = make_pipeline(
        models[final_model_name], use_pca=use_pca_final,
        n_components=n_components_95 if use_pca_final else None,
    )
    final_pipe.fit(X_train, y_train)
    y_pred = final_pipe.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = root_mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"[7] TEST -- {final_model_name} (PCA={use_pca_final}): MAE={mae:.3f} RMSE={rmse:.3f} R2={r2:.3f}")

    fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))
    ax[0].scatter(y_test, y_pred, alpha=0.6, color="teal")
    lims = [min(y_test.min(), y_pred.min()), max(y_test.max(), y_pred.max())]
    ax[0].plot(lims, lims, "r--")
    ax[0].set_xlabel("Giá trị thực tế"); ax[0].set_ylabel("Giá trị dự báo")
    ax[0].set_title("Thực tế và Dự báo (tập kiểm tra)")

    residuals = y_test - y_pred
    ax[1].scatter(y_pred, residuals, alpha=0.6, color="orange")
    ax[1].axhline(0, color="red", linestyle="--")
    ax[1].set_xlabel("Giá trị dự báo"); ax[1].set_ylabel("Phần dư")
    ax[1].set_title("Biểu đồ phần dư")
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "04_test_predictions.png"), dpi=150)
    plt.close(fig)

    summary = {
        "n_components_95": n_components_95,
        "best_model_no_pca": best_name_no_pca,
        "best_model_pca": best_name_pca,
        "final_model": final_model_name,
        "use_pca_final": bool(use_pca_final),
        "test_MAE": mae,
        "test_RMSE": rmse,
        "test_R2": r2,
    }
    with open(os.path.join(OUT_DIR, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"\nHoan tat. Ket qua duoc luu trong: {OUT_DIR}")


if __name__ == "__main__":
    main()
