
#TODO: store in MongoDB?

class AbilityModel:
    def __init__(self, name, description):
        self.name = name
        self.description = description

class MechamonModel:

    def __init__(self,
                 name,
                 appearance,
                 description,
                 abilities = None):
        self.name = name
        self.appearance = appearance
        self.description = description
        if abilities is None:
            self.abilities = []
        else:
            self.abilities = abilities