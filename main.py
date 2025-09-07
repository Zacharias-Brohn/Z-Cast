from imports import *
from widgets.launcher.main import Launcher

dotenv.load_dotenv()

style_path = os.getenv( "HOME" ) + "/.config/z-cast/"

def check_css( *_ ):
    return app.set_stylesheet_from_file( style_path + "z-cast.css" )


if __name__ == "__main__":
    launcher = Launcher()

    # Hide initially

    launcher.hide()
    app = Application()

    monitor = monitor_file( style_path )
    monitor.connect( "changed", check_css )
    app.set_stylesheet_from_file( style_path + "z-cast.css" )

    app.run()
