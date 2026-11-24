"""CALIBRATION task — Electrical assembly demo.

Runs from the CALIBRATION button only. This cell has no calibration routine:
the task reports one step and moves nothing. The file must exist anyway:
without it the app would run the demo calib() shipped in
mecademic_demo_app/app_logic/, written for other devices.
"""

from typing import Dict

from core import AppContext
from devices import Device


def calib(devices: Dict[str, Device], context: AppContext):
    """Placeholder: nothing to calibrate on this cell."""
    with context.step("No calibration for this cell"):
        pass
