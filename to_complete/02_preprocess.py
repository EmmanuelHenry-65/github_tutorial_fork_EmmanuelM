from __future__ import annotations

from typing import Any, Dict, List


# The garden helper predicts how much water a plot needs.
TARGET_NAME = "water_need"

# These are the columns the model learns from. We keep the raw, readable
# column names here so the training step can encode them however it likes.
FEATURE_NAMES = [
    "day_of_week",
    "weather",
    "temperature_c",
    "rainfall_mm",
    "soil_moisture",
    "crop_type",
]

# Which features are text (categorical) and which are numbers. Splitting them
# up keeps the cleaning logic simple to read.
TEXT_FEATURES = ["day_of_week", "weather", "crop_type"]
NUMERIC_FEATURES = ["temperature_c", "rainfall_mm", "soil_moisture"]

# Sensible fallbacks used only when a value is missing. Numbers fall back to a
# neutral middle value; text falls back to "unknown".
NUMERIC_DEFAULTS = {
    "temperature_c": 25.0,
    "rainfall_mm": 0.0,
    "soil_moisture": 40.0,
}

# Fraction of the cleaned rows kept for testing. The rest are used for training.
TEST_FRACTION = 0.25


def _clean_text(value: Any) -> str:
    """Normalize a text field: strip spaces and lowercase it."""
    if value is None:
        return "unknown"
    text = str(value).strip().lower()
    return text if text else "unknown"


def _clean_number(value: Any, default: float) -> float:
    """Turn a value into a float, using a default when it is missing/broken."""
    if value is None:
        return float(default)
    try:
        return float(value)
    except (TypeError, ValueError):
        return float(default)


def _clean_record(record: Dict[str, Any]) -> Dict[str, Any] | None:
    """Clean one raw record into a tidy training row.

    Returns None when the row has no usable target label, because we cannot
    train or test on a row when we do not know the answer.
    """
    target = _clean_text(record.get(TARGET_NAME))
    if target == "unknown":
        return None

    row: Dict[str, Any] = {}
    for name in TEXT_FEATURES:
        row[name] = _clean_text(record.get(name))
    for name in NUMERIC_FEATURES:
        row[name] = _clean_number(record.get(name), NUMERIC_DEFAULTS[name])
    row[TARGET_NAME] = target
    return row


def preprocess_event_data(raw_bundle: Dict[str, Any]) -> Dict[str, Any]:
    """
    Turn raw records into trainable data.

    Input contract:
    - raw_bundle["dataset_name"]: str
    - raw_bundle["source"]: str
    - raw_bundle["records"]: list[dict]

    Expected work:
    - clean missing values
    - normalize text fields
    - convert categories into model-friendly features
    - split the data into train and test rows

    Output contract:
    - dataset_name: str
    - feature_names: list[str]
    - target_name: str  # likely "water_need"
    - train_rows: list[dict]
    - test_rows: list[dict]
    - summary: dict
    """
    dataset_name = str(raw_bundle.get("dataset_name", "unknown_dataset"))
    records = raw_bundle.get("records") or []

    # Clean every record and drop the ones we cannot use.
    cleaned_rows: List[Dict[str, Any]] = []
    dropped = 0
    for record in records:
        if not isinstance(record, dict):
            dropped += 1
            continue
        row = _clean_record(record)
        if row is None:
            dropped += 1
            continue
        cleaned_rows.append(row)

    # Split into train and test. We take every 4th row for the test set so the
    # split is deterministic (no randomness) and reproducible for everyone.
    train_rows: List[Dict[str, Any]] = []
    test_rows: List[Dict[str, Any]] = []
    test_every = max(2, round(1 / TEST_FRACTION))  # 1/0.25 -> every 4th row
    for index, row in enumerate(cleaned_rows):
        if cleaned_rows and index % test_every == test_every - 1:
            test_rows.append(row)
        else:
            train_rows.append(row)

    # If there is enough data but the split left the test set empty (very few
    # rows), move one row over so downstream evaluation has something to score.
    if len(cleaned_rows) >= 2 and not test_rows:
        test_rows.append(train_rows.pop())

    # Count how many rows landed in each water-need class. Handy for a sanity
    # check and shown by the pipeline summary.
    label_counts: Dict[str, int] = {}
    for row in cleaned_rows:
        label = row[TARGET_NAME]
        label_counts[label] = label_counts.get(label, 0) + 1

    summary = {
        "raw_count": len(records),
        "clean_count": len(cleaned_rows),
        "dropped_count": dropped,
        "train_count": len(train_rows),
        "test_count": len(test_rows),
        "label_counts": label_counts,
    }

    return {
        "dataset_name": dataset_name,
        "feature_names": list(FEATURE_NAMES),
        "target_name": TARGET_NAME,
        "train_rows": train_rows,
        "test_rows": test_rows,
        "summary": summary,
    }
