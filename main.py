import dotenv

from imports import *
from widgets.launcher.main import Launcher

dotenv.load_dotenv()


def check_css( *_ ):
    return app.set_stylesheet_from_file(
            get_relative_path( "./css/main.css" )
        )


if __name__ == "__main__":
    launcher = Launcher()

    # Hide initially

    launcher.hide()
    app = Application()

    monitor = monitor_file(get_relative_path( "./css" ))
    monitor.connect( "changed", check_css )
    app.set_stylesheet_from_file( "css/main.css" )

    with open( get_relative_path( "debug/debug.txt" ), "w" ) as f:
        f.write( "It is opened" )
    app.run()
