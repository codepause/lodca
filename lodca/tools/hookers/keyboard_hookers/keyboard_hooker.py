import keyboard
from functools import partial

from epta.tools.hookers.keyboard_hookers import KeyboardHooker


class KeyboardAppController(KeyboardHooker):
    def __init__(self, config: 'Config', app_states: dict, name: str = 'kbd_app_controller', **kwargs):
        super(KeyboardAppController, self).__init__(config=config, name=name, **kwargs)

        # working_state:
        # 0 - off, 1 - on

        # render_state:
        # 0 - off, 1 - on, 2 - detailed

        # active_state:
        # hold 'c' to update current additional stats and items

        # combo_state:
        # 0 - off, 1 - add combo damage calculation

        # exit:
        # 1 - app off, 0 - app on
        self.app_states = app_states

        self._add_hotkeys()

    def set_state(self, state_name: str, *args, **kwargs):
        state = self.app_states.get(state_name, 0)

        if state_name == 'working_state':
            state = (state + 1) % 2
        elif state_name == 'render_state':
            state = (state + 1) % 3
        elif state_name == 'combo_state':
            state = (state + 1) % 2
        elif state_name == 'active_state_start':
            state_name = 'active_state'
            state = 1
        elif state_name == 'active_state_end':
            state_name = 'active_state'
            state = 0
        elif state_name == 'exit':
            state = 1

        self.app_states[state_name] = state
        print(f'{state_name} state is set to', state)

    def _add_hotkeys(self):
        keyboard.add_hotkey(self.config.kh_config.settings.working_state_key, self.set_state, args=('working_state',))
        keyboard.add_hotkey(self.config.kh_config.settings.render_state_key, self.set_state, args=('render_state',))
        keyboard.add_hotkey(self.config.kh_config.settings.combo_state_key, self.set_state, args=('combo_state',))

        keyboard.on_press_key(self.config.kh_config.settings.active_state_key,
                              partial(self.set_state, 'active_state_start'))
        keyboard.on_release_key(self.config.kh_config.settings.active_state_key,
                                partial(self.set_state, 'active_state_end',))

        keyboard.add_hotkey(self.config.kh_config.settings.exit_state_key, self.set_state, args=('exit',))


if __name__ == '__main__':
    def clb(state: str, *args, **kwargs):
        print(state, args, kwargs)


    keyboard.on_press_key('space', partial(clb, 'pressed'))
    keyboard.on_release_key('space', partial(clb, 'released'))
    keyboard.wait()
