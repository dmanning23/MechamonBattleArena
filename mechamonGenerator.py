from mechamonModel import MechamonModel
from mechamonModel import AbilityModel
from langchain_openai import ChatOpenAI

class MechamonGenerator:

    # 'description': "A list of comma separated values for MidJourney describing the appearance of this pocket monster"
    # 'description': "A description of the appearance of this pocket monster"

    generate_mechamon = {
        'name': 'generate_mechamon',
        'description': 'Create a single Mechamon pocket monster',
        'parameters': {
            "type": "object",
            "properties": {
                "name":{
                    'type': 'string',
                    'description': "The name of this pocket monster"
                },
                "appearance":{
                    'type': 'string',
                    'description': "A list of comma separated values for MidJourney describing the appearance of this pocket monster"
                },
                "description":{
                    'type': 'string',
                    'description': "Some flavor text for this pocket monster"
                },
                "abilities": {
                    'type': 'array',
                    "description": "A list of the offensive and defensive abilities of the pocket monster",
                    "items": {
                        "type": "object",
                        "description": "A single offensive or defensive capability of the pocket monster",
                        'properties': {
                            'name': {
                                'type': 'string',
                                'description': 'Name of the ability'
                            },
                            'description': {
                                'type': 'string',
                                'description': "A short description of the ability"
                            },
                        },
                        "required": ["name", "description"]
                    },
                },
            },
            "required": ["name", "appearance", "description", "abilities"]
        }
    }

    def _generate_mechamon(self, name, appearance, description, abilities):
        abilityList = []
        for ability in abilities:
            abilityList.append(self._generate_ability(**ability))
        mechamon = MechamonModel(name, appearance, description, abilityList)
        return mechamon

    def _generate_ability(self, name, description):
        return AbilityModel(name, description)
    
    def _parseResponse(self, response, available_functions):
        if response.tool_calls:
            for tool_call in response.tool_calls:
                #Which function call was invoked?
                function_name = tool_call['name']

                #Call the function with the provided arguments
                function_to_call = available_functions[function_name]
                return function_to_call(**tool_call['args'])
        else:
            #The LLM didn't call a function but provided a response
            #return response_message.content
            return None
    
    def Generate(self, shortDescription, llm = None):
        if not llm:
            #create the client API
            llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.4)

        #Add all the messages
        messages = [
            {'role': 'system', 'content': "Given the following short description, create a complete Mechamon Pocket Monster."},
            {'role': 'user', 'content': shortDescription}
        ]

        #Once the LLM chooses to call a function, this is the mapping to the Python method
        available_functions = {
            "generate_mechamon": self._generate_mechamon,
        }

        #Bind the tools and call the LLM
        llm_with_tools = llm.bind_tools(tools=[MechamonGenerator.generate_mechamon], tool_choice="required")
        response = llm_with_tools.invoke(messages)

        #Parse the response from the LLM
        mechamon = self._parseResponse(response, available_functions)
        return mechamon
    
    def Merge(self, monster1, monster2, llm = None):
        if not llm:
            llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)

        messages = [
            {'role': 'system', 'content': f'Two Mechamon Pocket Monsters are merging into a third. Given the following list of Mechamon and the abilities of each Mechamon, generate third Mechamon with abilities that are a blended combination of the originals.'},
        ]

        messages.append({'role': 'system', 'content': f'The first Mechamon being merged is {monster1.name}. {monster1.appearance} {monster1.description}'})
        for ability in monster1.abilities:
            messages.append({'role': 'system', 'content': f'{monster1.name} ability: {ability.name}: {ability.description}'})

        messages.append({'role': 'system', 'content': f'The second Mechamon being merged is {monster2.name}. {monster2.appearance} {monster2.description}'})
        for ability in monster2.abilities:
            messages.append({'role': 'system', 'content': f'{monster2.name} ability: {ability.name}: {ability.description}'})

        available_functions = {
            "generate_mechamon": self._generate_mechamon,
        }
        
        llm_with_tools = llm.bind_tools(tools=[MechamonGenerator.generate_mechamon], tool_choice="required")
        response = llm_with_tools.invoke(messages)

        mechamon = self._parseResponse(response, available_functions)
        return mechamon