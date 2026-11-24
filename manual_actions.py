"""Manual actions of the Electrical assembly demo — the buttons of the Manual tab.

Each key returned by :func:`get_manual_actions` must also be listed under
``manual_actions:`` in config.yaml (label, description, confirmation text),
and every key listed there must be returned here, or the app refuses to
start the workspace.

A manual action runs as an exclusive task, like HOME, so the cell must be
READY. It is the only kind of task allowed while a device is released.
An exception here faults the cell.

Reuse: each action runs one station of the production cycle with the same
functions PROD uses (prod.py), at production speeds, and waits for every
robot before it ends.
"""

from __future__ import annotations

from typing import Dict

from core import AppContext
from devices import Device

from prod import apply_production_speeds, dispense_glue, screw_parts, test_screen, wait_all_robots


def screw_parts_action(devices: Dict[str, Device], context: AppContext):
    """Run the screwing station on its own."""
    apply_production_speeds(devices, context)
    with context.step("Screw parts"):
        screw_parts(devices, context)
        wait_all_robots(devices, float(context.get_param("program_timeout_s", 120)))


def dispense_glue_action(devices: Dict[str, Device], context: AppContext):
    """Run the dispensing station on its own."""
    apply_production_speeds(devices, context)
    with context.step("Dispense glue"):
        dispense_glue(devices, context)
        wait_all_robots(devices, float(context.get_param("program_timeout_s", 120)))


def test_screen_action(devices: Dict[str, Device], context: AppContext):
    """Run the screen test station on its own."""
    apply_production_speeds(devices, context)
    with context.step("Test screen"):
        test_screen(devices, context)
        wait_all_robots(devices, float(context.get_param("program_timeout_s", 120)))


def get_manual_actions():
    """Keys must match the ``key:`` entries under ``manual_actions:`` in config.yaml."""
    return {
        "screw_parts": screw_parts_action,
        "dispense_glue": dispense_glue_action,
        "test_screen": test_screen_action,
    }
