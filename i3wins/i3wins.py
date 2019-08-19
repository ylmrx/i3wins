from dynmen import Menu
import i3ipc
from shlex import split
import collections
import sys

def main(rofi_args=sys.argv[1:]):
    command_line = "rofi -dmenu -i -markup-rows -p '> '"
    i3 = i3ipc.Connection()
    pink = "w{} d{:<4} |<span color='pink'> {}</span>"
    yellow = "w{} d{:<4} |<span color='yellow'> {}</span>"
    coll = collections.deque()
    t = i3.get_tree()
    f = t.find_focused()
    for w, n in zip(t.leaves(), range(len(t.leaves()))):
        if f.id == w.id:
            coll.appendleft((w.id, yellow.format(n + 1, w.workspace().name, w.name)))
        elif w.workspace().id == f.workspace().id:
            coll.appendleft((w.id, pink.format(n + 1, w.workspace().name, w.name)))
        else:
            coll.append((w.id, "w{} d{:<4} | {}".format(n + 1, w.workspace().name, w.name)))

    rofi = Menu(split(command_line) + rofi_args)
    result = rofi(collections.OrderedDict((v, k) for k, v in coll))
    f = t.find_by_id(result.value)
    f.command('focus')
    
if __name__ == '__main__':
    main()
