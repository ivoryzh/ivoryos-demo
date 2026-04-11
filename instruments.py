"""
Example (not real) interfaces for different instruments on a SDL platform
"""

import sys
import logging
import random
import time
from typing import Optional

import numpy as np

# ----------------------------------------------------------------------------------------
# dummy variables to use track the weight of a vial as solids and liquids are added into it, to be used as the
# dummy value returned by the weigh balance
DEFAULT_VIAL_WEIGHT_MG: float = 1500.  # weight of an empty vial
_dummy_vial_weight_mg: float = DEFAULT_VIAL_WEIGHT_MG
_solid_added_mg: float = 0.0
_liquid_added_ml: float = 0.0

# ----------------------------------------------------------------------------------------
# Tracking variables for vial location and arm state
# assume only 1 vial at a time and it starts in the tray
_vial_location: Optional[str] = 'tray'
_is_held_by_arm: bool = False
_cap_is_on: bool = True
_current_vial_number: Optional[int] = None  # slot currently being processed

# Per-slot content memory (slots 1-15)
_vial_contents: dict = {
    i: {"solid_mg": 0.0, "liquid_ml": 0.0, "cap_is_on": True, "processed": False}
    for i in range(1, 16)
}


def reset_state():
    """Resets all simulation globals back to defaults."""
    global _vial_location, _is_held_by_arm, _cap_is_on, _current_vial_number
    global _vial_contents, _dummy_vial_weight_mg, _solid_added_mg, _liquid_added_ml

    _vial_location = 'tray'
    _is_held_by_arm = False
    _cap_is_on = True
    _current_vial_number = None

    _vial_contents = {
        i: {"solid_mg": 0.0, "liquid_ml": 0.0, "cap_is_on": True, "processed": False}
        for i in range(1, 16)
    }

    _dummy_vial_weight_mg = DEFAULT_VIAL_WEIGHT_MG
    _solid_added_mg = 0.0
    _liquid_added_ml = 0.0


# ----------------------------------------------------------------------------------------
class RoboticArm:
    """
    Example of a robotic arm to move things around a deck, not a real implementation
    """
    def __init__(self):
        self.logger = logging.getLogger(f'{self.__class__.__name__}')

    def pick_up_vial_from_tray(self, vial_number):
        global _vial_location, _is_held_by_arm, _current_vial_number
        if _is_held_by_arm:
            raise RuntimeError("Robotic arm is already holding a vial")
        if _vial_location != 'tray':
            raise RuntimeError(f"Vial is not in the tray, it is at: {_vial_location}")

        self.logger.info(f"Pick up vial {vial_number} from tray")
        _is_held_by_arm = True
        _vial_location = None
        _current_vial_number = int(vial_number)

        global _dummy_vial_weight_mg, _solid_added_mg, _liquid_added_ml, _cap_is_on
        _dummy_vial_weight_mg = DEFAULT_VIAL_WEIGHT_MG
        _solid_added_mg = 0.0
        _liquid_added_ml = 0.0
        _cap_is_on = True
        time.sleep(2)

    def place_vial_in_tray(self, vial_number):
        global _vial_location, _is_held_by_arm, _current_vial_number
        if not _is_held_by_arm:
            raise RuntimeError("Robotic arm is not holding a vial")

        slot = int(vial_number)
        if _current_vial_number is not None and slot != _current_vial_number:
            raise RuntimeError(
                f"Cannot place vial in slot {slot}: arm is holding vial from slot "
                f"{_current_vial_number}. Vials must be returned to their original slot."
            )

        self.logger.info(f"Place vial {vial_number} into tray")
        _vial_contents[slot] = {
            "solid_mg": _solid_added_mg,
            "liquid_ml": _liquid_added_ml,
            "cap_is_on": _cap_is_on,
            "processed": True,
        }
        _is_held_by_arm = False
        _vial_location = 'tray'
        _current_vial_number = slot
        time.sleep(2)

    def pick_up_vial_on_weigh_balance(self):
        global _vial_location, _is_held_by_arm
        if _is_held_by_arm:
            raise RuntimeError("Robotic arm is already holding a vial")
        if _vial_location != 'weigh_balance':
            raise RuntimeError(f"Vial is not on the weigh balance, it is at: {_vial_location}")

        self.logger.info(f"Pick up vial on weigh balance")
        _is_held_by_arm = True
        _vial_location = None
        time.sleep(2)

    def place_vial_on_weigh_balance(self):
        global _vial_location, _is_held_by_arm
        if not _is_held_by_arm:
            raise RuntimeError("Robotic arm is not holding a vial")

        self.logger.info(f"Place vial on weigh balance")
        _is_held_by_arm = False
        _vial_location = 'weigh_balance'
        time.sleep(2)

    def pick_up_vial_on_stir_plate(self):
        global _vial_location, _is_held_by_arm
        if _is_held_by_arm:
            raise RuntimeError("Robotic arm is already holding a vial")
        if _vial_location != 'stir_plate':
            raise RuntimeError(f"Vial is not on the stir plate, it is at: {_vial_location}")

        self.logger.info(f"Pick up vial on stir plate")
        _is_held_by_arm = True
        _vial_location = None
        time.sleep(2)

    def place_vial_on_stir_plate(self):
        global _vial_location, _is_held_by_arm
        if not _is_held_by_arm:
            raise RuntimeError("Robotic arm is not holding a vial")

        self.logger.info(f"Place vial on stir plate")
        _is_held_by_arm = False
        _vial_location = 'stir_plate'
        time.sleep(2)

    def pick_up_vial_on_capping_station(self):
        global _vial_location, _is_held_by_arm
        if _is_held_by_arm:
            raise RuntimeError("Robotic arm is already holding a vial")
        if _vial_location != 'capping_station':
            raise RuntimeError(f"Vial is not on the capping station, it is at: {_vial_location}")

        self.logger.info(f"Pick up vial on capping station")
        _is_held_by_arm = True
        _vial_location = None
        time.sleep(2)

    def place_vial_on_capping_station(self):
        global _vial_location, _is_held_by_arm
        if not _is_held_by_arm:
            raise RuntimeError("Robotic arm is not holding a vial")

        self.logger.info(f"Place vial on capping station")
        _is_held_by_arm = False
        _vial_location = 'capping_station'
        time.sleep(2)

    def pick_up_vial_on_solid_addition_station(self):
        global _vial_location, _is_held_by_arm
        if _is_held_by_arm:
            raise RuntimeError("Robotic arm is already holding a vial")
        if _vial_location != 'solid_addition_station':
            raise RuntimeError(f"Vial is not on the solid addition station, it is at: {_vial_location}")

        self.logger.info(f"Pick up vial on solid addition station")
        _is_held_by_arm = True
        _vial_location = None
        time.sleep(2)

    def place_vial_on_solid_addition_station(self):
        global _vial_location, _is_held_by_arm
        if not _is_held_by_arm:
            raise RuntimeError("Robotic arm is not holding a vial")

        self.logger.info(f"Place vial on solid addition station")
        _is_held_by_arm = False
        _vial_location = 'solid_addition_station'
        time.sleep(2)

    def pick_up_vial_on_liquid_addition_station(self):
        global _vial_location, _is_held_by_arm
        if _is_held_by_arm:
            raise RuntimeError("Robotic arm is already holding a vial")
        if _vial_location != 'liquid_addition_station':
            raise RuntimeError(f"Vial is not on the liquid addition station, it is at: {_vial_location}")

        self.logger.info(f"Pick up vial on liquid addition station")
        _is_held_by_arm = True
        _vial_location = None
        time.sleep(2)

    def place_vial_on_liquid_addition_station(self):
        global _vial_location, _is_held_by_arm
        if not _is_held_by_arm:
            raise RuntimeError("Robotic arm is not holding a vial")

        self.logger.info(f"Place vial on liquid addition station")
        _is_held_by_arm = False
        _vial_location = 'liquid_addition_station'
        time.sleep(2)

    def pick_up_vial_in_analysis_station(self):
        global _vial_location, _is_held_by_arm
        if _is_held_by_arm:
            raise RuntimeError("Robotic arm is already holding a vial")
        if _vial_location != 'analysis_station':
            raise RuntimeError(f"Vial is not in the analysis station, it is at: {_vial_location}")

        self.logger.info(f"Pick up vial on analysis station")
        _is_held_by_arm = True
        _vial_location = None
        time.sleep(2)

    def place_vial_in_analysis_station(self):
        global _vial_location, _is_held_by_arm
        if not _is_held_by_arm:
            raise RuntimeError("Robotic arm is not holding a vial")

        self.logger.info(f"Place vial on analysis station")
        _is_held_by_arm = False
        _vial_location = 'analysis_station'
        time.sleep(2)


# ----------------------------------------------------------------------------------------
class WeighBalance:
    """
    Example of a weigh balance, not a real implementation
    """
    def __init__(self):
        self.logger = logging.getLogger(f'{self.__class__.__name__}')

    def zero(self):
        self.logger.info(f"Zero weigh balance")
        time.sleep(2)

    def get_weight_mg(self) -> float:
        global _dummy_vial_weight_mg
        self.logger.info(f"Weight on weigh balance: {_dummy_vial_weight_mg} mg")
        time.sleep(2)
        return _dummy_vial_weight_mg


# ----------------------------------------------------------------------------------------
class StirPlate:
    """
    Example of a stir plate, not a real implementation
    """
    def __init__(self):
        self.logger = logging.getLogger(f'{self.__class__.__name__}')

    def start_stirring(self):
        self.logger.info(f"Start stirring")

    def stop_stirring(self):
        self.logger.info(f"Stop stirring")


# ----------------------------------------------------------------------------------------
class CappingStation:
    """
    Example of a vial capping station, not a real implementation
    """
    def __init__(self):
        self.logger = logging.getLogger(f'{self.__class__.__name__}')

    def uncap_vial(self):
        global _cap_is_on
        if _vial_location != 'capping_station':
            raise RuntimeError(f"Cannot uncap vial if it is not on the capping station. Current location: {_vial_location}")
        if not _cap_is_on:
            raise RuntimeError("Vial is already uncapped")
        self.logger.info(f"Uncap vial")
        _cap_is_on = False
        time.sleep(3)

    def cap_vial(self):
        global _cap_is_on
        if _vial_location != 'capping_station':
            raise RuntimeError(f"Cannot cap vial if it is not on the capping station. Current location: {_vial_location}")
        if _cap_is_on:
            raise RuntimeError("Vial is already capped")
        self.logger.info(f"Cap vial")
        _cap_is_on = True
        time.sleep(3)


# ----------------------------------------------------------------------------------------
class SolidAdditionStation:
    """
    Example of a solid addition station, not a real implementation
    """
    def __init__(self):
        self.logger = logging.getLogger(f'{self.__class__.__name__}')

    def add_solid(self, mass_mg: float):
        if _vial_location != 'solid_addition_station':
            raise RuntimeError(f"Cannot add solid if vial is not on the solid addition station. Current location: {_vial_location}")
        if _cap_is_on:
            raise RuntimeError("Cannot add solid because the vial cap is on")
        self.logger.info(f"Add solid {mass_mg} mg")
        global _dummy_vial_weight_mg, _solid_added_mg
        _dummy_vial_weight_mg += mass_mg
        _solid_added_mg += mass_mg
        time.sleep(2)


# ----------------------------------------------------------------------------------------
class LiquidAdditionStation:
    """
    Example of a liquid addition station, not a real implementation
    """
    def __init__(self):
        self.logger = logging.getLogger(f'{self.__class__.__name__}')

    def add_liquid(self, volume_ml: float):
        if _vial_location != 'liquid_addition_station':
            raise RuntimeError(f"Cannot add liquid if vial is not on the liquid addition station. Current location: {_vial_location}")
        if _cap_is_on:
            raise RuntimeError("Cannot add liquid because the vial cap is on")
        self.logger.info(f"Add liquid {volume_ml} mL")
        global _dummy_vial_weight_mg, _liquid_added_ml
        _dummy_vial_weight_mg += volume_ml
        _liquid_added_ml += volume_ml
        time.sleep(2)


# ----------------------------------------------------------------------------------------
class SampleAnalysisStation:
    """
    Example of a sample analysis station, not a real implementation
    This version evaluates the Branin function internally.
    """
    def __init__(self):
        self.logger = logging.getLogger(f'{self.__class__.__name__}')

    @staticmethod
    def _branin(x, y):
        a = 1.0
        b = 5.1 / (4 * np.pi ** 2)
        c = 5 / np.pi
        r = 6
        s = 10
        t = 1 / (8 * np.pi)

        return a * (y - b * x ** 2 + c * x - r) ** 2 + s * (1 - t) * np.cos(x) + s

    def analyze(self, input_1: Optional[float], input_2: Optional[float]) -> float:
        """
        Return a Branin signal value
        If no inputs are given, random values
            input_1 in [-5, 10]
            input_2 in [ 0, 15]

        :param input_1: optional, float
        :param input_2: optional, float
        :return:
        """
        if _vial_location != 'analysis_station':
            raise RuntimeError(f"Cannot analyze if vial is not on the analysis station. Current location: {_vial_location}")
        self.logger.info("Analyze sample")

        if input_1 is None:
            input_1 = -5.0 + random.random() * 15.0    # [-5, 10]
        if input_2 is None:
            input_2 = 0.0 + random.random() * 15.0     # [0, 15]

        x = float(input_1)
        y = float(input_2)

        # Evaluate Branin + light noise
        value = self._branin(x, y) + 0.05 * np.random.randn()
        self.logger.info(f'Sample signal: {value}')

        return value


# ----------------------------------------------------------------------------------------
# create example instruments
robotic_arm = RoboticArm()
weigh_balance = WeighBalance()
stir_plate = StirPlate()
capping_station = CappingStation()
solid_addition_station = SolidAdditionStation()
liquid_addition_station = LiquidAdditionStation()
sample_analysis_station = SampleAnalysisStation()

def enable_logging_to_console():
    stream_handler = logging.StreamHandler(sys.stdout)
    robotic_arm.logger.addHandler(stream_handler)
    robotic_arm.logger.setLevel(logging.INFO)
    weigh_balance.logger.addHandler(stream_handler)
    weigh_balance.logger.setLevel(logging.INFO)
    stir_plate.logger.addHandler(stream_handler)
    stir_plate.logger.setLevel(logging.INFO)
    capping_station.logger.addHandler(stream_handler)
    capping_station.logger.setLevel(logging.INFO)
    solid_addition_station.logger.addHandler(stream_handler)
    solid_addition_station.logger.setLevel(logging.INFO)
    liquid_addition_station.logger.addHandler(stream_handler)
    liquid_addition_station.logger.setLevel(logging.INFO)
    sample_analysis_station.logger.addHandler(stream_handler)
    sample_analysis_station.logger.setLevel(logging.INFO)
