"""HOME task — bring the Electrical assembly demo to its start position.

Runs from the HOME button, and automatically before the first PROD cycle and
after a graceful STOP. INITIALIZE already activated and homed every robot and
the Zaber axis, so this only moves to the cell's own start poses.
An exception here faults the cell.
"""

from typing import Dict

from core import AppContext
from devices import Device

from prod import (DISPENSER_REST_JOINTS, SCREWDRIVER_REST_JOINTS, TESTER_REST_JOINTS,
                  move_axis, wait_all_robots)

# Joint velocity of each robot while homing, percent.
HOME_JOINT_VEL = {"screwdriver": 20, "dispenser": 5, "scara": 10, "tester": 30}

SCARA_HOME_JOINTS = (-140, 90, -40, 0)
AXIS_HOME_MM = 0


def home(devices: Dict[str, Device], context: AppContext):
    """Move every robot to its rest pose and the axis to 0, all at once."""
    timeout = float(context.get_param("program_timeout_s", 120))

    with context.step("Move stations to home"):
        for name, vel in HOME_JOINT_VEL.items():
            devices[name].api.SetJointVel(vel)

        devices["screwdriver"].api.MoveJoints(*SCREWDRIVER_REST_JOINTS)
        devices["dispenser"].api.MoveJoints(*DISPENSER_REST_JOINTS)
        devices["scara"].api.MoveJoints(*SCARA_HOME_JOINTS)
        devices["tester"].api.MoveJoints(*TESTER_REST_JOINTS)

        move_axis(devices, context, AXIS_HOME_MM)       # blocks; the robots move meanwhile
        wait_all_robots(devices, timeout)
