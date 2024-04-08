
class AttackModel():

    def __init__(self, mechamon, description, result):
        self.mechamon = mechamon
        self.description = description
        self.result = result

class BattleModel():

    def __init__(self, setup, attacks, climax, winner):
        self.setup = setup
        self.attacks = attacks
        self.climax = climax
        self.winner = winner