,
            () => {
                this._shutdownTimeoutId = 0;
                this._maybeShutdown();

                return GLib.SOURCE_REMOVE;
            });
    }

    _trackSender(sender) {
        if (this._senders.has(sender))
            return;

        this.hold();
        this._senders.set(sender,
            this._dbusImpl.get_connection().watch_name(
                sender,
                Gio.BusNameWatcherFlags.NONE,
                null,
                () => this._untrackSender(sender)));
    }

    _untrackSender(sender) {
        const id = this._senders.get(sender);

        if (id)
            this._dbusImpl.get_connection().unwatch_name(id);

        if (this._senders.delete(sender))
            this.release();
    }

    _injectTracking(methodName) {
        const { prototype } = Gio.DBusMethodInvocation;
        const origMethod = prototype[methodName];
        const that = this;

        prototype[methodName] = function (...args) {
            origMethod.apply(this, args);

            if (that._hasSignals)
                that._trackSender(this.get_sender());

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
