from dataclasses import dataclass
from enum import Enum
from typing import Union, NamedTuple, List
from flask import Flask, request, Response, jsonify
import math

# SpaceCowboy models a cowboy in our super amazing system
@dataclass
class SpaceCowboy:
    name: str
    lassoLength: int

# SpaceAnimal models a single animal in our amazing system
@dataclass
class SpaceAnimal:
    # SpaceAnimalType is an enum of all possible space animals we may encounter
    class SpaceAnimalType(Enum):
        PIG = "pig"
        COW = "cow"
        FLYING_BURGER = "flying_burger"

    type: SpaceAnimalType

# SpaceEntity models an entity in the super amazing (ROUND UPPER 100) system
@dataclass
class SpaceEntity:
    class Location(NamedTuple):
        x: int
        y: int

    metadata: Union[SpaceCowboy, SpaceAnimal]
    location: Location

# ==== HTTP Endpoint Stubs ====
app = Flask(__name__)
space_database: List[SpaceEntity] = []

# the POST /entity endpoint adds an entity to your global space database
@app.route('/entity', methods=['POST'])
def create_entity():
    # TODO: implement me
    json_data = request.get_json()
    for entity in json_data['entities']:
        new_space_entity = SpaceEntity(None, None)
        newMetadata = None
        if entity['type'] == 'space_cowboy':
            newMetadata = SpaceCowboy(entity['metadata']['name'], entity['metadata']['lassoLength'])
            # new_space_cowboy.name = entity['metadata']['name']
            # new_space_cowboy.lassoLength = entity['metadata']['lassoLength']
            
        elif entity['type'] == 'space_animal':
            newMetadata = SpaceAnimal(entity['metadata']['type'])
            # new_space_animal.type = entity['metadata']['type']
            
        new_space_entity = SpaceEntity(newMetadata, SpaceEntity.Location(entity['location']['x'], entity['location']['y']))
        # new_space_entity.location = SpaceEntity.Location(entity['location']['x'], entity['location']['y'])
        space_database.append(new_space_entity)

    return Response(status=200)

# lasooable returns all the space animals a space cowboy can lasso given their name
@app.route('/lassoable', methods=['GET'])
def lassoable():
    # TODO: implement me
    cowboyName = request.args.get('cowboy_name')
    cowboy = [x for x in space_database if isinstance(x.metadata, SpaceCowboy) and x.metadata.name==cowboyName][0]
    animal_candidates = list(filter(lambda x: isinstance(x.metadata, SpaceAnimal), space_database))

    response_list = []
    for candidate in animal_candidates:
        distance = math.sqrt( ((cowboy.location.x-candidate.location.x)**2)+((cowboy.location.y-candidate.location.y)**2) )
        if distance <= cowboy.metadata.lassoLength:
            response_list.append({
                "type": candidate.metadata.type,
                "location": {
                    "x": candidate.location.x,
                    "y": candidate.location.y
                }
            })

    return jsonify({'space_animals': response_list}), 200

# DO NOT TOUCH ME, thanks :D
if __name__ == '__main__':
    app.run(debug=True, port=8080)