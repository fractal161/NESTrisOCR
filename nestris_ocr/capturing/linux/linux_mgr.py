import Xlib
import Xlib.display
from Xlib import X


class WindowMgr:
    """Encapsulates some calls for window management"""

    def __init__(self, hwnd=None):
        self.handle = hwnd

    def checkWindow(self, hwnd):
        """checks if a window still exists"""
        return hwnd

    def getWindows(self):
        """
        Return a list of tuples (handler, window name) for each real window.
        """
        windows = []
        display = Xlib.display.Display()
        root = display.screen().root

        try:
            _NET_CLIENT_LIST = display.get_atom('_NET_CLIENT_LIST')
            _NET_WM_NAME = display.get_atom('_NET_WM_NAME')
            client_list = root.get_full_property(
                _NET_CLIENT_LIST,
                property_type=X.AnyPropertyType,
            ).value

            for window_id in client_list:
                window = display.create_resource_object('window', window_id)
                window_name = window.get_full_property(
                    _NET_WM_NAME,
                    property_type=X.AnyPropertyType,
                ).value.decode('utf-8')
                windows.append((window_id, window_name))
            return windows

        except Xlib.error.BadAtom:
            windows = []
            def getWindowHierarchy(window, windows):
                children = window.query_tree().children
                for w in children:
                    try:
                        w.get_image(0, 0, 1, 1, X.ZPixmap, 0xFFFFFFFF)
                        wname = ""
                        if w.get_wm_name() is not None:
                        	wname += w.get_wm_name()
                        if w.get_wm_class() is not None:
                        	wname += w.get_wm_class()[1]
                        windows.append(
                            (
                                w.id,
                                wname,
                            )
                        )
                    except Xlib.error.BadMatch:
                        pass
                    finally:
                        windows = getWindowHierarchy(w, windows)
                return windows
            windows = getWindowHierarchy(root, windows)
            return windows
