# Based on a name within the collection extract the id
def get_id_from_collection(data, name):
    for item in data["collections"]:
        if item["name"] == name:
            return item["id"]
    return None