import sys
import os
import time

# Ensure mecademic_demo_app is in the Python path for standalone execution
app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'mecademic_demo_app'))
if app_path not in sys.path:
    sys.path.insert(0, app_path)

from devices import Device
from typing import Dict


def calib(devices: Dict[str, Device]):
    """
    Template logic for CALIBRATION task.
    This function is called for calibration routines.
    
    Args:
        devices: A dictionary mapping device names to their Device instances.
    """
    # Placeholder calibration routine to keep task contract valid.
    time.sleep(1)  # Simulate time taken for calibration
    return

if __name__ == '__main__':
    import os
    import logging
    from core.ApplicationController import ApplicationController

    logging.basicConfig(level=logging.INFO)
    print("Running standalone test for calib...")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "config.yaml")

    # Load actual device configurations
    app_ctrl = ApplicationController(config_path=config_path)

    try:
        # Optional: uncomment to actually communicate with hardware
        app_ctrl.initialize()

        calib(app_ctrl.devices)
    finally:
        app_ctrl.shutdown()

    print("Test completed successfully.")
