from pulsectl import Pulse

pulse = Pulse('pulse-creen')


def sound_pids():
    sink_inputs = pulse.sink_input_list()
    return [int(sink_input.proplist['application.process.id']) for sink_input in sink_inputs]


def get_sink_input(pid):
    for sink_input in pulse.sink_input_list():
        sink_input_id = int(sink_input.proplist['application.process.id'])
        if sink_input_id == pid:
            return sink_input


def get_sink(sink_name):
    for sink in pulse.sink_list():
        if sink.name == sink_name:
            return sink


def move_sink(pid, sink_name):
    print(pid, sink_name)
    pulse.sink_input_move(get_sink_input(pid).index, get_sink(sink_name).index)
