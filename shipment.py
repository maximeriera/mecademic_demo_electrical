"""SHIPMENT task — fold the Electrical assembly demo into its transport pose.

Runs from the SHIPMENT button only. The Zaber axis is not moved.
An exception here faults the cell.
"""

from typing import Dict

from core import AppContext
from devices import Device

from prod import wait_all_robots

# Joint velocity of each robot while moving to shipment, percent.
SHIPMENT_JOINT_VEL = {"screwdriver": 100, "dispenser": 5, "scara": 10, "tester": 30}

SHIPMENT_JOINTS = {
    "screwdriver": (0, 10, 70, 90, 115, -164.75),
    "dispenser": (0, -65, 65, 0, 30, -45),
    "scara": (-140, 145, -60, 0),
    "tester": (0, -60, 60, 0, 50, 0),
}


def shipment(devices: Dict[str, Device], context: AppContext):
    """Move every robot to its shipment pose, all at once."""
    timeout = float(context.get_param("program_timeout_s", 120))

    with context.step("Move stations to shipment pose"):
        for name, vel in SHIPMENT_JOINT_VEL.items():
            devices[name].api.SetJointVel(vel)
        for name, joints in SHIPMENT_JOINTS.items():
            devices[name].api.MoveJoints(*joints)
        wait_all_robots(devices, timeout)
