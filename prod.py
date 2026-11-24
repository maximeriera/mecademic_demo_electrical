"""PROD task — one production cycle of the Electrical assembly demo.

The app calls ``prod_cycle(devices, context)`` in a loop while PROD runs:
home() first, then cycles until STOP, then home() again. ABORT interrupts
the cycle where it is (a robot wait raises, the Zaber axis stops) and skips
the exit home. Nothing here needs to check for STOP or ABORT.

Sequence (declared under ``sequences: prod_cycle`` in config.yaml):
  1. Screw parts      screwdriver program "screwing_seq", end checkpoint 11
  2. Dispense glue    dispenser program "iphone_dispensing", end checkpoint 11
  3. Place screen     scara program "place_screen", end checkpoint 11
  4. Test screen      tester touch pattern, driven from this file
  5. Pick screen      scara program "pick_screen", end checkpoint 12

The Zaber axis carries the part to each station before its step. The
screwdriver's retract move is sent at the end of its step and finishes while
the axis moves on; every step waits for all robots before it ends.

Robot programs and checkpoints this file relies on are listed in README.md
("Robot programs").
"""

from typing import Dict

from core import AppContext
from devices import Device

from cell_tools import run_program

# Robot programs saved on the controllers, and the checkpoint each must set on
# its last line. TODO: add SetCheckpoint(<n>) at the end of each program on the
# robot (the backups of 2026-05-25 have none).
SCREW_PROGRAM, SCREW_DONE = "screwing_seq", 11          # screwdriver
DISPENSE_PROGRAM, DISPENSE_DONE = "iphone_dispensing", 11       # dispenser
PLACE_SCREEN_PROGRAM, PLACE_SCREEN_DONE = "place_screen", 11   # scara
PICK_SCREEN_PROGRAM, PICK_SCREEN_DONE = "pick_screen", 12      # scara

# Zaber axis position of each station, mm.
AXIS_SCREW_MM = 0
AXIS_DISPENSE_MM = 180
AXIS_SCARA_MM = 400
AXIS_TEST_MM = 450

ROBOTS = ("screwdriver", "dispenser", "scara", "tester")

# Screwdriver: WRF of the first screw, the retract move in that frame, and its rest joints.
SCREW_RETRACT_WRF = (49, 137, 478.5, 180, 0, -90)
SCREW_RETRACT_POSE = (0, 0, 10, 180, 0, 0)
SCREWDRIVER_REST_JOINTS = (2.59797, -47.59947, 64.63894, 90.76177, 87.51615, -107.05599)

# Dispenser rest joints (HOME). The glue path itself lives in the robot
# program DISPENSE_PROGRAM.
DISPENSER_REST_JOINTS = (0, -60, 60, 0, 30, -45)

# Tester: touch pattern on the screen, WRF, mm / deg.
# Screen corners at touch height (z 127): bottom right (177, 69.5),
# bottom left (226, 69.5), top left (226, -20.5), top right (177, -20.5).
TEST_APPROACH = (205, 19, 140, -180, 0, 180)
TEST_BUTTON_UP = (202.7, -27.9, 135, -180, 0, -180)
TEST_BUTTON_DOWN = (202.7, -27.9, 126, -180, 0, -180)
TEST_BUTTON_PRESSES = 3
TEST_SWIPES = 8           # vertical swipes, 7 mm apart, starting at x = 226
TESTER_REST_JOINTS = (0, -60, 0, 0, 90, 0)


# --------------------------------------------------------------------------
# Shared helpers (also used by home.py, shipment.py and manual_actions.py)
# --------------------------------------------------------------------------

def wait_all_robots(devices: Dict[str, Device], timeout: float) -> None:
    """Block until every robot finished its queued moves. Raises on ABORT or timeout."""
    for name in ROBOTS:
        devices[name].api.WaitIdle(timeout=timeout)


def move_axis(devices: Dict[str, Device], context: AppContext, position_mm: float) -> None:
    """Move the Zaber axis to *position_mm* and block until it is there.

    Publishes ``axis`` ({target_mm, moving}) before and after the move, for the
    line diagram of the custom view: the Zaber driver offers no position read
    that is safe from another thread while this one blocks in the move.

    ``move_axis`` is a method of the Zaber driver, not of its ``.api``, so a
    ``type: "simulated"`` stand-in (the smoke test) doesn't have it: there is
    nothing to move then, and the call only logs.
    """
    axis = devices["zaber"]
    context.publish("axis", {"target_mm": position_mm, "moving": True})
    if not hasattr(axis, "move_axis"):
        axis.logger.info(f"[zaber] simulated: move_axis({position_mm}) skipped.")
    else:
        axis.move_axis(position_mm)
    context.publish("axis", {"target_mm": position_mm, "moving": False})


def apply_production_speeds(devices: Dict[str, Device], context: AppContext) -> None:
    """Set every robot's motion parameters from the params (HOME leaves slower ones)."""
    joint_vel = float(context.get_param("joint_vel_pct", 100))
    lin_vel = float(context.get_param("cart_lin_vel_mm_s", 1000))
    dispense_vel = float(context.get_param("dispense_lin_vel_mm_s", 100))
    acc = float(context.get_param("cart_acc_pct", 30))
    for name in ROBOTS:
        robot = devices[name].api
        robot.SetJointVel(joint_vel)
        robot.SetCartLinVel(dispense_vel if name == "dispenser" else lin_vel)
        robot.SetCartAcc(acc)


# --------------------------------------------------------------------------
# Stations — one per PROD step, shared with the manual actions
# --------------------------------------------------------------------------

def screw_parts(devices: Dict[str, Device], context: AppContext) -> None:
    """Run the screwing program, then send the screwdriver back to rest (not waited)."""
    screwdriver = devices["screwdriver"].api
    timeout = float(context.get_param("program_timeout_s", 120))

    move_axis(devices, context, AXIS_SCREW_MM)
    run_program(devices["screwdriver"], SCREW_PROGRAM, SCREW_DONE, timeout=timeout)
    wait_all_robots(devices, timeout)

    screwdriver.SetWrf(*SCREW_RETRACT_WRF)
    screwdriver.MoveLin(*SCREW_RETRACT_POSE)
    screwdriver.MoveJoints(*SCREWDRIVER_REST_JOINTS)


def dispense_glue(devices: Dict[str, Device], context: AppContext) -> None:
    """Run the dispensing program on the dispenser."""
    timeout = float(context.get_param("program_timeout_s", 120))
    move_axis(devices, context, AXIS_DISPENSE_MM)
    run_program(devices["dispenser"], DISPENSE_PROGRAM, DISPENSE_DONE, timeout=timeout)
    wait_all_robots(devices, timeout)


def place_screen(devices: Dict[str, Device], context: AppContext) -> None:
    """Place the screen on the part with the SCARA."""
    timeout = float(context.get_param("program_timeout_s", 120))
    move_axis(devices, context, AXIS_SCARA_MM)
    run_program(devices["scara"], PLACE_SCREEN_PROGRAM, PLACE_SCREEN_DONE, timeout=timeout)
    wait_all_robots(devices, timeout)


def test_screen(devices: Dict[str, Device], context: AppContext) -> None:
    """Press the button three times, then swipe across the screen."""
    tester = devices["tester"].api
    timeout = float(context.get_param("program_timeout_s", 120))

    move_axis(devices, context, AXIS_TEST_MM)
    tester.MovePose(*TEST_APPROACH)
    tester.SetBlending(0)

    for _ in range(TEST_BUTTON_PRESSES):
        tester.MoveLin(*TEST_BUTTON_UP)
        tester.MoveLin(*TEST_BUTTON_DOWN)
        tester.Delay(0.5)
        tester.MoveLin(*TEST_BUTTON_UP)

    tester.MoveLin(226, -20.5, 135, -180, 0, 180)
    x = 0
    for i in range(TEST_SWIPES):
        if i % 2 == 0:   # top to bottom
            tester.MoveLin(226 - x, -20.5, 127, -180, 0, 180)
            tester.MoveLin(226 - x, 69.5, 127, 180, 0, 180)
        else:            # bottom to top
            tester.MoveLin(226 - x, 69.5, 127, 180, 0, 180)
            tester.MoveLin(226 - x, -20.5, 127, -180, 0, 180)
        x += 7
    tester.MoveLin(226 - x + 7, -20.5, 135, -180, 0, 180)

    tester.MoveLin(177, 69.5, 135, 180, 0, -180)
    tester.MoveLin(177, 79.5, 135, 180, 0, -180)
    tester.SetBlending(100)
    tester.MoveJoints(*TESTER_REST_JOINTS)
    wait_all_robots(devices, timeout)


def pick_screen(devices: Dict[str, Device], context: AppContext) -> None:
    """Remove the screen from the part with the SCARA."""
    timeout = float(context.get_param("program_timeout_s", 120))
    move_axis(devices, context, AXIS_SCARA_MM)
    run_program(devices["scara"], PICK_SCREEN_PROGRAM, PICK_SCREEN_DONE, timeout=timeout)
    wait_all_robots(devices, timeout)


# --------------------------------------------------------------------------
# The cycle
# --------------------------------------------------------------------------

def prod_cycle(devices: Dict[str, Device], context: AppContext):
    """Screw, dispense, place the screen, test it, remove it; count the part."""
    apply_production_speeds(devices, context)

    with context.step("Screw parts"):
        screw_parts(devices, context)

    with context.step("Dispense glue"):
        dispense_glue(devices, context)

    with context.step("Place screen"):
        place_screen(devices, context)

    with context.step("Test screen"):
        test_screen(devices, context)

    with context.step("Pick screen"):
        pick_screen(devices, context)

    context.set_variable("part_count", context.get_variable("part_count", 0) + 1)
