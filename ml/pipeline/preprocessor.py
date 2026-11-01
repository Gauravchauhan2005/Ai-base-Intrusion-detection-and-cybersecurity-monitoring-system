import numpy as np
import pandas as pd
import joblib
from typing import List, Dict, Any, Tuple, Optional
from sklearn.preprocessing import StandardScaler, LabelEncoder

# 38 core flow features aligned with CICIDS2018 standard flow specifications
NUMERIC_FEATURES = [
    "dst_port",
    "flow_duration",
    "tot_fwd_pkts",
    "tot_bwd_pkts",
    "totlen_fwd_pkts",
    "totlen_bwd_pkts",
    "fwd_pkt_len_max",
    "fwd_pkt_len_min",
    "fwd_pkt_len_mean",
    "bwd_pkt_len_max",
    "bwd_pkt_len_min",
    "bwd_pkt_len_mean",
    "flow_byts_s",
    "flow_pkts_s",
    "flow_iat_mean",
    "flow_iat_std",
    "flow_iat_max",
    "flow_iat_min",
    "fwd_iat_tot",
    "bwd_iat_tot",
    "fwd_psh_flags",
    "bwd_psh_flags",
    "fwd_urg_flags",
    "bwd_urg_flags",
    "fwd_header_len",
    "bwd_header_len",
    "fwd_pkts_s",
    "bwd_pkts_s",
    "pkt_len_min",
    "pkt_len_max",
    "pkt_len_mean",
    "pkt_len_std",
    "pkt_len_var",
    "fin_flag_cnt",
    "syn_flag_cnt",
    "rst_flag_cnt",
    "psh_flag_cnt",
    "ack_flag_cnt",
    "down_up_ratio",
    "init_fwd_win_byts",
    "init_bwd_win_byts",
]

class Preprocessor:
    """
    Reusable feature engineering, cleaning, and normalization pipeline.
    Shared strictly between offline model training and real-time online inference.
    """
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.feature_names = NUMERIC_FEATURES
        self.is_fitted = False
        self.feature_medians: Dict[str, float] = {}

    def fit(self, df: pd.DataFrame, label_col: Optional[str] = "true_label") -> "Preprocessor":
        """Fits scaler and label encoder on training dataset."""
        cleaned_df = self._clean_dataframe(df)
        X = cleaned_df[self.feature_names].values
        self.scaler.fit(X)

        # Compute medians for handling missing runtime attributes
        for col in self.feature_names:
            self.feature_medians[col] = float(cleaned_df[col].median())

        if label_col and label_col in df.columns:
            self.label_encoder.fit(df[label_col].astype(str))

        self.is_fitted = True
        return self

    def transform_dataframe(self, df: pd.DataFrame) -> np.ndarray:
        """Transforms an entire DataFrame for batch evaluation or training."""
        if not self.is_fitted:
            raise RuntimeError("Preprocessor must be fitted before calling transform_dataframe.")
        cleaned_df = self._clean_dataframe(df)
        X = cleaned_df[self.feature_names].values
        return self.scaler.transform(X)

    def transform_single(self, flow: Dict[str, Any]) -> np.ndarray:
        """
        Transforms a single raw flow dictionary for online microsecond inference.
        Ensures identical feature ordering, replaces NaNs/Infs, and applies fitted scaler.
        """
        if not self.is_fitted:
            raise RuntimeError("Preprocessor must be fitted before calling transform_single.")
        
        row = []
        for feat in self.feature_names:
            val = flow.get(feat)
            if val is None or np.isnan(val) or np.isinf(val):
                val = self.feature_medians.get(feat, 0.0)
            else:
                try:
                    val = float(val)
                    if np.isneginf(val):
                        val = 0.0
                    elif np.isposinf(val):
                        val = 1e8
                except (ValueError, TypeError):
                    val = self.feature_medians.get(feat, 0.0)
            row.append(val)

        arr = np.array(row, dtype=np.float32).reshape(1, -1)
        return self.scaler.transform(arr)

    def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardizes column names, fills missing columns, and clamps extreme values."""
        df_copy = df.copy()
        
        # Ensure all required features exist
        for col in self.feature_names:
            if col not in df_copy.columns:
                df_copy[col] = 0.0
            else:
                df_copy[col] = pd.to_numeric(df_copy[col], errors="coerce")

        # Replace Infs and NaNs
        df_copy[self.feature_names] = df_copy[self.feature_names].replace([np.inf, -np.inf], np.nan)
        df_copy[self.feature_names] = df_copy[self.feature_names].fillna(0.0)
        
        return df_copy

    def save(self, filepath: str):
        """Serializes fitted pipeline to disk."""
        data = {
            "scaler": self.scaler,
            "label_encoder": self.label_encoder,
            "feature_names": self.feature_names,
            "feature_medians": self.feature_medians,
            "is_fitted": self.is_fitted
        }
        joblib.dump(data, filepath)

    @classmethod
    def load(cls, filepath: str) -> "Preprocessor":
        """Loads fitted pipeline from disk."""
        data = joblib.load(filepath)
        instance = cls()
        instance.scaler = data["scaler"]
        instance.label_encoder = data["label_encoder"]
        instance.feature_names = data["feature_names"]
        instance.feature_medians = data["feature_medians"]
        instance.is_fitted = data["is_fitted"]
        return instance
