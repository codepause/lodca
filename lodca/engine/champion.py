class Champion:
    def __init__(self, name: str = None, meta_data: dict = None, skills: dict = None, combos: dict = None):
        self.name = name
        self.meta_data = meta_data or dict()
        self.skills = skills or dict()
        self.combos = combos or dict()
