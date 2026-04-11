from sim_instruments import *
from sim_plugin.sdl_sim_web.plugin import web_viz_bp
from sdl_docs.plugin import docs_bp
import os
if __name__ == "__main__":
    import ivoryos
    from ivoryos.config import DemoConfig
    _config = DemoConfig()
    _config.SESSION_COOKIE_SAMESITE = "Lax"
    ivoryos.run(__name__, config=DemoConfig(), blueprint_plugins=[web_viz_bp, docs_bp], port=7860)

    # # USE CASE 2 - start OS using current module and enable LLM with Ollama
    # ivoryos.run(__name__, model="llama3.1", llm_server='localhost')
