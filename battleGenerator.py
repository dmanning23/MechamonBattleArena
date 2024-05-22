from langchain_openai import ChatOpenAI
from battleModel import AttackModel
from battleModel import BattleModel

class BattleGenerator():

    create_battle = {
        'name': 'create_battle',
        'description': 'Create a battle',
        'parameters': {
            "type": "object",
            "properties": {
                "setup":{
                    'type': 'string',
                    'description': "Before the battle begins, describe the match that is about to occur. Compare and contrast the strengths and weaknesses of each monster and how they might affect the outcome of this battle"
                },
                "attacks": {
                    'type': 'array',
                    "description": "A list of back and forth offensive and defensive actions between several Mechamon pocket monsters",
                    "items": {
                        "type": "object",
                        "description": "A single action in the battle",
                        'properties': {
                            'name': {
                                'type': 'string',
                                'description': 'Name of the pocket monster that is performing the action'
                            },
                            'description': {
                                'type': 'string',
                                'description': "A description of the action being performed"
                            },
                            'result': {
                                'type': 'string',
                                'description': "The result of the action"
                            },
                        },
                        "required": ["name", "description", "result"]
                    },
                },
                "climax":{
                    'type': 'string',
                    'description': "The final epic attack resulting in the climax of the battle"
                },
                "winner":{
                    'type': 'string',
                    'description': "The pocket monster that won the battle"
                },
            },
            "required": ["setup", "attacks", "climax", "winner"]
        }
    }

    def _create_battle(self, setup, attacks, climax, winner):
        #create the list of attacks
        attackList = []
        for attack in attacks:
            attackList.append(self._generate_attack(**attack))

        #create the battle object
        return BattleModel(setup, attackList, climax, winner)

    def _generate_attack(self, name, description, result):
        return AttackModel(name, description, result)
    
    def _parseResponse(self, response, available_functions):
        if response.tool_calls:
            for tool_call in response.tool_calls:
                function_name = tool_call['name']
                function_to_call = available_functions[function_name]
                return function_to_call(**tool_call['args'])
        else:
            return None
        
    def Battle(self, monster1, monster2, llm = None):
        if not llm:
            llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.6)

        messages = [
            {'role': 'system', 'content': f'Two Mechamon Pocket Monsters are having a battle. Given the following list of Mechamon in the battle and the abilities of each Mechamon, generate a furious battle between them. Make sure the battle includes an epic climax and a clear winner!'},
        ]

        messages.append({'role': 'system', 'content': f'The first Mechamon in the battle is {monster1.name}. {monster1.appearance} {monster1.description}'})
        for ability in monster1.abilities:
            messages.append({'role': 'system', 'content': f'{monster1.name} ability: {ability.name}: {ability.description}'})

        messages.append({'role': 'system', 'content': f'The second Mechamon in the battle is {monster2.name}. {monster2.appearance} {monster2.description}'})
        for ability in monster2.abilities:
            messages.append({'role': 'system', 'content': f'{monster2.name} ability: {ability.name}: {ability.description}'})

        available_functions = {
            "create_battle": self._create_battle,
        }

        llm_with_tools = llm.bind_tools(tools=[BattleGenerator.create_battle], tool_choice="required")
        response = llm_with_tools.invoke(messages)

        battle = self._parseResponse(response, available_functions)
        return battle