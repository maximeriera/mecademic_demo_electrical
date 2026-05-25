# Mecademic Demo Electrical Workspace

This workspace contains configuration files and task scripts used by the Mecademic demo application for an electrical assembly flow.

## Workspace Layout

- `config.yaml`: Main application and device configuration.
- `production_context.yaml`: Persistent variables used during production cycles.
- `calib.py`: Calibration task entry point.
- `home.py`: Initialize/home routine for all stations.
- `prod.py`: Main production cycle logic.
- `shipment.py`: Shipment/safe posture routine.
- `backups/`: Backup configuration files.

## Task Overview

- Calibration (`calib.py`): Placeholder calibration routine (safe template hook).
- Home (`home.py`): Moves robots and axis to known startup positions.
- Production (`prod.py`): Runs screwing, glue dispensing, screen place/test/pick sequence and updates `part_count` in context.
- Shipment (`shipment.py`): Moves robots to shipment-safe positions.

## Running With The Main App

Start the main app and point it to this workspace directory:

```bash
python app.py --workspace ./mecademic_demo_electrical/
```

## Running Task Scripts Standalone

Each task script can be executed directly for validation (it loads `config.yaml` from this folder):

```bash
python calib.py
python home.py
python prod.py
python shipment.py
```

Note: standalone runs call `app_ctrl.initialize()` and may communicate with real hardware depending on your connected setup.
