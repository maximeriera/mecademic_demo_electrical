# Mecademic Demo Template

This directory contains template configurations and task scripts for the Mecademic Demo Application.

## Contents

- **`config.yaml`**: The main configuration file for the application, where devices and overall settings are defined.
- **`production_context.yaml`**: Context variables, state parameters, and definitions used during production runs.
- **Task Scripts** (`calib.py`, `home.py`, `prod.py`, `shipment.py`): Python scripts defining specific routines and routines to be executed by the Application Controller.

## Usage

Use this directory as a template or reference when creating your own workspace configurations for the Mecademic application. When launching the app, you can specify your workspace directory using the `--workspace` flag.

For example:
```bash
python app.py --workspace ./mecademic_demo_template/
```
