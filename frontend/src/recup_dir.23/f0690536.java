Sender(this.get_sender());

            that._queueShutdownCheck();
        };
    }
};
Signals.addSignalMethods(ServiceImplementation.prototype);

var DBusService = class {
    constructor(name, service) {
        this._name = name;
        this._service = service;
        this._loop = new GLib.MainLoop(null, false);

        this._service.connect('shutdown', () => this._loop.quit());
    }

    run() {
        // Bail out when not running under gnome-shell
        Gio.DBus.watch_name(Gio.BusType.SESSION,
            'org.gnome.Shell',
            Gio.BusNameWatcherFlags.NONE,
            null,
            () => this._loop.quit());

        this._service.register();

        Gio.DBus.own_name(Gio.BusType.SESSION,
            this._name,
            Gio.BusNameOwnerFlags.REPLACE,
            () => this._service.export(),
            null,
            () => this._loop.quit());

        this._loop.run();
    }
};
