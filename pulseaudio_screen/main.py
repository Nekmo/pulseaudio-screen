import time
from pulseaudio_screen.pulse import sound_pids, move_sink
from pulseaudio_screen.tempdict import TempDict
from pulseaudio_screen.window import windows_by_pid, window_data

DELAY = .5
SCREENS_IDS = [0, 1920, 3840]

SCREENS_PULSE_NAMES = [
    'alsa_output.pci-0000_01_00.1.hdmi-surround-extra2',
] + ['alsa_output.pci-0000_03_04.0.analog-stereo'] * 2

pids_windows_ids = TempDict(15)  # ids de las ventanas por su pid
pids_screens = TempDict(15)


def pid_window_corner(pid):
    windows = pids_windows_ids.get(pid) or list(windows_by_pid(pid))
    if pid not in pids_windows_ids:
        pids_windows_ids[pid] = windows
    if not windows or not windows[0]:
        return
    return [int(x) for x in window_data(windows[0])['Corners'].split('  ')[0].split('+')[-2:]]


def get_screen(width):
    for i, screen in enumerate(SCREENS_IDS):
        if SCREENS_IDS[(i+1) % len(SCREENS_IDS)] > width or i + 1 >= len(SCREENS_IDS):
            return i


def pids_changed_screen():
    """Aplicaciones cuya ventana puede haber cambiado su posición
    :return: 
    """
    pids = sound_pids()
    for pid in pids:
        corner = pid_window_corner(pid)
        if not corner:
            continue
        screen = get_screen(corner[0])
        if pids_screens.get(pid) != screen:
            pids_screens[pid] = screen
            yield pid, screen


def main():
    while True:
        for pid, screen in list(pids_changed_screen()):
            move_sink(pid, SCREENS_PULSE_NAMES[screen])
        time.sleep(DELAY)
