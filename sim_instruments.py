import os
import inspect
import threading
import time
import instruments
from sim_plugin.sdl_sim_web.plugin import web_viz_bp, process_event
from instruments import (
    RoboticArm, WeighBalance, StirPlate, CappingStation,
    SolidAdditionStation, LiquidAdditionStation, SampleAnalysisStation
)

def trigger_event(instrument_name, method_name, *args, **kwargs):
    """Trigger an internal server event about an instrument action."""
    try:
        process_event({
            "instrument": instrument_name,
            "action": method_name,
            "args": list(args),
            "kwargs": kwargs
        })
    except Exception as e:
        import traceback
        traceback.print_exc()

class SimRoboticArm(RoboticArm):
    def pick_up_vial_from_tray(self, vial_number):
        if not instruments._is_held_by_arm and instruments._vial_location == 'tray':
            trigger_event("robotic_arm", "pick_up_vial_from_tray", vial_number)
        super().pick_up_vial_from_tray(vial_number)
        
    def place_vial_in_tray(self, vial_number):
        if instruments._is_held_by_arm:
            trigger_event("robotic_arm", "place_vial_in_tray", vial_number)
        super().place_vial_in_tray(vial_number)

    def pick_up_vial_on_weigh_balance(self):
        if not instruments._is_held_by_arm and instruments._vial_location == 'weigh_balance':
            trigger_event("robotic_arm", "pick_up_vial_on_weigh_balance")
        super().pick_up_vial_on_weigh_balance()

    def place_vial_on_weigh_balance(self):
        if instruments._is_held_by_arm:
            trigger_event("robotic_arm", "place_vial_on_weigh_balance")
        super().place_vial_on_weigh_balance()

    def pick_up_vial_on_stir_plate(self):
        if not instruments._is_held_by_arm and instruments._vial_location == 'stir_plate':
            trigger_event("robotic_arm", "pick_up_vial_on_stir_plate")
        super().pick_up_vial_on_stir_plate()

    def place_vial_on_stir_plate(self):
        if instruments._is_held_by_arm:
            trigger_event("robotic_arm", "place_vial_on_stir_plate")
        super().place_vial_on_stir_plate()

    def pick_up_vial_on_capping_station(self):
        if not instruments._is_held_by_arm and instruments._vial_location == 'capping_station':
            trigger_event("robotic_arm", "pick_up_vial_on_capping_station")
        super().pick_up_vial_on_capping_station()

    def place_vial_on_capping_station(self):
        if instruments._is_held_by_arm:
            trigger_event("robotic_arm", "place_vial_on_capping_station")
        super().place_vial_on_capping_station()

    def pick_up_vial_on_solid_addition_station(self):
        if not instruments._is_held_by_arm and instruments._vial_location == 'solid_addition_station':
            trigger_event("robotic_arm", "pick_up_vial_on_solid_addition_station")
        super().pick_up_vial_on_solid_addition_station()

    def place_vial_on_solid_addition_station(self):
        if instruments._is_held_by_arm:
            trigger_event("robotic_arm", "place_vial_on_solid_addition_station")
        super().place_vial_on_solid_addition_station()

    def pick_up_vial_on_liquid_addition_station(self):
        if not instruments._is_held_by_arm and instruments._vial_location == 'liquid_addition_station':
            trigger_event("robotic_arm", "pick_up_vial_on_liquid_addition_station")
        super().pick_up_vial_on_liquid_addition_station()

    def place_vial_on_liquid_addition_station(self):
        if instruments._is_held_by_arm:
            trigger_event("robotic_arm", "place_vial_on_liquid_addition_station")
        super().place_vial_on_liquid_addition_station()

    def pick_up_vial_in_analysis_station(self):
        if not instruments._is_held_by_arm and instruments._vial_location == 'analysis_station':
            trigger_event("robotic_arm", "pick_up_vial_in_analysis_station")
        super().pick_up_vial_in_analysis_station()

    def place_vial_in_analysis_station(self):
        if instruments._is_held_by_arm:
            trigger_event("robotic_arm", "place_vial_in_analysis_station")
        super().place_vial_in_analysis_station()

class SimWeighBalance(WeighBalance):
    def zero(self):
        trigger_event("weigh_balance", "zero")
        super().zero()
    def get_weight_mg(self):
        val = super().get_weight_mg()
        trigger_event("weigh_balance", "get_weight_mg", val)
        return val

class SimStirPlate(StirPlate):
    def start_stirring(self):
        trigger_event("stir_plate", "start_stirring")
        super().start_stirring()
    def stop_stirring(self):
        trigger_event("stir_plate", "stop_stirring")
        super().stop_stirring()

class SimCappingStation(CappingStation):
    def uncap_vial(self):
        if instruments._vial_location == 'capping_station' and getattr(instruments, '_cap_is_on', True):
            trigger_event("capping_station", "uncap_vial")
        super().uncap_vial()
    def cap_vial(self):
        if instruments._vial_location == 'capping_station' and not getattr(instruments, '_cap_is_on', True):
            trigger_event("capping_station", "cap_vial")
        super().cap_vial()

class SimSolidAdditionStation(SolidAdditionStation):
    def add_solid(self, mass_mg):
        if instruments._vial_location == 'solid_addition_station' and not getattr(instruments, '_cap_is_on', True):
            trigger_event("solid_addition_station", "add_solid", mass_mg)
        super().add_solid(mass_mg)

class SimLiquidAdditionStation(LiquidAdditionStation):
    def add_liquid(self, volume_ml):
        if instruments._vial_location == 'liquid_addition_station' and not getattr(instruments, '_cap_is_on', True):
            trigger_event("liquid_addition_station", "add_liquid", volume_ml)
        super().add_liquid(volume_ml)

class SimSampleAnalysisStation(SampleAnalysisStation):
    def analyze(self, input_1=None, input_2=None):
        val = super().analyze(input_1, input_2)
        if instruments._vial_location == 'analysis_station':
            trigger_event("sample_analysis_station", "analyze", val)
        return val

# Global instances for users to easily import
robotic_arm = SimRoboticArm()
weigh_balance = SimWeighBalance()
stir_plate = SimStirPlate()
capping_station = SimCappingStation()
solid_addition_station = SimSolidAdditionStation()
liquid_addition_station = SimLiquidAdditionStation()
sample_analysis_station = SimSampleAnalysisStation()

# Copy logging enabling function
import sys
import logging
def enable_logging_to_console():
    stream_handler = logging.StreamHandler(sys.stdout)
    instruments = [robotic_arm, weigh_balance, stir_plate, capping_station, 
                   solid_addition_station, liquid_addition_station, sample_analysis_station]
    for inst in instruments:
        inst.logger.addHandler(stream_handler)
        inst.logger.setLevel(logging.INFO)

last_synced_state = None
def state_monitor():
    global last_synced_state
    while True:
        current_state = {
            "vial_location": instruments._vial_location,
            "is_held_by_arm": instruments._is_held_by_arm,
            "solid_added": instruments._solid_added_mg,
            "liquid_added": instruments._liquid_added_ml,
            "cap_is_on": getattr(instruments, "_cap_is_on", True),
            "current_vial": instruments._current_vial_number,
            "vial_contents": {
                str(k): v for k, v in instruments._vial_contents.items()
            },
        }
        if current_state != last_synced_state:
            last_synced_state = current_state
            trigger_event("system", "sync_state", current_state)
        time.sleep(0.1)

_monitor_thread = threading.Thread(target=state_monitor, daemon=True)
_monitor_thread.start()

if __name__ == "__main__":
    import ivoryos
    ivoryos.run(__name__, blueprint_plugins=[web_viz_bp])