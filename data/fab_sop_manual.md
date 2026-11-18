# Fab Standard Operating Procedure (SOP): Plasma Etch & CVD Yield Troubleshooting Manual

## 1. RF Power & Plasma Impedance Subsystem
### Sensor_103 (RF Matching Network Phase Angle Offset)
* **Normal Target (Median):** `-0.010` | **Safe SPC Bounds:** `[-0.016, -0.004]`
* **Physical Root Cause:** Drift outside `[-0.016, -0.004]` indicates variable capacitor wear in the 13.56 MHz RF matchbox or polymer buildup on the chamber liner shifting plasma impedance.
* **Corrective Action:** Retune RF matchbox home position toward `-0.010` and inspect chamber wall conditioning.

### Sensor_59 (Reflected RF Power Ratio)
* **Normal Target (Median):** `0.731` | **Safe SPC Bounds:** `[-14.995, 16.457]` (Optimal: `0.000` to `3.000`)
* **Physical Root Cause:** High positive spikes (`>16.457`) indicate plasma instability, arcing, or electrostatic chuck (ESC) dielectric degradation.
* **Corrective Action:** Reduce reflected power ratio toward `0.731` by adjusting forward RF bias tuning and verifying ESC helium backside cooling seal.

### Sensor_319 (Top Electrode Bias Voltage Drift)
* **Normal Target (Median):** `8.382` | **Safe SPC Bounds:** `[4.232, 12.532]`
* **Physical Root Cause:** Drift indicates focus ring erosion altering sheath voltage across the wafer edge.
* **Corrective Action:** Adjust bias compensation toward `8.382` and schedule focus ring thickness measurement.

---

## 2. Chamber Pressure & Vacuum Exhaust Subsystem
### Sensor_33 (Throttle Valve Position / Chamber Pressure Control)
* **Normal Target (Median):** `8.765` | **Safe SPC Bounds:** `[5.753, 11.777]`
* **Physical Root Cause:** Deviations indicate exhaust line foreline buildup or butterfly throttle valve hysteresis causing etch rate non-uniformity.
* **Corrective Action:** Recalibrate throttle valve PID setpoint toward `8.765` and check turbo pump backing pressure.

### Sensor_21 (Foreline Base Vacuum Pressure Sensor)
* **Normal Target (Median):** `-5533.875` | **Safe SPC Bounds:** `[-6703.457, -4364.293]`
* **Physical Root Cause:** Shift toward higher pressure (`>-4364.293`) indicates a micro-leak at the load-lock slit valve O-ring or moisture outgassing.
* **Corrective Action:** Restore base vacuum offset toward `-5533.875` via extended chamber pump-down and leak-rate check.

### Sensor_81 (Chamber Differential Manometer Drift)
* **Normal Target (Median):** `-0.019` | **Safe SPC Bounds:** `[-0.057, 0.019]`
* **Physical Root Cause:** Baratron capacitance manometer zero-drift caused by thermal cycling.
* **Corrective Action:** Perform manometer zero-calibration at base vacuum to center reading at `-0.019`.

---

## 3. Mass Flow Controller (MFC) & Gas Delivery Subsystem
### Sensor_477 (Fluorocarbon Etchant Gas Flow Ratio)
* **Normal Target (Median):** `5.220` | **Safe SPC Bounds:** `[-3.172, 13.612]` (Optimal: `3.000` to `7.500`)
* **Physical Root Cause:** MFC thermal sensor drift causing polymer-to-etchant imbalance and sidewall taper defects.
* **Corrective Action:** Adjust MFC gas flow ratio setpoint toward `5.220`.

### Sensor_577 (Diluent Argon Purge Flow Stability)
* **Normal Target (Median):** `13.898` | **Safe SPC Bounds:** `[-14.294, 42.090]` (Optimal: `8.000` to `20.000`)
* **Physical Root Cause:** Gas line pressure regulator oscillation affecting plasma density uniformity.
* **Corrective Action:** Stabilize Argon purge flow toward `13.898`.

### Sensor_31 (Showerhead Gas Distribution Pressure)
* **Normal Target (Median):** `3.431` | **Safe SPC Bounds:** `[2.345, 4.517]`
* **Physical Root Cause:** Clogged showerhead gas injection holes causing center-to-edge etch rate skew.
* **Corrective Action:** Adjust manifold pressure toward `3.431` and flag showerhead for preventive wet clean.

### Sensor_213 (Endpoint Optical Emission Spectroscopy Ratio)
* **Normal Target (Median):** `0.058` | **Safe SPC Bounds:** `[-0.106, 0.222]`
* **Physical Root Cause:** Over-etch or under-etch timing error due to OES viewport window clouding.
* **Corrective Action:** Recalibrate endpoint trigger threshold toward `0.058`.
