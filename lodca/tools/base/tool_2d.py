import epta.core.base_ops as ecb


class Atomic2DTool(ecb.Variable, ecb.Atomic):
    """
    Wrapper for a tool to be used on a dictionary with 2 level of keys.
    """
    def __init__(self, name='SkillTool', **kwargs):
        super(Atomic2DTool, self).__init__(name=name, **kwargs)

    def use(self, data: dict, **kwargs):
        # converts 2d dict of data to 1d dict of results with an atomic key
        inp = data.get(self.key, {})
        result = dict()
        for key, value in inp.items():
            result[key] = self.tool(value)
        return result
