from demo_code_plugin.demo_code import pump, sdl, balance
from demo_code_plugin.plugin import source_code
import os
if __name__ == "__main__":
    import ivoryos
    from ivoryos.config import DemoConfig
    import eventlet

    eventlet.monkey_patch()

    _config = DemoConfig()
    _config.SESSION_COOKIE_SAMESITE = "Lax"

    port = int(os.environ.get("PORT", 7860))

    ivoryos.run(__name__, config=DemoConfig(), blueprint_plugins=source_code, port=port)

    # # USE CASE 2 - start OS using current module and enable LLM with Ollama
    # ivoryos.run(__name__, model="llama3.1", llm_server='localhost')
