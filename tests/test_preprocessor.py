import pytest
import os
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath("."))
from ml.pipeline.preprocessor import Preprocessor, NUMERIC_FEATURES
from producer.replay_traffic import TrafficGenerator

def test_preprocessor_fit_transform():
    # Generate small DataFrame
    flows = [TrafficGenerator.generate_flow() for _ in range(50)]
    df = pd.DataFrame(flows)

    prep = Preprocessor()
    prep.fit(df, label_col="true_label")

    assert prep.is_fitted is True
    assert len(prep.feature_names) == len(NUMERIC_FEATURES)

    # Test batch transform
    X_batch = prep.transform_dataframe(df)
    assert X_batch.shape == (50, len(NUMERIC_FEATURES))
    assert not np.isnan(X_batch).any()

    # Test single flow transform
    sample_flow = flows[0]
    X_single = prep.transform_single(sample_flow)
    assert X_single.shape == (1, len(NUMERIC_FEATURES))
    assert not np.isnan(X_single).any()

    # Test resilience against missing or NaN values in runtime flow
    corrupted_flow = sample_flow.copy()
    corrupted_flow["flow_duration"] = None
    corrupted_flow["flow_byts_s"] = np.nan
    del corrupted_flow["fwd_pkt_len_mean"]

    X_corrupted = prep.transform_single(corrupted_flow)
    assert X_corrupted.shape == (1, len(NUMERIC_FEATURES))
    assert not np.isnan(X_corrupted).any()
