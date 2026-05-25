import sys
import os

# Ensure mecademic_demo_app is in the Python path for standalone execution
app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'mecademic_demo_app'))
if app_path not in sys.path:
    sys.path.insert(0, app_path)

from devices import Device
from typing import Dict


def home(devices: Dict[str, Device]):
    """
    Template logic for HOME task.
    This function is called when the Initialize/Home action is triggered.
    
    Args:
        devices: A dictionary mapping device names to their Device instances.
                 You can interact with the devices via `devices['device_name']`.
    """
    screwdriver = devices["screwdriver"]
    dispenser = devices["dispenser"]
    scara = devices["scara"]
    tester = devices["tester"]

    zaber = devices["zaber"]

    screwdriver.api.SetJointVel(20)
    dispenser.api.SetJointVel(5)
    scara.api.SetJointVel(10)
    tester.api.SetJointVel(30)

    # Move all stations to known home/posture presets.
    screwdriver.api.MoveJoints(2.59797, -47.59947, 64.63894, 90.76178, 87.51615, -107.05599)
    dispenser.api.MoveJoints(0, -60, 60, 0, 30, -45)
    scara.api.MoveJoints(-140, 90, -40, 0)
    tester.api.MoveJoints(0, -60, 0, 0, 90, 0)

    zaber.move_axis(0)

    # Block until every robot completes its move.
    screwdriver.api.WaitIdle()
    dispenser.api.WaitIdle()
    scara.api.WaitIdle()
    tester.api.WaitIdle()

    return

if __name__ == '__main__':
    import os
    import logging
    from core.ApplicationController import ApplicationController

    logging.basicConfig(level=logging.INFO)
    print("Running standalone test for home...")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "config.yaml")

    # Load actual device configurations
    app_ctrl = ApplicationController(config_path=config_path)

    try:
        # Optional: uncomment to actually communicate with hardware
        app_ctrl.initialize()

        home(app_ctrl.devices)
    finally:
        app_ctrl.shutdown()

    print("Test completed successfully.")
