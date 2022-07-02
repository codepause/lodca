def mappers_test():
    import cv2 as cv

    import epta.core as ec
    import epta.core.base_ops as ecb
    import epta.tools.base as etb
    from epta.utils import save_crops
    from epta.tools.hookers.image_hookers import ImreadHooker

    import lodca
    import lodca.tools.mappings.mappers as ltm
    import lodca.tools.mappings.wrappers as ltw
    import lodca.tools.mappings.croppers as ltc

    cfg = lodca.configs.app_configs.GameConfig()
    cfg.settings.scale = 1.
    cfg.settings.minimap_on_left = True

    # TODO: add registry
    relative_manager = ltm.RelativeManager(cfg)
    actual_manager = ltw.ActualManager(relative_manager)

    position_manager = ec.ToolDict([relative_manager, actual_manager])

    image_hooker = ecb.Sequential([
        ImreadHooker(),
        etb.PositionCropper(key='interface', position_manager=actual_manager),
    ])

    cropper = ltc.CropperManager(actual_manager, build_names=[
        'inventory', 'stats', 'additional_stats',
        'rune_stats',
        # 'health_bar', 'mana_bar',
        'skill_points', 'champion_level',
        'current_health', 'total_health',
        'current_mana', 'total_mana',
    ])

    position_manager.update()
    image_hooker.update()
    cropper.update()

    image = image_hooker.use(
        './temp/examples/evelynn_1920_1080_minimap_on_left_scale_1_target_enemy.png')
    result = cropper.use(image)

    save_crops(image, './temp/crops/interface.png')
    save_crops(result, './temp/crops/')
    return result


def target_mappers_test():
    import epta.core as ec
    import epta.core.base_ops as ecb
    import epta.tools.base as etb
    from epta.utils import save_crops
    from epta.tools.hookers.image_hookers import ImreadHooker

    import lodca
    import lodca.tools.mappings.target_mappers as ltm
    import lodca.tools.mappings.target_wrappers as ltw
    import lodca.tools.mappings.target_croppers as ltc

    cfg = lodca.configs.app_configs.GameConfig()
    cfg.settings.scale = 0.23
    cfg.settings.minimap_on_left = True

    relative_manager = ltm.RelativeManager(cfg)
    actual_manager = ltw.ActualManager(relative_manager)

    position_manager = ec.ToolDict([relative_manager, actual_manager])

    image_hooker = ecb.Sequential([
        ImreadHooker(),
        etb.PositionCropper(key='interface', position_manager=actual_manager),
    ])

    cropper = ltc.CropperManager(actual_manager, build_names=[
        'inventory', 'stats',
        # 'health_bar', 'mana_bar',
        'champion', 'champion_level',
        'current_health', 'total_health',
        'current_mana', 'total_mana', 'indicator'
    ])

    position_manager.update()
    image_hooker.update()
    cropper.update()

    image = image_hooker.use('./temp/examples/lux_1920_1080_minimap_on_left_scale_0.23_skill_points1000_dmg_q_88.png')
    result = cropper.use(image)

    save_crops(image, './temp/crops/interface.png')
    save_crops(result, './temp/crops/')
    return result


def tesserocr_test():
    import lodca
    import epta

    crops = mappers_test()
    del crops['rune_stats']
    cfg = lodca.configs.app_configs.TesserocrConfig()

    names_to_get = ['stats', 'champion_level']

    selective_tool = lodca.tools.recognition.tesserocr_rec.TessTool(cfg)
    result = selective_tool(crops, names_to_get)
    result = selective_tool(crops, [])
    numeric_tool = lodca.tools.recognition.tesserocr_rec.ToNumeric()
    result = numeric_tool(result)
    import json
    print(json.dumps(result, indent=4))
    tool_2 = epta.core.base_ops.Sequential([
        selective_tool,
        numeric_tool
    ])
    result = tool_2(crops)
    return result


def template_test():
    import lodca

    import lodca.tools.mappings.mappers as ltm

    cfg = lodca.configs.app_configs.GameConfig()
    cfg.settings.scale = 0.23
    cfg.settings.minimap_on_left = True

    relative_manager = ltm.RelativeManager(cfg)

    cfg = lodca.configs.app_configs.ItemTemplateConfig()

    template_tool = lodca.tools.recognition.template_rec.TemplateRecognition(relative_manager, config=cfg, key='item')
    relative_manager.update()
    template_tool.update()

    crops = mappers_test()

    result = template_tool.use_on_1d_dict(crops['inventory'])  # , names=['item_0'])
    return None


def player_layout_test():
    import lodca
    import epta
    cfg = lodca.configs.app_configs.AppConfig()
    cfg.game_config.settings.scale = 0.5
    cfg.game_config.settings.minimap_on_left = True
    cfg.game_config.settings.champion = 'Evelynn'

    layout = lodca.tools.layouts.LayoutManager(cfg)

    # select names to process for tess ocr
    player_tess_names = [
        'stats', 'additional_stats',
        'rune_stats',
        # 'health_bar', 'mana_bar',
        'champion_level',
        'current_health', 'total_health',
        'current_mana', 'total_mana',
    ]
    image_path = './temp/examples/ezreal_1920_1080_minimap_on_left_scale_0.5.png'
    image = epta.tools.hookers.image_hookers.ImreadHooker.hook_image(image_path)
    result = layout.use(image_path,
                        tools_kwargs={'tess': {'names': player_tess_names}})

    # cache testing
    cfg.game_config.settings.champion = 'Luxa'
    player_tess_names = [
        'stats'
    ]
    # deactivate item recognition
    result = layout.use(image_path,
                        tools_kwargs={'tess': {'names': player_tess_names}, 'item': None})

    # default layout created only.
    # links are {'default': Default, 'Evelynn': Default, 'Luxa': Default}
    assert len(layout) == 3

    import json
    print(json.dumps(result, indent=4))

    return layout


def target_layout_test():
    import lodca
    import epta
    cfg = lodca.configs.app_configs.AppConfig()
    cfg.game_config.settings.scale = 0.23
    cfg.game_config.settings.minimap_on_left = True

    layout = lodca.tools.layouts.LayoutManager(cfg, target=True)

    image_path = './temp/examples/lux_1920_1080_minimap_on_left_scale_0.23_skill_points2000_dmg_q_252.png'
    image = epta.tools.hookers.image_hookers.ImreadHooker.hook_image(image_path)
    result = layout.use(image_path)

    import json
    print(json.dumps(result, indent=4))
    return layout


def timings_test():
    import time
    import epta
    pl, tg = player_layout_test(), target_layout_test()
    q = time.time()
    image = epta.tools.hookers.image_hookers.ImreadHooker.hook_image(
        './temp/examples/lux_1920_1080_minimap_on_left_scale_0.23_skill_points2000_dmg_q_252.png')
    for i in range(50):
        tg.use(image)
        pl.use(image)
    print('total mean fps:', (time.time() - q) / 50)  # 0.48 p+p


if __name__ == '__main__':
    mappers_test()
    target_mappers_test()
    tesserocr_test()
    template_test()
    player_layout_test()
    target_layout_test()
    pass
    # timings_test()
