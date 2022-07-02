from typing import Dict


def _get_image_hooker(config: 'AppConfig', key: str, actual_manager: 'ToolDict'):
    import epta.core.base_ops as ecb
    import epta.tools.base as etb
    from epta.tools.hookers.image_hookers import ImreadHooker, MssScreenHooker

    if config.settings.image_hooker == 'imread':
        image_hooker = ecb.Sequential([
            ImreadHooker(),
            etb.PositionCropper(key=key, position_manager=actual_manager),
        ])
    elif config.settings.image_hooker == 'mss':
        image_hooker = MssScreenHooker(key=key, position_manager=actual_manager)
    else:
        raise Exception(f"Image hooker is '{config.settings.image_hooker}' but must be 'imread' or 'mss'")

    return image_hooker


def player_builder(config: 'AppConfig', **kwargs) -> Dict[str, 'BaseTool']:
    import epta.core as ec

    import lodca.tools.mappings.mappers as ltm
    import lodca.tools.mappings.wrappers as ltw
    import lodca.tools.mappings.croppers as ltc

    from lodca.tools.recognition.image_recognition import ImageRecognition

    relative_manager = ltm.RelativeManager(config.game_config)
    actual_manager = ltw.ActualManager(relative_manager)

    position_manager = ec.ToolDict([relative_manager, actual_manager])

    image_hooker = _get_image_hooker(config, 'interface', position_manager['actual_manager'])

    cropper = ltc.CropperManager(actual_manager, build_names=[
        'inventory', 'stats', 'additional_stats',
        'rune_stats',
        # 'health_bar', 'mana_bar',
        'skill_points', 'champion_level',
        'current_health', 'total_health',
        'current_mana', 'total_mana',
    ])

    image_rec = ImageRecognition(config, position_manager)

    return {'position_manager': position_manager,
            'cropper': cropper,
            'image_rec': image_rec,
            'image_hooker': image_hooker}


def target_builder(config: 'AppConfig', **kwargs) -> Dict[str, 'BaseTool']:
    import epta.core as ec

    import lodca.tools.mappings.target_mappers as ltm
    import lodca.tools.mappings.target_wrappers as ltw
    import lodca.tools.mappings.target_croppers as ltc

    from lodca.tools.recognition.image_recognition import ImageRecognitionTarget

    relative_manager = ltm.RelativeManager(config.game_config)
    actual_manager = ltw.ActualManager(relative_manager)

    position_manager = ec.ToolDict([relative_manager, actual_manager])

    image_hooker = _get_image_hooker(config, 'interface', position_manager['actual_manager'])

    cropper = ltc.CropperManager(actual_manager, build_names=[
        'inventory', 'stats',
        # 'health_bar', 'mana_bar',
        'champion', 'champion_level',
        'current_health', 'total_health',
        'current_mana', 'total_mana', 'indicator'
    ])
    image_rec = ImageRecognitionTarget(config, position_manager)

    return {'position_manager': position_manager,
            'cropper': cropper,
            'image_hooker': image_hooker,
            'image_rec': image_rec}
