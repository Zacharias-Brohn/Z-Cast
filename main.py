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

    config_file = style_path + "config.json"
    if not os.path.exists( config_file ):
        default_config = {
            "launch_prefix": ""
        }
        with open( config_file, "w" ) as f:
            json.dump( default_config, f, indent=4 )

def check_css( *_ ):
    return app.set_stylesheet_from_file( style_path + "z-cast.css" )

def restart_app():
    python = sys.executable
    subprocess.Popen( [ python ] + sys.argv, start_new_session=True )
    sys.exit(0)

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
