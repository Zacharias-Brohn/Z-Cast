from collections.abc import Iterator
from imports import *


class Launcher( WaylandWindow ):
    def __init__( self ):
        super().__init__(
            title="launcher",
            name="launcher",
            layer="top",
            anchor="center",
            exclusivity="none",
            keyboard_mode="on-demand",
            visible=False,
            all_visible=False,
        )
        self._arranger_handler: int = 0
        self._app_usage = self._load_app_usage()
        self._all_apps = get_desktop_applications()
        self._current_top_app = None
        self.config_dir = os.getenv( "HOME" ) + "/.config/z-cast/"
        self.data_dir = os.getenv( "HOME" ) + "/.local/share/z-cast/"

        self.viewport = Box( orientation="v", name="launcher-viewport" )

        self.search = Entry(
            placeholder="Search for apps...",
            h_expand=True,
            notify_text=lambda entry, *_: self.arrange_viewport( entry.get_text() ),
            name="launcher-search",
            on_focus_in_event=lambda *_: (
                self.details_label.set_label( "Z-Cast" )
            ),
        )
        self.search.connect( "key-press-event", self.on_search_key_press )

        self.apps = ScrolledWindow(
            min_content_size=( 600, 800 ),
            max_content_size=( 280 * 2, 800 ),
            child=self.viewport,
            name="launcher-apps",
            smooth_scroll=True,
            kinetic_scroll=True,
            overlay_scroll=True,
        )

        self.action_area = Box( name="launcher-area" )
        self.details_label = Label( label="Z-Cast", name="launcher-details-label" )
        self.details_image = (
            Image(
                icon_name="edit-undo-symbolic",
                name="launcher-details-icon",
            )
            .build()
            .set_pixel_size( 12 )
            .unwrap()
        )
        self.details = CenterBox(
            name="launcher-details",
            start_children=[
                Svg(
                    size=24,
                    svg_file=get_relative_path( "../../assets/wolf.svg" ),
                    style="fill: #fafafa;",
                )
            ],
            end_children=[
                Button( child=Box( children=[ self.details_label, self.details_image ]))
            ],
        )

        self.add(
            Box(
                name="launcher-container",
                orientation="v",
                children=[ self.search, self.action_area, self.apps, self.details ],
            )
        )
        self.show_all()

        self.connect( "key-release-event", self.on_key )

    def on_key( self, entry, event_key ):
        if event_key.keyval == 65307:
            self.toggle()

    def on_search_key_press( self, entry, event_key ):
        if event_key.keyval == 65293:
            if self._current_top_app:
                self.launch_app( self._current_top_app )
                self.hide()
                return True
        return False

    def arrange_viewport( self, query: str = "" ):
        remove_handler( self._arranger_handler ) if self._arranger_handler else None

        self.viewport.children = []

        if not query:
            filtered_apps = [
                app
                for app in self._all_apps
            ]
            filtered_apps.sort(
                key=lambda app: (
                    -(self._app_usage.get(app.name, 0) > 0),
                    -self._app_usage.get(app.name, 0),
                    (app.display_name or app.name).lower()
                ),
            )
        else:
            scored_apps = [
                ( self._score_app_match( app, query ), app )
                for app in self._all_apps
            ]

            scored_apps = [ 
                ( score, app ) for score, app in scored_apps if score >= 0.7
            ]

            scored_apps.sort( key=lambda x: x[0], reverse=True )

            filtered_apps = [ app for score, app in scored_apps ]


        filtered_apps_iter = iter( filtered_apps )

        should_resize = operator.length_hint( filtered_apps_iter ) == len( self._all_apps )

        self._current_top_app = filtered_apps[0] if filtered_apps else None

        self._arranger_handler = idle_add(
            lambda *args: self.add_next_application( *args )
            or ( self.resize_viewport() if should_resize else False ),
            filtered_apps_iter,
            pin=True,
        )

        return False

    def add_next_application( self, apps_iter: Iterator[ DesktopApp ]):
        if not ( app := next( apps_iter, None )):
            return False

        app_button = self.bake_application_slot( app )
        self.viewport.add( app_button )

        return True

    def resize_viewport( self ):
        self.apps.set_min_content_width(
            self.viewport.get_allocation().width  # type: ignore
        )
        return False

    def bake_application_slot( self, app: DesktopApp, **kwargs ) -> Button:
        return Button(
            name="launcher-app",
            child=Box(
                orientation="h",
                children=[
                    Image(
                        pixbuf=app.get_icon_pixbuf( size=32 ),
                        h_align="start",
                        name="launcher-app-icon",
                    ),
                    Label(
                        label=app.display_name or "Unknown",
                        v_align="center",
                        h_align="center",
                    ),
                    Box( h_expand=True ),
                    Label(
                        label="Application",
                        tooltip_text=app.description,
                        name="launcher-app-label",
                    ),
                ],
            ),
            on_focus_in_event=lambda *_: (
                self.details_label.set_label( "Open Application" )
            ),
            on_clicked=lambda *_: (
                self.launch_app( app ),
                self.hide(),
            ),
            **kwargs,
        )

    def launch_app( self, app: DesktopApp ):
        self._app_usage[ app.name ] = self._app_usage.get( app.name, 0 ) + 1
        self._save_app_usage()

        command = (
            " ".join([ arg for arg in app.command_line.split() if "%" not in arg ])
            if app.command_line
            else None
        )
        (
            exec_shell_command_async(
                f"uwsm-app -S out -- { command }",
                lambda *_: print( f"Launched { app.name }" ),
            )
            if command
            else None
        )

    def toggle( self ):
        self._all_apps = get_desktop_applications()
        self.search.set_text( "" )
        self.search.grab_focus()
        self.arrange_viewport()
        self.set_visible( not self.is_visible() )

    def _score_app_match( self, app: DesktopApp, query: str ) -> float:
        query_lower = query.casefold()
        display_name_lower = (app.display_name or "").casefold()
        name_lower = app.name.casefold()
        generic_name_lower = (app.generic_name or "").casefold()

        score = 0.0

        if query_lower == display_name_lower:
            score = 1.0
        elif query_lower == name_lower:
            score = 0.95

        elif display_name_lower.startswith(query_lower):
            score = 0.9
        elif name_lower.startswith(query_lower):
            score = 0.85

        elif f" {query_lower}" in display_name_lower:
            score = 0.75
        elif f" {query_lower}" in name_lower:
            score = 0.7

        elif query_lower in display_name_lower:
            score = 0.6
        elif query_lower in name_lower:
            score = 0.55

        elif query_lower in generic_name_lower:
            score = 0.4

        else:
            fuzz_ratio = max(
                fuzz.ratio(query_lower, display_name_lower),
                fuzz.ratio(query_lower, name_lower),
                fuzz.ratio(query_lower, generic_name_lower),
            )
            score = fuzz_ratio / 100

        usage_bonus = min(self._app_usage.get(app.name, 0) / 1000, 0.1)
        score += usage_bonus

        return score

    def _load_app_usage( self ):
        try:
            with open( self.data_dir + "usage.json", "r" ) as f:
                return json.loads( f.read() )
        except ( FileNotFoundError, json.JSONDecodeError ):
            return {}

    def _save_app_usage( self ):
        os.makedirs( self.data_dir, exist_ok=True )
        with open( self.data_dir + "usage.json", "w" ) as f:
            f.write( json.dumps( self._app_usage ))
