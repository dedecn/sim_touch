#coding: utf-8
import threading

import pykeyboard
import pymouse
import pykeyboard.mac
import Quartz
print Quartz.CFMachPortCreateRunLoopSource, Quartz.CFRunLoopGetCurrent, Quartz.CFRunLoopAddSource
print Quartz.CGEventTapEnable, Quartz.CGEventTapEnable, Quartz.CFRunLoopRunInMode

class ClickKeyEventListener(pykeyboard.PyKeyboardEvent):
    def __init__(self):
        super(ClickKeyEventListener, self).__init__(True)
        self.mouse = pymouse.PyMouse()
        self._mouse_down = False
        self._mouse_down_lock = threading.Lock()

    @property
    def mouse_down(self):
        with self._mouse_down_lock:
            return self._mouse_down

    @mouse_down.setter
    def mouse_down(self, flag):
        with self._mouse_down_lock:
            self._mouse_down = flag

    def handler(self, proxy, type, event, refcon):
        import Quartz
        # print 'type', type
        # print 'event', event
        key = Quartz.CGEventGetIntegerValueField(event, Quartz.kCGKeyboardEventKeycode)

        flags = Quartz.CGEventGetFlags(event)
        # print 'flags', hex(flags), hex(Quartz.kCGEventFlagMaskSecondaryFn), key
        if flags & Quartz.kCGEventFlagMaskSecondaryFn and key == 0x30: #tab

            Quartz.CGEventSetFlags(event, flags ^ Quartz.kCGEventFlagMaskSecondaryFn)
            pos = self.mouse.position()
            if type == Quartz.kCGEventKeyDown:
                if not self.mouse_down:
                    self.mouse_down = True
                    self.mouse.press(pos[0], pos[1])
                else:
                    pass
                # print 'press mouse'
            elif type == Quartz.kCGEventKeyUp:
                self.mouse_down = False
                self.mouse.release(pos[0], pos[1])
                # print 'release mouse'
            Quartz.CGEventSetType(event, Quartz.kCGEventNull)
            return event

        if flags & Quartz.kCGEventFlagMaskSecondaryFn and key == 6: #z
            self.stop()
            Quartz.CGEventSetType(event, Quartz.kCGEventNull)

        return event

class MouseEventListener(pymouse.PyMouseEvent):
    def __init__(self):
        super(MouseEventListener, self).__init__()
        pass

    def handler(self, proxy, type, event, refcon):
        # (x, y) = Quartz.CGEventGetLocation(event)
        # print 'type', type
        if type == Quartz.kCGEventLeftMouseDragged:
            # print 'drag mouse'
            pass
        elif type == Quartz.kCGEventMouseMoved:
            # print 'move mouse'
            if listener.mouse_down:
                # print 'trans drag'
                Quartz.CGEventSetType(event, Quartz.kCGEventLeftMouseDragged)
            else:
                pass
        return event


if __name__ == '__main__':
    print 'press Fn+tab=left mouse, press Fn+z to quit'
    mouse_listener = MouseEventListener()
    mouse_listener.start()
    listener = ClickKeyEventListener()
    listener.start()
    listener.join()
    mouse_listener.stop()
    mouse_listener.join()