from imports import *
from widgets.launcher.main import Launcher

dotenv.load_dotenv()

style_path = os.getenv( "HOME" ) + "/.config/z-cast/"

def setup_directories():
    if not os.path.exists( style_path ):
        os.makedirs( style_path, exist_ok=True )

        project_css = get_relative_path( "./css/" )
        for css in os.listdir( project_css ):
            shutil.copy( project_css + css, style_path )

def check_css( *_ ):
    return app.set_stylesheet_from_file( style_path + "z-cast.css" )


if __name__ == "__main__":
    launcher = Launcher()

    setup_directories()

    # Hide initially

    launcher.hide()
    app = Application()

    monitor = monitor_file( style_path )
    monitor.connect( "changed", check_css )
    app.set_stylesheet_from_file( style_path + "z-cast.css" )

    app.run()
