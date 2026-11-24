# Electrical assembly demo

A four-robot electrical assembly line: a Zaber linear axis carries the part from station to station, where a Meca500 screws it, a second Meca500 dispenses a glue bead, an MCS500 SCARA places a screen on it, a third Meca500 runs a touch test pattern on the screen, and the SCARA removes the screen again. One PROD cycle completes one part and adds one to `part_count`.

This folder is a workspace of the [Mecademic demo app](https://github.com/maximeriera/mecademic_demo_app): the app provides the web UI, the device drivers and the task runner; this folder provides the cell's devices (`config.yaml`), its sequences (`*.py`) and its tunable values (`context.yaml`).

## Run it

```bash
python <path to>/mecademic_demo_app/app.py --workspace <path to this folder>
```

or, on the demo box, `docker compose up -d` from `~/demo_ws` (the compose file starts the app on `/workspaces/demo_workspace`).

Open the app, press **INITIALIZE** (connects, activates and homes every robot, homes the Zaber axis), then **HOME**, then **PROD** on the Production tab. **STOP** ends after the current cycle and homes; **ABORT** stops at once.

## Devices

| Name in code | Type | Address | Role |
|---|---|---|---|
| `screwdriver` | Meca500 (`mecademic`) | 192.168.0.101 | Screws the part (program `screwing_seq`) |
| `dispenser` | Meca500 (`mecademic`) | 192.168.0.102 | Dispenses the glue bead (moves in `prod.py`) |
| `scara` | MCS500 (`mecademic`) | 192.168.0.103 | Places and removes the screen (programs `place_screen`, `pick_screen`) |
| `tester` | Meca500 (`mecademic`) | 192.168.0.104 | Touch test pattern on the screen (moves in `prod.py`) |
| `zaber` | Zaber axis (`zaber`, legacy driver) | `COM3` | Carries the part: screwing 0 mm, dispensing 180 mm, SCARA 400 mm, test 450 mm |

## Robot programs

The screwdriver and SCARA motion lives in programs saved on the controllers. Each program must end with `SetCheckpoint(<n>)`; the Python side starts it and waits for that checkpoint (see `cell_tools.py` for why `WaitIdle()` alone is not enough). **They must exist on the controller, with that last line, before PROD runs.**

| Robot | Program | Ends with | Called from |
|---|---|---|---|
| `screwdriver` | `screwing_seq` (calls `screw` once per screw) | `SetCheckpoint(11)` | `prod.py`, manual action *Screw parts* |
| `scara` | `place_screen` | `SetCheckpoint(11)` | `prod.py` |
| `scara` | `pick_screen` | `SetCheckpoint(12)` | `prod.py` |

The dispenser and tester moves are written in `prod.py`; HOME and SHIPMENT are joint moves in `home.py` and `shipment.py`.

## Sequences

| Task | Steps |
|---|---|
| PROD cycle | Screw parts → Dispense glue → Place screen → Test screen → Pick screen |
| HOME | Move stations to home (all robots to rest, axis to 0 mm) |
| SHIPMENT | Move stations to shipment pose (robots only) |
| CALIBRATION | No calibration for this cell (moves nothing) |
| Manual: *Screw parts* | Screw parts |
| Manual: *Dispense glue* | Dispense glue |
| Manual: *Test screen* | Test screen |

## Params and variables (Variables tab)

| Name | Kind | Default | Meaning |
|---|---|---|---|
| `joint_vel_pct` | param | 100 | Joint velocity of every robot in production, % |
| `cart_lin_vel_mm_s` | param | 1000 | Linear velocity of screwdriver, SCARA and tester, mm/s |
| `dispense_lin_vel_mm_s` | param | 100 | Linear velocity of the dispenser along the glue bead, mm/s |
| `cart_acc_pct` | param | 30 | Cartesian acceleration of every robot, % |
| `program_timeout_s` | param | 120 | Longest a robot program or a station's moves may take before the cell faults, s |
| `part_count` | variable | 0 | Parts completed since PROD start (kept across restarts) |

## Files

| File | Contents |
|---|---|
| `config.yaml` | Devices, manual actions, declared step sequences |
| `context.yaml` | Params and variables |
| `prod.py` | `prod_cycle()` and one function per station, shared with the other modules |
| `home.py`, `shipment.py`, `calib.py` | HOME, SHIPMENT and CALIBRATION tasks |
| `manual_actions.py` | Manual tab buttons |
| `cell_tools.py` | Start a robot program and wait for its checkpoint |
| `custom_view/` | Line overview page (`/view/`, linked from the sidebar after INITIALIZE): stations on the Zaber rail with the carriage, robot status cards highlighted while their step runs, part count and cycle times |
| `backups/` | Robot backups written by the app (programs, variables, configuration) |

## Before the next run on hardware (TODO)

- [ ] Add `SetCheckpoint(11)` as the last line of `screwing_seq` on the screwdriver, and `SetCheckpoint(11)` / `SetCheckpoint(12)` as the last lines of `place_screen` / `pick_screen` on the SCARA. Without them PROD faults after `program_timeout_s`.
- [ ] Confirm the Zaber serial port. In the Docker container it is a Linux device (e.g. `/dev/ttyUSB0`) that must also be passed to the container (`devices:` in `~/demo_ws/docker-compose.yml`).
- [ ] Check `program_timeout_s` (120 s) against the real duration of `screwing_seq`.

## Tested

- Simulated smoke test (`check_workspace.py` of the new-workspace skill): every task ran on simulated devices, 2026-11-23.
- Hardware: not yet since the migration to the current workspace format.
