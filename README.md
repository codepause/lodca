# LODCA: League of Legends Online Damage Calculator

### About:
CV-project made for League of Legends. General idea is to **predict** damage of a player champion for a current game state.

[Youtube video](https://youtu.be/7OyWXWnVABw)

### Installation:
- Install [EPTA](https://github.com/antistack/epta)
- Install [tesserocr](https://github.com/sirfz/tesserocr)
- Install [LODCA](https://github.com/codepause/lodca)
```
git clone https://github.com/codepause/lodca
cd lodca
pip install -r requirements.txt
python setup.py develop
```
- Templates for image recognition. [Data Dragon](https://developer.riotgames.com/docs/lol) 
- Configure [config](https://github.com/codepause/lodca/blob/master/lodca/configs/app_settings.py):
``` 
Specify path for two folders with images in TemplateSettings:
 dragontail/{version}/img/{item, champion}
And two json files in DatabaseSettings:
 dragontail/{version}/data/en_GB/{item, champion}.json
Specify other settings:
 interface scale
 minimap position
 additional stats button ('c' by default)

Make sure ingame option to always show base stats is on.
```

### Launch:

```
cd demo
python main.py
```

### Hotkeys:
>- `c`: Update current items / additional stats
>- `NUM_1`: `on / off` application
>- `NUM_2`: Change rendering mode:
>   - `0` - render disabled
>   - `1` - damage output
>   - `2` - detailed damage output (with sources)
>- `NUM_3`: `on / off` combo damage
>- `NUM_0`: `Shutdown`
  
### Acknowledgement:
- [Antistack basic tools for CV bots](https://github.com/antistack/epta)


## P.S:
- This is a fun-made project mainly for portfolio. I appreciate any support.
- There is only `Lux` currently for demo purposes.
- Auto skill construction is not possible (or just for simple ones).
- Auto patch changes to damage / stats is possible, not implemented. 
- Currently it is working at ~3fps: `Tesserocr` and `opencv` methods might be replaced with more smart solutions.
 (Neural nets, API integration)
- **Use at your own risk. No responsibilities taken.**