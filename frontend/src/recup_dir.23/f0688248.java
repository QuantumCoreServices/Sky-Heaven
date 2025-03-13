eves the current list of windows and their properties

        A window is exposed as:
        * t ID: unique ID of the window
        * a{sv} properties: high-level properties

          Known properties:

          - "title"       (s): (readonly) title of the window
          - "app-id"      (s): (readonly) application ID of the window
          - "wm-class"    (s): (readonly) class of the window
          - "client-type" (u): (readonly) 0 for Wayland, 1 for X11
          - "is-hidden"   (b): (readonly) if the window is currently hidden
          - "has-focus"   (b): (readonly) if the window currently have
                                          keyboard focus
          - "width"       (u): (readonly) width of the window
          - "height"      (u): (readonly) height of the window
    --><method name="GetWindows"><arg name="windows" direction="out" type="a{ta{sv}}"/></method><!--
       AnimationsEnabled:
       @short_description: Whether the shell animations are enabled

       By default determined by the org.gnome.desktop.interface enable-animations
       gsetting, but may be overridden, e.g. if there is an active screen cast or
       remote desktop session that asked for animations to be disabled.

       Since: 2
    --><property name="AnimationsEnabled" type="b" access="read"/><!--
       ScreenSize:
       @short_description: The size of the screen

       Since: 3
    --><property name="ScreenSize" type="(ii)" access="read"/><property name="version" type="u" access="read"/></interface></node>
