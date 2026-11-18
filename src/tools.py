import os
from typing import Dict
import joblib
import numpy as np
from pydantic import BaseModel, Field
from langchain_core.tools import tool

# Resolve paths relative to repository root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUNDLE_PATH = os.path.join(BASE_DIR, "models", "secom_yield_bundle.joblib")
SOP_PATH = os.path.join(BASE_DIR, "data", "fab_sop_manual.md")

# Load trained ML artifacts once at module startup
bundle = joblib.load(BUNDLE_PATH)
model = bundle["model"]
explainer = bundle["explainer"]
X_test = bundle["X_test_clean"]

# Hard SPC safety bounds (median +/- 2*std from training baseline)
SPC_LIMITS = {
    "Sensor_103": (-0.016, -0.004),
    "Sensor_33": (5.753, 11.777),
    "Sensor_59": (-14.995, 16.457),
    "Sensor_477": (-3.172, 13.612),
    "Sensor_319": (4.232, 12.532),
    "Sensor_81": (-0.057, 0.019),
    "Sensor_577": (-14.294, 42.090),
    "Sensor_31": (2.345, 4.517),
    "Sensor_21": (-6703.457, -4364.293),
    "Sensor_213": (-0.106, 0.222),
}


class RecipeFixInput(BaseModel):
    wafer_id: int = Field(description="The integer ID of the wafer in the test dataset.")
    adjustments: Dict[str, float] = Field(
        description="Dictionary mapping sensor names (e.g. 'Sensor_103') to proposed new numeric values."
    )


@tool
def inspect_wafer(wafer_id: int) -> dict:
    """Runs the XGBoost yield model and SHAP explainer on a wafer to get its failure probability and top 3 anomalous sensors."""
    if wafer_id not in X_test.index:
        return {"error": f"Wafer ID {wafer_id} not found in test dataset."}

    row = X_test.loc[[wafer_id]]
    fail_prob = float(model.predict_proba(row)[0, 1])
    shap_vals = explainer.shap_values(row)[0]

    top_indices = np.argsort(shap_vals)[::-1][:3]
    top_sensors = []
    for idx in top_indices:
        col = X_test.columns[idx]
        top_sensors.append({
            "sensor": col,
            "current_value": round(float(row.iloc[0, idx]), 4),
            "shap_impact": round(float(shap_vals[idx]), 4),
        })

    return {
        "wafer_id": wafer_id,
        "status": "FAIL" if fail_prob >= 0.20 else "PASS",
        "fail_probability": round(fail_prob, 4),
        "top_3_sensors": top_sensors,
    }


@tool
def lookup_sop_rules(sensor_or_symptom: str) -> str:
    """Searches the Fab SOP Troubleshooting Manual for physical root causes, normal targets, and safe SPC limits."""
    with open(SOP_PATH, "r", encoding="utf-8") as f:
        manual_text = f.read()

    sections = manual_text.split("### ")
    matches = [s for s in sections if sensor_or_symptom.lower() in s.lower()]

    if not matches:
        return f"No specific SOP section matched '{sensor_or_symptom}'. Check top sensor names like Sensor_103, Sensor_33, or Sensor_59."

    return "\n\n---\n\n".join(["### " + m.strip() for m in matches])


@tool(args_schema=RecipeFixInput)
def simulate_recipe_fix(wafer_id: int, adjustments: Dict[str, float]) -> dict:
    """Validates proposed sensor adjustments against SPC guardrails and re-runs XGBoost to check if failure probability drops below 20%."""
    if wafer_id not in X_test.index:
        return {"error": f"Wafer ID {wafer_id} not found."}

    # 1. Enforce deterministic SPC guardrails before running model
    violations = []
    for sensor, new_val in adjustments.items():
        if sensor not in X_test.columns:
            violations.append(f"{sensor} is not a valid active sensor.")
        elif sensor in SPC_LIMITS:
            low, high = SPC_LIMITS[sensor]
            if not (low <= new_val <= high):
                violations.append(
                    f"GUARDRAIL BLOCKED: {sensor}={new_val} violates safe SPC bounds [{low}, {high}]."
                )

    if violations:
        return {
            "approved_for_simulation": False,
            "guardrail_violations": violations,
        }

    # 2. Apply adjustments on a copy of the wafer row and re-score
    modified_row = X_test.loc[[wafer_id]].copy()
    for sensor, new_val in adjustments.items():
        modified_row[sensor] = new_val

    new_fail_prob = float(model.predict_proba(modified_row)[0, 1])
    return {
        "approved_for_simulation": True,
        "wafer_id": wafer_id,
        "applied_adjustments": adjustments,
        "new_fail_probability": round(new_fail_prob, 4),
        "recovered_to_pass": new_fail_prob < 0.20,
    }
