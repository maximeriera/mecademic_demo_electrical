import sys
import os

# Ensure mecademic_demo_app is in the Python path for standalone execution
app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'mecademic_demo_app'))
if app_path not in sys.path:
    sys.path.insert(0, app_path)

from devices import Device
from typing import Dict
from core.ProductionContext import ProductionContext


def everyone_wait(screwdriver, dispenser, scara, tester):
    screwdriver.api.WaitIdle()
    dispenser.api.WaitIdle()
    scara.api.WaitIdle()
    tester.api.WaitIdle()


def dispensing_glue(dispenser):
    dispenser.api.MovePose(93.00003, 74.64999, 165.54995,
                      113.81136, 3.12123, -135.76364)
    dispenser.api.SetBlending(0)
    # Keep the loop shape for easy extension to multiple glue passes.
    for _ in range(1):
        dispenser.api.MoveLin(93.00002, 74.64999, 129.74996,
                          113.81135, 3.12122, -135.76365)
        dispenser.api.SetBlending(100)
        dispenser.api.MoveLin(200.30003, 74.65, 129.74995,
                          113.81136, 3.12123, -135.76366)
        dispenser.api.MoveLin(203.50002, 72.5002, 129.74994,
                          113.81136, 3.12123, -135.76366)
        dispenser.api.MoveLin(205.50002, 69.15002, 129.74994,
                          113.81136, 3.12123, -135.76366)
        dispenser.api.MoveLin(205.50002, 27.30003, 129.74994,
                          113.81137, 3.12123, -135.76367)
        dispenser.api.MoveLin(203.50002, 24.30003, 129.74994,
                          113.81137, 3.12123, -135.76367)
        dispenser.api.MoveLin(199.65002, 21.10003, 129.74993,
                          113.81137, 3.12123, -135.76369)
        dispenser.api.MoveLin(93.25002, 21.10003, 129.74993,
                          113.81138, 3.12123, -135.76368)
        dispenser.api.MoveLin(91.25002, 23.50003, 129.74993,
                          113.81138, 3.12123, -135.76368)
        dispenser.api.MoveLin(85, 24.00005, 129.7499,
                          113.81139, 3.12122, -135.7637)
        dispenser.api.MoveLin(85, 70.75004, 129.74989,
                          113.81139, 3.12122, -135.76369)
        dispenser.api.MoveLin(91.00002, 73.64999, 129.74996,
                          113.81135, 3.12122, -135.76365)
        dispenser.api.MoveLin(93.00002, 74.64999, 129.74996,
                          113.81135, 3.12122, -135.76365)
    dispenser.api.SetBlending(100)
    dispenser.api.MoveLin(93.00003, 74.64999, 165.54995,
                      113.81136, 3.12123, -135.76364)


def test_pattern(tester):
    '''
    #note: these are the positions on the screen, no app or ret
    bottom_right = tester.MoveLin(177, 69.5, 127, 180, 0, -180)
    bottom_left = tester.MoveLin(226, 69.5, 127, 180, 0, 180)
    top_left = tester.MoveLin(226, -20.5, 127, -180, 0, 180)
    top_right = tester.MoveLin(177, -20.5, 127, -180, 0, 180)
    '''
    # approach middle
    tester.api.MovePose(205, 19, 140, -180, 0, 180)
    tester.api.SetBlending(0)
    '''
    # Testing corners
    tester.MoveLin(177, 69.5, 135, 180, 0, 180)
    tester.MoveLin(177, 69.5, 127, 180, 0, -180)
    tester.MoveLin(177, 69.5, 135, 180, 0, 180)
    tester.MoveLin(226, 69.5, 135, 180, 0, 180)
    tester.MoveLin(226, 69.5, 127, 180, 0, 180)
    tester.MoveLin(226, 69.5, 135, 180, 0, 180)
    tester.MoveLin(226, -20.5, 135, -180, 0, 180)
    tester.MoveLin(226, -20.5, 127, -180, 0, 180)
    tester.MoveLin(226, -20.5, 135, -180, 0, 180)
    tester.MoveLin(177, -20.5, 135, -180, 0, 180)
    tester.MoveLin(177, -20.5, 127, -180, 0, 180)
    tester.MoveLin(177, -20.5, 135, -180, 0, 180)
    tester.MoveLin(177+(49/2), -20.5+45, 135, -180, 0, 180)
    tester.MoveLin(177+(49/2), -20.5+45, 127, -180, 0, 180)
    tester.MoveLin(177+(49/2), -20.5+45, 135, -180, 0, 180) 
    '''
    # Testing buttons
    for _ in range(3):
        tester.api.MoveLin(202.7, -27.9, 135, -180, 0, -180)
        tester.api.MoveLin(202.7, -27.9, 126, -180, 0, -180)
        tester.api.Delay(0.5)
        tester.api.MoveLin(202.7, -27.9, 135, -180, 0, -180)
    x = 0
    tester.api.MoveLin(226, -20.5, 135, -180, 0, 180)
    for i in range(8):
        if i % 2 == 1:  # impair
            tester.api.MoveLin(226-x, 69.5, 127, 180, 0, 180)
            tester.api.MoveLin(226-x, -20.5, 127, -180, 0, 180)
        if i % 2 == 0:  # pair
            tester.api.MoveLin(226-x, -20.5, 127, -180, 0, 180)
            tester.api.MoveLin(226-x, 69.5, 127, 180, 0, 180)
        x = x + 7
    tester.api.MoveLin(226-x+7, -20.5, 135, -180, 0, 180)
    y = 0
    tester.api.MoveLin(177, 69.5, 135, 180, 0, -180)
    '''
    for i in range(10):
        if i % 2 == 1:  # impair
            tester.MoveLin(226, 69.5-y, 127, 180, 0, 180)
            tester.MoveLin(177, 69.5-y, 127, 180, 0, -180)
        if i % 2 == 0:  # pair
            tester.MoveLin(177, 69.5-y, 127, 180, 0, -180)
            tester.MoveLin(226, 69.5-y, 127, 180, 0, 180)
        y = y + 10
        '''
    tester.api.MoveLin(177, 69.5-y+10, 135, 180, 0, -180)
    tester.api.SetBlending(100)
    tester.api.MoveJoints(0, -60, 0, 0, 90, 0)


def prod_cycle(devices: Dict[str, Device], context: ProductionContext = None):
    """
    Template logic for PROD task.
    This function is executed cyclically while the PROD task is running.

    Parameters
    ----------
    devices : Dict[str, Device]
        Configured device objects.
    context : ProductionContext | None
        Shared production context for params/variables persistence across cycles.
    """
    LIN_SPEED = 1000
    JOINT_SPEED = 100
    DISPENSING_LIN_SPEED = 100
    CART_ACC = 30

    ZABER_SCREW_POS = 0
    ZABER_DISPENSER_POS = 180
    ZABER_SCARA_POS = 400
    ZABER_TEST_POS = 450
    
    screwdriver = devices["screwdriver"]
    dispenser = devices["dispenser"]
    scara = devices["scara"]
    tester = devices["tester"]

    zaber = devices["zaber"]

    # Configure motion profiles for each robot station.
    screwdriver.api.SetJointVel(JOINT_SPEED)
    screwdriver.api.SetCartLinVel(LIN_SPEED)
    screwdriver.api.SetCartAcc(CART_ACC)
    
    dispenser.api.SetJointVel(JOINT_SPEED)
    dispenser.api.SetCartLinVel(DISPENSING_LIN_SPEED)
    dispenser.api.SetCartAcc(CART_ACC)
    
    scara.api.SetJointVel(JOINT_SPEED)
    scara.api.SetCartLinVel(LIN_SPEED)
    scara.api.SetCartAcc(CART_ACC)
    
    tester.api.SetJointVel(JOINT_SPEED)
    tester.api.SetCartLinVel(LIN_SPEED)
    tester.api.SetCartAcc(CART_ACC)

    # Sequence: screw -> dispense -> place -> test -> remove screen.
    zaber.move_axis(ZABER_SCREW_POS)
    screwdriver.api.StartProgram("screwing_seq")

    everyone_wait(screwdriver, dispenser, scara, tester)

    screwdriver.api.SetWrf(49, 137, 478.5, 180, 0, -90)
    screwdriver.api.MoveLin(0, 0, 10, 180, 0, 0)
    screwdriver.api.MoveJoints(2.59797, -47.59947, 64.63894, 90.76177, 87.51615, -107.05599)

    # if stoped_check():
    #     return

    zaber.move_axis(ZABER_DISPENSER_POS)

    dispensing_glue(dispenser)
    everyone_wait(screwdriver, dispenser, scara, tester)
    dispenser.api.MoveJoints(0, -60, 60, 0, 30, -45)

    # if stoped_check():
    #     everyone_wait(screwdriver, dispenser, scara, tester)
    #     return

    zaber.move_axis(ZABER_SCARA_POS)
    scara.api.StartProgram("place_screen")
    everyone_wait(screwdriver, dispenser, scara, tester)

    zaber.move_axis(ZABER_TEST_POS)
    test_pattern(tester)
    everyone_wait(screwdriver, dispenser, scara, tester)

    zaber.move_axis(ZABER_SCARA_POS)
    scara.api.StartProgram("pick_screen")
    everyone_wait(screwdriver, dispenser, scara, tester)

    part_count = context.get_variable("part_count", 0) if context else 0

    if context:
        context.set_variable("part_count", part_count + 1, force=True)
    return

if __name__ == '__main__':
    import os
    from core.ApplicationController import ApplicationController

    print("Running standalone test for prod_cycle...")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "config.yaml")
    context_path = os.path.join(script_dir, "production_context.yaml")

    # 1. Initialize ApplicationController to parse real configs and create device objects
    app_ctrl = ApplicationController(
        config_path=config_path,
        production_context_path=context_path
    )

    try:
        # Optional: uncomment to actually communicate with hardware
        app_ctrl.initialize()

        # Execute the cycle using the loaded devices and production context
        prod_cycle(app_ctrl.devices, context=app_ctrl.production_context)
        
    finally:
        # Ensure to cleanly shut down any background thread created by the controller
        app_ctrl.shutdown()

    print("prod_cycle executed successfully.")

