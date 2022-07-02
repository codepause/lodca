import time
from typing import Union, Tuple

from lodca.configs.app_configs import AppConfig
from lodca.tools.layouts import LayoutManager
from lodca.engine.game_state import GameState
from lodca.tools.hookers.keyboard_hookers import KeyboardAppController
from lodca.tools.renderers.screen_renderer import RendererMP

_player_tess_default_names = [
    'stats', 'health_bar', 'mana_bar',
    'champion_level',
    'current_health', 'total_health',
    'current_mana', 'total_mana',
]

# set kwargs to pass only default stats and skill levels w/o items
_default_tools_kwargs = {
    'tess': {'names': _player_tess_default_names},
    'skill_level': {},
    'item': None
}


class App:
    def __init__(self):
        self.app_config = AppConfig()
        self.app_config.game_config.settings.scale = 0.23
        self.app_config.game_config.settings.minimap_on_left = True
        self.app_config.game_config.settings.champion = 'Lux'

        self.app_states = dict()

        self.player_layout = LayoutManager(self.app_config)
        self.target_layout = LayoutManager(self.app_config, target=True)

        self.game_state = GameState()

        self.kh = KeyboardAppController(self.app_config, self.app_states)
        # self.re = SimpleRenderer()
        self.re = RendererMP(self.app_config, key=None)

    def update(self):
        self.player_layout.update()
        self.target_layout.update()
        self.kh.update()
        self.re.update()

    def recognise(self, *args, **kwargs) -> Tuple[dict, dict]:
        if self.app_states.get('active_state', 0):
            tess_names = _player_tess_default_names + ['additional_stats', 'rune_stats']
            tools_kwargs = {'tess': {'names': tess_names}}
        else:
            tools_kwargs = _default_tools_kwargs

        player_data = self.player_layout(*args, tools_kwargs=tools_kwargs)
        target_data = self.target_layout(*args)
        return player_data, target_data

    def update_game_state(self, player_data: dict, target_data: dict):
        self.game_state.player_unit.update(ocr_data=player_data)
        self.game_state.target_unit.update(ocr_data=target_data)
        self.game_state.update()

    def render(self, data: list):
        self.re(data, render_state=self.app_states.get('render_state', 0))

    def use_skills(self, skills: dict, snapshot: dict) -> list:
        result = list()
        for idx, (name, skill) in enumerate(skills.items()):
            skill.snapshot_state(self.game_state)
            self.game_state.player_unit.set_stats(snapshot['player_unit']['stats'])
            self.game_state.target_unit.set_stats(snapshot['target_unit']['stats'])
            self.game_state.update()
            result.append({'name': skill.name, 'result': skill(), 'value': skill.value})
        return result

    def launch_once(self, *args, **kwargs):
        if self.app_states.get('working_state', 0):
            player_data, target_data = self.recognise(*args, **kwargs)
            # print(player_data, target_data)
            self.update_game_state(player_data, target_data)
            snapshot = self.game_state()

            skills_to_use = dict(self.game_state.player_unit.champion.data.skills)
            if self.app_states.get('combo_state', 0):
                skills_to_use.update(self.game_state.player_unit.champion.data.combos)
            result = self.use_skills(skills_to_use, snapshot)
            # print(self.game_state.player_unit.items.items())
            print(result)
            self.render(result)
        else:
            self.render(list())
            time.sleep(0.1)
        return None

    def launch(self):
        # self.app_states['active_state'] = 1
        self.re.start()
        while not self.app_states.get('exit', 0):
            a = time.time()
            self.launch_once()  # 0.5s active, 0.4 stats only
            # print(time.time() - a)
        self.re.join()
        # os._exit(0)
