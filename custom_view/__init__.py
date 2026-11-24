"""Custom view — line overview of the Electrical assembly demo, at /view/.

The controller calls :func:`setup` at every INITIALIZE, then starts the hub.
The page (``index.html``) shows:

* the line: the Zaber rail with the four stations at their axis positions and
  the carriage moving to the axis target (channel ``axis``, published by
  ``prod.move_axis`` from the task thread);
* one card per robot with its link, activation, homing and error state
  (channel ``robots``, sampled here), highlighted while its step runs (the
  live step comes from ``/api/status``);
* part count (``/api/context``) and the time of every completed cycle
  (channel ``cycle_time_s``, from the framework's ``cycle_end`` event).

Delete this folder and the app runs exactly as before, without the view link.
"""

from devices.SimulatedDevice import SimulatedDevice

from prod import AXIS_DISPENSE_MM, AXIS_SCARA_MM, AXIS_SCREW_MM, AXIS_TEST_MM, ROBOTS

#: Robot status is shown to the operator, not plotted: 2 Hz is plenty.
ROBOT_STATE_RATE_HZ = 2

#: Stations along the rail, in axis order: the page draws them from this.
#: `steps` are the context.step() names during which the station is busy.
STATIONS = [
    {"key": "screwdriver", "label": "Screwing", "model": "Meca500", "axis_mm": AXIS_SCREW_MM,
     "steps": ["Screw parts"]},
    {"key": "dispenser", "label": "Glue dispensing", "model": "Meca500", "axis_mm": AXIS_DISPENSE_MM,
     "steps": ["Dispense glue"]},
    {"key": "scara", "label": "Screen place / pick", "model": "MCS500", "axis_mm": AXIS_SCARA_MM,
     "steps": ["Place screen", "Pick screen"]},
    {"key": "tester", "label": "Screen test", "model": "Meca500", "axis_mm": AXIS_TEST_MM,
     "steps": ["Test screen"]},
]

_STATE_KEYS = ("link", "activated", "homed", "paused", "error", "error_code")


def setup(hub, devices):
    """Declare the robot status source, the line layout and the cycle-time analysis."""
    missing = [name for name in ROBOTS if name not in devices]
    if missing:
        raise LookupError(f"No device {', '.join(missing)} in config.yaml: this view shows every robot.")

    def read_robots():
        return {name: _robot_state(devices[name]) for name in ROBOTS}

    hub.add_source("robots", read_robots, rate_hz=ROBOT_STATE_RATE_HZ, history_s=10)
    hub.publish("line", {"stations": STATIONS})
    hub.on("cycle_end", record_cycle_time)


def _robot_state(robot):
    """Link and status of one robot, from mecademicpy's cached data (no request to the robot)."""
    if isinstance(robot, SimulatedDevice):
        return {"link": "simulated"}
    try:
        if not robot.connected:
            return {"link": "disconnected"}
        telemetry = robot.telemetry()   # cached getters only, safe from this thread
    except Exception as error:          # one robot's link dropping must not blank the others
        return {"link": "unavailable", "message": str(error)}
    return {key: telemetry.get(key) for key in _STATE_KEYS}


def record_cycle_time(hub, event):
    """Publish the duration of the PROD cycle that just completed, seconds."""
    start_t = event.get("start_t")
    if start_t is not None:
        hub.publish("cycle_time_s", round(event["t"] - start_t, 2))
