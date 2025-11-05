import logging
import time
from abc import ABC


class AbstractSDL(ABC):
    def __init__(self):
        self.pump = pump
        self.balance = balance
        self.logger = logging.getLogger(f"logger_name")

    def analyze(self):
        self.logger.info("analyze")
        return 1


    def dose_solid(self,
                   amount_in_mg: float = 5,
                   solid_name: str = "Acetaminophen"
                   ):
        """dose current chemical"""
        self.balance.dose_solid(amount_in_mg=amount_in_mg)
        self.balance.weigh_sample()
        self.logger.info(f"dosing solid {amount_in_mg} mg of {solid_name}")
        return 1

    def dose_solvent(self,
                     solvent_name: str = "Methanol",
                     amount_in_ml: float = 5,
                     rate_ml_per_minute: float = 1
                     ):
        self.logger.info(f"dosing {amount_in_ml} ml of {solvent_name} solvent at {rate_ml_per_minute} ml/min")
        return 1


    def equilibrate(self,
                    temp: float,
                    duration: float
                    ):
        self.logger.info(f"equilibrate at {temp} for {duration}")

    def simulate_error(self):
        raise ValueError("some error")

    def _send_command(self):
        """helper function"""
        pass

class BraninFunction:
    def __init__(self):
        self.a = 1
        self.b = 5.1 / (4 * 3.14159 ** 2)
        self.c = 5 / 3.14159
        self.r = 6
        self.s = 10
        self.t = 1 / (8 * 3.14159)

    def evaluate(self, x1: float, x2: float) -> float:
        """Evaluate the Branin function with given parameters x1 and x2."""
        term1 = self.a * (x2 - self.b * x1 ** 2 + self.c * x1 - self.r) ** 2
        term2 = self.s * (1 - self.t) * np.cos(x1)
        return term1 + term2 + self.s


# initializing hardware
robot = AbstractSDL()
branin = BraninFunction()

if __name__ == "__main__":
    import ivoryos
    ivoryos.run(__name__)