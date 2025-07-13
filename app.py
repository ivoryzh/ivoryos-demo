import sys

import eventlet
eventlet.monkey_patch()

from demo_code_plugin.demo_code import pump, sdl, balance
from demo_code_plugin.plugin import source_code
import os


if __name__ == "__main__":
    import ivoryos
    from ivoryos.config import DemoConfig
    from ivoryos import socketio, utils

    _config = DemoConfig()
    _config.SESSION_COOKIE_SAMESITE = "Lax"
    #
    # run(__name__, config=_config, port=7860, debug=False, enable_design=True,
    #     exclude_names=["app", "global_config", "db","socketio", "login_manager", "g"])
    # #

    app = ivoryos.create_app(config_class=_config)  # Create app instance using factory function
    socketio.init_app(app, cors_allowed_origins="*", async_mode="eventlet")

    # plugins = load_installed_plugins(app, socketio)
    plugins = []
    config_plugins = ivoryos.load_plugins(source_code, app, socketio)
    plugins.extend(config_plugins)

    def inject_nav_config():
        """Make NAV_CONFIG available globally to all templates."""
        return dict(
            enable_design=True,
            plugins=plugins,
        )


    app.context_processor(inject_nav_config)
    port = 7860
    debug = False

    logger_path = os.path.join(app.config["OUTPUT_FOLDER"], app.config["LOGGERS_PATH"])
    dummy_deck_path = os.path.join(app.config["OUTPUT_FOLDER"], app.config["DUMMY_DECK"])

    module = __name__
    app.config["MODULE"] = module
    app.config["OFF_LINE"] = False
    ivoryos.global_config.deck = sys.modules[module]
    ivoryos.global_config.deck_snapshot = utils.create_deck_snapshot(ivoryos.global_config.deck,
                                                                     exclude_names=["app", "global_config", "db","socketio", "login_manager", "g"])

    app.config["ENABLE_LLM"] = False

    socketio.run(app, port=port, debug=debug, use_reloader=False)
