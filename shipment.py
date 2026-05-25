import sys
import os
import time

# Ensure mecademic_demo_app is in the Python path for standalone execution
app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'mecademic_demo_app'))
if app_path not in sys.path:
    sys.path.insert(0, app_path)

from devices import Device
from typing import Dict

def shipment(devices: Dict[str, Device]):
    """
    Template logic for SHIPMENT task.
    This function is called when a shipment action is triggered.
    
    Args:
        devices: A dictionary mapping device names to their Device instances.
    """
    JOINT_VEL = 15

    screwdriver = devices["screwdriver"]
    dispenser = devices["dispenser"]
    scara = devices["scara"]
    tester = devices["tester"]

    zaber = devices["zaber"]

    screwdriver.api.SetJointVel(100)
    dispenser.api.SetJointVel(5)
    scara.api.SetJointVel(10)
    tester.api.SetJointVel(30)

    screwdriver.api.MoveJoints(0, 10, 70, 90, 115, -164.75)
    dispenser.api.MoveJoints(0, -65, 65, 0, 30, -45)
    scara.api.MoveJoints(-140, 145, -60, 0)
    tester.api.MoveJoints(0, -60, 60, 0, 50, 0)

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
    print("Running standalone test for shipment...")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "config.yaml")

    # Load actual device configurations
    app_ctrl = ApplicationController(config_path=config_path)

    try:
        # Optional: uncomment to actually communicate with hardware
        app_ctrl.initialize()

        shipment(app_ctrl.devices)
    finally:
        app_ctrl.shutdown()

    print("Test completed successfully.")
