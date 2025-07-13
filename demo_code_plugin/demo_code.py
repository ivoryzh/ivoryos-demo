import logging
import time
from abc import ABC


class AbstractPump:

    def __init__(self, com_port: str):
        self.com_port = com_port
        self.dictionary = {}
        self.logger = logging.getLogger("pump")

    def dose_liquid(self, amount_in_ml: float, rate_ml_per_minute: float = 1):
        """dose liquid"""
        self.logger.info("dosing liquid")
        self.logger.info(f"pretending dosing {amount_in_ml} at {rate_ml_per_minute} ml/min")
        return 1



class AbstractBalance:

    def __init__(self, com_port: str):
        self.com_port = com_port
        self._value = None
        self.logger = logging.getLogger("balance")

    @property
    def setter_value(self):
        return self._value

    @setter_value.setter
    def setter_value(self, value):
        self._value = value

    def weigh_sample(self):
        time.sleep(1)
        self.logger.info(f"Weighing sample using {self.com_port}")
        return 1

    def dose_solid(self, amount_in_mg: float):
        """this function is used to dose solid"""
        time.sleep(1)
        self.logger.info(f"Dosing {amount_in_mg} mg using {self.com_port}")
        return 1

    def _helper(self):
        """helper function will not be extracted and displayed over function panel"""
        pass




class AbstractSDL(ABC):
    def __init__(self, pump: AbstractPump, balance: AbstractBalance):
        self.pump = pump
        self.balance = balance
        self.logger = logging.getLogger(f"logger_name")

    def analyze(self):
        self.logger.info("analyze")
        time.sleep(1)
        return 1


    def dose_solid(self,
                   amount_in_mg: float = 5,
                   solid_name: str = "Acetaminophen"
                   ):
        """dose current chemical"""
        print("dosing solid")
        self.balance.dose_solid(amount_in_mg=amount_in_mg)
        self.balance.weigh_sample()
        time.sleep(1)
        self.logger.info(f"dosing solid {amount_in_mg} mg of {solid_name}")
        return 1

    def dose_solvent(self,
                     solvent_name: str = "Methanol",
                     amount_in_ml: float = 5,
                     rate_ml_per_minute: float = 1
                     ):
        print("dosing liquid")
        self.logger.info(f"dosing {amount_in_ml} ml of {solvent_name} solvent at {rate_ml_per_minute} ml/min")
        time.sleep(1)
        return 1


    def equilibrate(self,
                    temp: float,
                    duration: float
                    ):
        print("equilibrate")
        self.logger.info(f"equilibrate at {temp} for {duration}")
        time.sleep(1)

    def simulate_error(self):
        raise ValueError("some error")

    def _send_command(self):
        """helper function"""
        pass



# initializing hardware
balance = AbstractBalance("Fake com port 1")
pump = AbstractPump("Fake com port 2")
sdl = AbstractSDL(pump, balance)


if __name__ == "__main__":
    import ivoryos
    ivoryos.run(__name__)