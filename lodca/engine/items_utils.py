import epta.core.base_ops as ecb


# if items are not present - return None
# if present - update all
def _temp(data: dict, ln: str, sn: str, database: 'DataBase'):
    if ln not in data:
        return None
    else:
        v = data[ln]
        if v is None:
            return {sn: None}
        else:
            result = {sn: database.get(v.get('name', 'default'))}
            return result


def build_ocr_getters(database: 'DataBase'):
    def _build_item_getter(lookup_name: str, store_name: str, default_value=None):
        tool_ = ecb.Compose(
            _temp,
            (
                ecb.Lambda(lambda data, *args, **kwargs: data),
                lookup_name,
                store_name,
                database
            ),
            name=f'ocr_{store_name}'
        )

        return tool_

    ocr_items_getters = [
        *[
            _build_item_getter(key, key) for key in [
                f'item_{i}' for i in range(6)
            ]
        ],
    ]
    return ocr_items_getters
