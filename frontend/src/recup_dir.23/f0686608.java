/* exported init, buildPrefsWidget */
const { Gdk, GdkPixbuf, Gio, GLib, GObject, Gtk } = imports.gi;
const ByteArray = imports.byteArray;

let GnomeDesktop = null;
try {
    GnomeDesktop = imports.gi.GnomeDesktop;
} catch (e) {
    // not compatible with GTK4 yet
}

const ExtensionUtils = imports.misc.extensionUtils;

const BACKGROUND_SCHEMA = 'org.gnome.desktop.background';

const MONITOR_WIDTH = 1920;
const PREVIEW_WIDTH = 400;

let BackgroundLogoPrefsWidget = GObject.registerClass(
class BackgroundLogoPrefsWidget extends Gtk.Grid {
    _init() {
        super._init({
            halign: Gtk.Align.CENTER,
            margin_top: 24,
            margin_bottom: 24,
            margin_start: 24,
            margin_end: 24,
            column_spacing: 12,
            row_spacing: 6,
        });

        this._settings = ExtensionUtils.getSettings();
        this._settings.connect('changed', (settings, key) => {
            if (key === 'logo-file' ||
                key === 'logo-size')
                this._logo = null;
            this._preview.queue_draw();
        });

        this._preview = new Gtk.DrawingArea({
            halign: Gtk.Align.CENTER,
            margin_bottom: 18,
            width_request: PREVIEW_WIDTH,
            height_request: PREVIEW_WIDTH * 9 / 16,
        });
        this._preview.set_draw_func(this._drawPreview.bind(this));
        this.attach(this._preview, 0, 0, 2, 1);

        const filter = new Gtk.FileFilter();
        filter.add_pixbuf_formats();

        this._fileChooser = new Gtk.FileChooserNative({
            title: 'Select an Image',
            filter,
            modal: true,
        });
        this._fileChooser.connect('response',  (dlg, response) => {
            if (response !== Gtk.ResponseType.ACCEPT)
                return;
            this._settings.set_string('logo-file', dlg.get_file().get_path());
        });

        this._logoPicker = new Gtk.Button({
            label: '(None)',
        });
        this._logoPicker.connect('clicked', () => {
            this._fileChooser.transient_for = this.get_root();
            this._fileChooser.show();
        });
        this._settings.connect('changed::logo-file',
            this._updateLogoPicker.bind(this));
        this._updateLogoPicker();
        this._addRow(1, 'Logo image', this._logoPicker);

        let comboBox = new Gtk.ComboBoxText();
        comboBox.append('center', 'Center');
        comboBox.append('bottom-left', 'Bottom left');
        comboBox.append('bottom-center', 'Bottom center');
        comboBox.append('bottom-right', 'Bottom right');
        comboBox.append('top-left', 'Top left');
        comboBox.append('top-center', 'Top center');
        comboBox.append('top-right', 'Top right');
        this._settings.bind('logo-position',
            comboBox, 'active-id',
            Gio.SettingsBindFlags.DEFAULT);
        this._addRow(2, 'Position', comboBox);

        let adjustment = this._createAdjustment('logo-size', 0.25);
        let scale = new Gtk.Scale({ adjustment, draw_value: false });
        this._addRow(3, 'Size', scale);

        adjustment = this._createAdjustment('logo-border', 1.0);
        scale = new Gtk.Scale({ adjustment, draw_value: false });
        this._addRow(4, 'Border', scale);

        adjustment = this._createAdjustment('logo-opacity', 1.0);
        scale = new Gtk.Scale({ adjustment, draw_value: false });
        this._addRow(5, 'Opacity', scale);

        let checkWidget = new Gtk.CheckButton({
            label: 'Show for all backgrounds',
        });
        this._settings.bind('logo-always-visible',
            checkWidget, 'active',
            Gio.SettingsBindFlags.DEFAULT);
        this.attach(checkWidget, 1, 6, 1, 1);
    }

    _addRow(row, label, widget) {
        let margin = 48;

        widget.margin_end = margin;
        widget.hexpand = true;

        if (!this._sizeGroup) {
            this._sizeGroup = new Gtk.SizeGroup({
                mode: Gtk.SizeGroupMode.VERTICAL,
            });
        }
        this._sizeGroup.add_widget(widget);

        this.attach(new Gtk.Label({
            label,
            xalign: 1.0,
            margin_start: margin,
        }), 0, row, 1, 1);
        this.attach(widget, 1, row, 1, 1);
    }

    _createAdjustment(key, step) {
        let schemaKey = this._settings.settings_schema.get_key(key);
        let [type, variant] = schemaKey.get_range().deep_unpack();
        if (type !== 'range')
            throw new Error('Invalid key type "%s" for adjustment'.format(type));
        let [lower, upper] = variant.deep_unpack();
        let adj = new Gtk.Adjustment({
            lower,
            upper,
            step_increment: step,
            page_increment: 10 * step,
        });
        this._settings.bind(key, adj, 'value', Gio.SettingsBindFlags.DEFAULT);
        return adj;
    }

    _drawPreview(preview, cr, width, height) {
        if (!this._background)
            this._createBackgroundThumbnail(width, height);
        Gdk.cairo_set_source_pixbuf(cr, this._background, 0, 0);
        cr.paint();

        if (!this._logo)
            this._createLogoThumbnail(width);

        let [x, y] = this._getLogoPosition(width, height);
        Gdk.cairo_set_source_pixbuf(cr, this._logo, x, y);
        cr.paintWithAlpha(this._settings.get_uint('logo-opacity') / 255.0);
    }

    _getSlideShowSlide(file, width, height) {
        if (GnomeDesktop) {
            const slideShow = new GnomeDesktop.BGSlideShow({ file });
            slideShow.load();

            const [progress_, duration_, isFixed_, filename1, filename2_] =
                slideShow.get_current_slide(width, height);
            return Gio.File.new_for_commandline_arg(filename1);
        } else {
            const [, contents] = file.load_contents(null);
            const str = ByteArray.toString(contents);
            const [, filename1] = str.match(/<file>(.*)<\/file>/);
            return Gio.File.new_for_commandline_arg(filename1);
        }
    }

    _createBackgroundThumbnail(width, height) {
        let settings = new Gio.Settings({ schema_id: BACKGROUND_SCHEMA });
        let uri = settings.get_default_value('picture-uri').deep_unpack();
        let file = Gio.File.new_for_commandline_arg(uri);

        if (uri.endsWith('.xml'))
            file = this._getSlideShowSlide(file, width, height);
        let pixbuf = GdkPixbuf.Pixbuf.new_from_file(file.get_path());
        this._background = pixbuf.scale_simple(
            width, height, GdkPixbuf.InterpType.BILINEAR);
    }

    _createLogoThumbnail(width) {
        let filename = this._settings.get_string('logo-file');
        let file = Gio.File.new_for_commandline_arg(filename);
        let pixbuf = GdkPixbuf.Pixbuf.new_from_file(file.get_path());
        let size = this._settings.get_double('logo-size') / 100;
        let ratio = pixbuf.get_width() / pixbuf.get_height();
        this._logo = pixbuf.scale_simple(
            size * width,
            size * width / ratio,
            GdkPixbuf.InterpType.BILINEAR);
    }

    _getLogoPosition(width, height) {
        const previewScale = PREVIEW_WIDTH / MONITOR_WIDTH;
        const scaledBorder =
            previewScale * this._settings.get_uint('logo-border');
        let x, y;
        const position = this._settings.get_string('logo-position');
        if (position.endsWith('left'))
            x = scaledBorder;
        else if (position.endsWith('right'))
            x = (width - this._logo.get_width() - scaledBorder);
        else
            x = (width - this._logo.get_width()) / 2;

        if (position.startsWith('top'))
            y = scaledBorder;
        else if (position.startsWith('bottom'))
            y = height - this._logo.get_height() - scaledBorder;
        else
            y = (height - this._logo.get_height()) / 2;

        return [x, y];
    }

    _updateLogoPicker() {
        const filename = this._settings.get_string('logo-file');
        this._logoPicker.label = GLib.basename(filename);
    }

    on_destroy() {
        if (this._fileChooser)
            this._fileChooser.destroy();
        this._fileChooser = null;
    }
});

function init() {
}

function buildPrefsWidget() {
    return new BackgroundLogoPrefsWidget();
}
