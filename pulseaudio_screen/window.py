from subprocess import check_output, CalledProcessError

import re


def get_windows_ids():
    # output = check_output(['xwininfo', '-root', '-children'])
    output = check_output(['wmctrl', '-lx']).decode('utf-8')
    return re.findall('(0x[0-9a-f]+)', output)


def get_window_pid(window_id):
    try:
        o = check_output(['xprop', '-id', window_id, '_NET_WM_PID'])
        return int(o.decode('utf-8').rstrip('\n').split(' ')[-1])
    except CalledProcessError:
        return


def windows_by_pid(process_id):
    windows = get_windows_ids()
    for window in windows:
        p = get_window_pid(window)
        if p == process_id:
            yield window


def window_data(window_id):
    lines = check_output(['xwininfo', '-id', window_id]).decode('utf-8')
    lines = lines.split('\n')
    lines = [line[2:].split(': ', 1) for line in lines if line.startswith('  ') and ': ' in line]
    return {k: v for k, v in lines}
