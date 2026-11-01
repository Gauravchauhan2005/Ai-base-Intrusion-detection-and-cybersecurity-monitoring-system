import os
import sys
import time
import json
import logging
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, precision_recall_fscore_support
from sklearn.ensemble import IsolationForest
from xgboost import XGBClassifier

# Ensure ml pipeline is importable
sys.path.insert(0, os.path.abspath("."))
from ml.pipeline.preprocessor import Preprocessor

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("ml_trainer")

def train_and_evaluate(
    data_path: str = "ml/dataset/cicids2018_sample.csv",
    output_dir: str = "ml/models"
):
    os.makedirs(output_dir, exist_ok=True)
    logger.info(f"Loading dataset from {data_path}...")
    df = pd.read_csv(data_path)
    logger.info(f"Loaded {len(df)} records. Classes: {df['true_label'].unique().tolist()}")

    # 1. Preprocessing and feature transformation
    preprocessor = Preprocessor()
    preprocessor.fit(df, label_col="true_label")
    
    X = preprocessor.transform_dataframe(df)
    y = preprocessor.label_encoder.transform(df["true_label"].astype(str))
    classes = list(preprocessor.label_encoder.classes_)
    
    # 2. Train-test split (80/20 stratified)
    X_train, X_test, y_train, y_test, df_train, df_test = train_test_split(
        X, y, df, test_size=0.20, random_state=42, stratify=y
    )
    logger.info(f"Train split: {len(X_train)} samples, Test split: {len(X_test)} samples")

    # 3. Train Supervised XGBoost Classifier
    logger.info("Training XGBoost multi-class classifier...")
    xgb = XGBClassifier(
        n_estimators=120,
        max_depth=6,
        learning_rate=0.1,
        subsample=0.85,
        colsample_bytree=0.85,
        objective="multi:softprob",
        eval_metric="mlogloss",
        random_state=42,
        n_jobs=-1
    )
    t0 = time.time()
    xgb.fit(X_train, y_train)
    xgb_train_time = time.time() - t0
    logger.info(f"XGBoost trained in {xgb_train_time:.2f}s")

    # 4. Train Unsupervised Isolation Forest (Anomaly Detector)
    logger.info("Training Isolation Forest unsupervised anomaly detector...")
    # Train primarily on benign baseline flows to detect out-of-distribution deviations
    benign_idx = preprocessor.label_encoder.transform(["Benign"])[0]
    X_benign_train = X_train[y_train == benign_idx]
    
    iso_forest = IsolationForest(
        n_estimators=100,
        contamination=0.08,
        max_samples="auto",
        random_state=42,
        n_jobs=-1
    )
    iso_forest.fit(X_benign_train)
    logger.info("Isolation Forest trained successfully.")

    # 5. Model Evaluation
    logger.info("Evaluating XGBoost model on held-out test dataset...")
    y_pred = xgb.predict(X_test)
    y_proba = xgb.predict_proba(X_test)
    
    report_dict = classification_report(
        y_test, y_pred, target_names=classes, output_dict=True, zero_division=0
    )
    print("\n" + "="*70)
    print("CLASSIFICATION REPORT (XGBoost on CICIDS2018):")
    print("="*70)
    print(classification_report(y_test, y_pred, target_names=classes, zero_division=0))

    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    print("\nCONFUSION MATRIX:")
    print(cm)

    # False Positive Rate Calculation:
    # A False Positive occurs when Benign is incorrectly predicted as an Attack.
    benign_mask = (y_test == benign_idx)
    benign_total = int(np.sum(benign_mask))
    false_positives = int(np.sum(y_pred[benign_mask] != benign_idx))
    fpr = (false_positives / benign_total) if benign_total > 0 else 0.0
    print(f"\nFALSE POSITIVE RATE (FPR on Benign): {fpr * 100:.2f}% ({false_positives}/{benign_total})")

    # Single-event inference latency benchmark
    latencies = []
    for i in range(min(500, len(X_test))):
        start = time.perf_counter()
        _ = xgb.predict_proba(X_test[i:i+1])
        _ = iso_forest.score_samples(X_test[i:i+1])
        latencies.append((time.perf_counter() - start) * 1000.0)
    
    avg_latency = float(np.mean(latencies))
    p95_latency = float(np.percentile(latencies, 95))
    p99_latency = float(np.percentile(latencies, 99))
    logger.info(f"Latency benchmark: mean={avg_latency:.2f}ms, p95={p95_latency:.2f}ms, p99={p99_latency:.2f}ms")

    # Feature importances
    feature_importances = dict(zip(preprocessor.feature_names, [float(v) for v in xgb.feature_importances_]))
    sorted_importances = sorted(feature_importances.items(), key=lambda x: x[1], reverse=True)[:10]

    # Save artifacts
    logger.info("Saving trained models and evaluation metrics to disk...")
    preprocessor.save(os.path.join(output_dir, "preprocessor.joblib"))
    joblib.dump(xgb, os.path.join(output_dir, "xgb_model.joblib"))
    xgb.save_model(os.path.join(output_dir, "xgb_model.json"))
    joblib.dump(iso_forest, os.path.join(output_dir, "isolation_forest.joblib"))

    metrics_payload = {
        "model_version": "v1.0.0",
        "training_date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_samples": len(df),
        "test_samples": len(X_test),
        "classes": classes,
        "classification_report": report_dict,
        "false_positive_rate": fpr,
        "accuracy": float(report_dict["accuracy"]),
        "macro_f1": float(report_dict["macro avg"]["f1-score"]),
        "weighted_f1": float(report_dict["weighted avg"]["f1-score"]),
        "avg_inference_latency_ms": avg_latency,
        "p95_inference_latency_ms": p95_latency,
        "top_features": sorted_importances
    }

    with open(os.path.join(output_dir, "metrics.json"), "w") as f:
        json.dump(metrics_payload, f, indent=2)

    logger.info(f"Training and evaluation complete. Artifacts saved in {output_dir}")
    return metrics_payload

if __name__ == "__main__":
    train_and_evaluate()
