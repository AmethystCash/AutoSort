

def open_door(material):
    door_mapper = {
        'plastic': 1,
        'glass': 2,
        'paper': 3,
        'misc': 4,
    }
    # you can use either this or some if/else
    
    print(f"opening the {material} door with number {door_mapper[material]}")