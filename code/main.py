import json
import os
from utils import *
from aiu import ArchiveItCollection


with open("../boston-collection-manual.json", "r") as f:
    data = json.load(f)
    
    
# Print as json dump
print(json.dumps(data, indent=4))

# Extract the collection id based on the a collection name
collection_id = get_id_from_collection(data, "2013 Boston Marathon Bombing")
print(f"Collection ID: {collection_id}")  # Should return the id of the item with name "Boston"

aic = ArchiveItCollection(collection_id=collection_id)

# Print available collection information
print(f"Collection Name: {aic.get_collection_name()}")
print(f"Collected By: {aic.get_collectedby()}")
print(f"Collection Description: {aic.get_description()}")
print(f"Collection URL: {aic.get_collection_uri()}")
print(f"Archived Since: {aic.get_archived_since()}")
print(f"Is Private: {aic.is_private()}")
print(f"Subject: {aic.get_subject()}")
print(f"Does it exist: {aic.does_exist()}")

# print(aic.return_all_metadata_dict())
# Get seed URIs
# seed_uris = aic.list_seed_uris()
# print(f"Number of Seed URIs: {len(seed_uris)}")

# # Get metadata for first seed URI (if available)
# if seed_uris:
#     first_seed = seed_uris[0]
#     print(f"First Seed URI: {first_seed}")
#     print(f"First Seed Metadata: {aic.get_seed_metadata(first_seed)}")


