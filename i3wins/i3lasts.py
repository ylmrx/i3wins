#!/usr/bin/env python3

import os
import socket
import selectors
import threading
from argparse import ArgumentParser
import i3ipc
import dynmen
from shlex import split
import collections
import sys

SOCKET_FILE = '/tmp/i3_focus_last'
MAX_WIN_HISTORY = 15


class FocusWatcher:
    def __init__(self):
        self.i3 = i3ipc.Connection()
        self.i3.on('window::focus', self.on_window_focus)
        self.listening_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        if os.path.exists(SOCKET_FILE):
            os.remove(SOCKET_FILE)
        self.listening_socket.bind(SOCKET_FILE)
        self.listening_socket.listen(1)
        self.window_list = []
        self.window_list_lock = threading.RLock()

    def on_window_focus(self, i3conn, event):
        with self.window_list_lock:
            window_id = event.container.props.id
            if window_id in self.window_list:
                self.window_list.remove(window_id)
            self.window_list.insert(0, window_id)
            if len(self.window_list) > MAX_WIN_HISTORY:
                del self.window_list[MAX_WIN_HISTORY:]

    def launch_i3(self):
        self.i3.main()

    def launch_server(self):
        selector = selectors.DefaultSelector()

        def accept(sock):
            conn, addr = sock.accept()
            selector.register(conn, selectors.EVENT_READ, read)

        def read(conn):
            data = conn.recv(1024)
            if data == b'switch':
                with self.window_list_lock:
                    tree = self.i3.get_tree()
                    windows = set(w.id for w in tree.leaves())
                    coll = []
                    for window_id, win_n in zip( self.window_list, range(len(self.window_list)) ):
                        if window_id not in windows:
                            self.window_list.remove(window_id)
                        else:
                            win = tree.find_by_id(window_id)
                            coll.append(("w{} d{:<4} | {}".format(win_n, win.workspace().name, win.name),
                                         window_id))
                    rofi = dynmen.Menu(split('rofi -dmenu -i -p \'> \'') + self.args)
                    print(coll)
                    try:
                        result = rofi(collections.OrderedDict(coll[1:]))
                        self.i3.command('[con_id=%s] focus' % result.value)
                    except dynmen.MenuError:
                        result = None
                        print("no selection")

            elif not data:
                selector.unregister(conn)
                conn.close()

        selector.register(self.listening_socket, selectors.EVENT_READ, accept)

        while True:
            for key, event in selector.select():
                callback = key.data
                callback(key.fileobj)

    def run(self, args):
        self.args = args
        t_i3 = threading.Thread(target=self.launch_i3)
        t_server = threading.Thread(target=self.launch_server)
        for t in (t_i3, t_server):
            t.start()


def server():
    args = sys.argv[1:]
    focus_watcher = FocusWatcher()
    focus_watcher.run(args)
    

def client():
    client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client_socket.connect(SOCKET_FILE)
    client_socket.send(b'switch')
    client_socket.close()


if __name__ == '__main__':
    server()
