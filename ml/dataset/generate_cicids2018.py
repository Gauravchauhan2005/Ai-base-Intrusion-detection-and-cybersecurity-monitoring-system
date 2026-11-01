import os
import sys
import pandas as pd
import numpy as np

# Ensure parent directory is accessible
sys.path.insert(0, os.path.abspath("."))
from producer.replay_traffic import TrafficGenerator

def generate_cicids2018_dataset(num_samples: int = 12000, output_csv: str = "ml/dataset/cicids2018_sample.csv"):
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    print(f"Generating {num_samples} flows simulating CICIDS2018 distribution...")

    attacks = [
        ("Benign", int(num_samples * 0.70)),
        ("DoS-Hulk", int(num_samples * 0.08)),
        ("DDoS-LOIC-HTTP", int(num_samples * 0.08)),
        ("Botnet", int(num_samples * 0.05)),
        ("SSH-Bruteforce", int(num_samples * 0.05)),
        ("Infiltration", int(num_samples * 0.04)),
    ]

    records = []
    for label, count in attacks:
        print(f"  - Generating {count} flows for {label}...")
        for _ in range(count):
            flow = TrafficGenerator.generate_flow(attack_override=label)
            records.append(flow)

    df = pd.DataFrame(records)
    # Shuffle
    df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
    df.to_csv(output_csv, index=False)
    print(f"Dataset successfully saved to {output_csv} ({len(df)} total rows).")
    print("\nClass Distribution:")
    print(df["true_label"].value_counts())

if __name__ == "__main__":
    generate_cicids2018_dataset()
