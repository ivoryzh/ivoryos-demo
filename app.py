from sdl_docs.plugin import docs_bp

from scripts.sim_instruments import SimWeighBalance
from scripts.sim_instruments import SimRoboticArm
from scripts.sim_instruments import SimStirPlate
from scripts.sim_instruments import SimSolidAdditionStation
from scripts.sim_instruments import SimSampleAnalysisStation
from scripts.sim_instruments import SimCappingStation
from scripts.sim_instruments import SimLiquidAdditionStation
from sdl_sim_web.plugin import web_viz_bp
import ivoryos

# Initialize hardware
try:
    weigh_balance = SimWeighBalance()
    robotic_arm = SimRoboticArm()
    stir_plate = SimStirPlate()
    solid_addition_station = SimSolidAdditionStation()
    sample_analysis_station = SimSampleAnalysisStation()
    capping_station = SimCappingStation()
    liquid_addition_station = SimLiquidAdditionStation()
except Exception as e:
    print(f"Failed to initialize hardware: {e}. Connect them in the web interface or try again.")

# Start IvoryOS web interface
if __name__ == "__main__":
    import ivoryos
    from ivoryos.config import DemoConfig
    _config = DemoConfig()
    _config.SESSION_COOKIE_SAMESITE = "Lax"
    ivoryos.run(__name__, config=DemoConfig(), blueprint_plugins=[web_viz_bp, docs_bp], port=7860)

    # # USE CASE 2 - start OS using current module and enable LLM with Ollama
    # ivoryos.run(__name__, model="llama3.1", llm_server='localhost')
