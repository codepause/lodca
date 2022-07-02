import tkinter as tk
from multiprocessing import Process, Queue
import pywintypes
import win32api
import win32con
from tabulate import tabulate
from PIL import Image, ImageTk
import numpy as np
import json

import epta.core as ec
from epta.core import ConfigDependent, PositionDependent
from epta.core.base_ops import Atomic
from epta.tools.renderers import BaseRenderer

import lodca.tools.mappings.mappers as ltm
import lodca.tools.mappings.wrappers as ltw


class ImageRenderer(PositionDependent, ConfigDependent):
    root: tk.Tk
    label_var: tk.StringVar
    label_var_2: tk.StringVar

    # https://stackoverflow.com/questions/21840133/how-to-display-text-on-the-screen-without-a-window-using-python
    def __init__(self, config: type, data_q: 'Queue', commands_q: 'Queue', name: str = 'screen_renderer',
                 key: str = None, **kwargs):
        config = config()

        relative_manager = ltm.RelativeManager(config.game_config)
        actual_manager = ltw.ActualManager(relative_manager)
        position_manager = ec.ToolDict([relative_manager, actual_manager])

        super(ImageRenderer, self).__init__(config=config, name=name, position_manager=position_manager, key=key,
                                            **kwargs)
        self.position_manager.update()

        self.ignore_color = '#fc0000'
        self._data_q = data_q
        self._commands_q = commands_q

        self.render_every_ms = 50
        self._quit = False

        self._init_labels()
        self.start()

    def apply_config_update(self, *args, **kwargs):
        self.position_manager.update()

    def _init_labels(self):
        # https://stackoverflow.com/questions/56096839/getting-background-color-as-well-when-i-transparent-the-background-color
        self.root = tk.Tk()
        self.label_var = tk.StringVar()
        self.label_var_2 = tk.StringVar()
        self.root.configure(background='#fc0000')
        label = tk.Label(textvariable=self.label_var, font=('Arial', '20'), fg='white', bg='#fc0000', anchor='w',
                         justify=tk.LEFT)
        label_2 = tk.Label(textvariable=self.label_var_2, font=('Arial', '20'), fg='white', bg='#fc0000', anchor='w',
                           justify=tk.RIGHT)
        label.master.overrideredirect(True)
        w = 400
        h = 900
        x = 1920 - w
        y = 1080 // 2 - h // 2
        label.master.geometry(f"{int(w)}x{int(h)}+{int(x)}+{int(y)}")
        label.master.lift()
        label.master.wm_attributes("-topmost", True)
        label.master.wm_attributes("-disabled", True)
        label.master.wm_attributes("-transparentcolor", self.ignore_color)
        hWindow = pywintypes.HANDLE(int(label.master.frame(), 16))
        # http://msdn.microsoft.com/en-us/library/windows/desktop/ff700543(v=vs.85).aspx
        # The WS_EX_TRANSPARENT flag makes events (like mouse clicks) fall through the window.
        exStyle = win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT | win32con.WS_EX_COMPOSITED
        win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)
        label.grid(row=0, column=0)
        label_2.grid(row=0, column=1, padx=30)

    @staticmethod
    def __render_skill(skill_name: str, skill_data: dict, render_state: int = 1) -> tuple:
        # skill data: {'total_damage': 0, 'detailed_damage': [(key, value), ...]}
        key_s = f'{skill_name}\n'
        value_s = f'{skill_data["total_damage"]:>5.2f}\n'

        if render_state == 2:
            for key, value in skill_data['detailed_damage']:
                key_s += f'  {key}:\n'
                value_s += f'{value:>5.2f}\n'
        return key_s, value_s

    def _prepare_data(self, data: dict):
        render_data = data['skills']
        keys_s, values_s = '', ''

        if data['render_state'] > 0:
            for key, value in render_data.items():
                k, v = self.__render_skill(key, value, data['render_state'])
                keys_s += k
                values_s += v
            # s = json.dumps(render_data, indent=2)
        self.label_var.set(keys_s)
        self.label_var_2.set(values_s)

    def parse_commands_q(self, *args, **kwargs):
        if not self._commands_q.empty():
            command = self._commands_q.get()
            if command == 'stop':
                self._quit = True
            if command == 'update':
                # TODO: be clever and redo all of this
                pass

    def parse_data_q(self, *args, **kwargs):
        if self._data_q.empty():
            pass
        else:
            self._prepare_data(self._data_q.get())

    def render_loop(self, **kwargs):
        self.parse_commands_q()
        self.parse_data_q()
        if self._quit:
            self.quit()
        else:
            self.root.after(self.render_every_ms, self.render_loop)

    def quit(self):
        self.root.destroy()

    def start(self):
        self.render_loop()
        self.root.mainloop()


class RendererMP(BaseRenderer, Atomic):
    """
    Setup new process to render data. (tk based)
    """

    def __init__(self, config: 'Config', name: str = 'screen_renderer_mp', **kwargs):
        super(RendererMP, self).__init__(name=name, **kwargs)
        self.data_q = Queue()
        self.commands_q = Queue()

        self.process = Process(target=ImageRenderer,
                               args=(type(config), self.data_q, self.commands_q),
                               kwargs={'key': self.key})

    def start(self):
        self.process.start()

    def join(self):
        self.commands_q.put('stop')
        self.process.join()

    def _prepare_data(self, data: list, render_state: int = 0, **kwargs):
        # data is a dictionary of {skill.name: skill_result}
        render_data = {'render_state': render_state, 'skills': dict()}
        if render_state > 0:  # default render state
            for skill_data in data:
                skills = skill_data['result']
                if not skills:
                    continue
                name = skill_data['name']
                render_data['skills'][name] = dict()

                skill_result = list()
                for idx, skill in enumerate(skills):
                    if isinstance(skill, list):  # if it is a combo
                        value = [temp.value for temp in skill if temp.value]
                        skill_result.append((idx, sum(value)))
                    elif skill.value:
                        skill_result.append((skill.name, skill.value))

                render_data['skills'][name]['total_damage'] = sum([result[1] for result in skill_result])
                if render_state == 2:
                    render_data['skills'][name]['detailed_damage'] = skill_result
        return render_data

    def render(self, data: list, **kwargs):
        if self.data_q.empty():  # "sync" frames
            render_data = self._prepare_data(data, **kwargs)
            self.data_q.put(render_data)
        return data
