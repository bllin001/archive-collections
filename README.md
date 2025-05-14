# Exploring Archive-It Collections: A Case Study of the 2013 Boston Marathon

## How to search in Archive-It?

Archive-It offers a web interface for searching collections, but programmatic access allows for more systematic data collection and analysis. This project implements a Python-based approach for searching Archive-It collections using web scraping techniques.

### Using the Python Library

To search Archive-It programmatically:

1. Use the `search_archive_collections()` function from the utility module:

```python
from code.id_collections import search_archive_collections

# Basic search example
result = search_archive_collections("boston marathon")

# Access the results
collection_count = result["count"]
collections = result["collections_data"]["collections"]

# Print collection information
for collection in collections:
    print(f"Collection: {collection['name']}")
    print(f"ID: {collection['id']}")
    print(f"URL: {collection['url']}")
```

2. Customize search parameters:

```python
# Advanced search with options
result = search_archive_collections(
    query="boston marathon",      # Search term
    save_to_file=True,            # Save results to JSON
    output_dir="../output",       # Output directory
    verbose=True                  # Print progress information
)
```

3. Results are saved as JSON files in the specified output directory, with filenames based on the search query (e.g., `boston_marathon_collections.json`).

### What the Search Returns

The search function extracts:
- Collection IDs
- Collection names
- Collection URLs

These results enable further exploration of archived web content related to specific events or topics. For additional metadata like URI counts, collection dates, or collector information, you would need to access the individual collection pages.


## How many collections are available?
There are three Archive-It collections related to the 2013 Boston Marathon bombing:

1. **Blasts in Boston Marathon** (ID: 3752) - Collected by Virginia Tech's Crisis, Tragedy, and Recovery Network since June 2013, containing 1 URI focusing on news about the bombings.

2. **2013 Boston Marathon Bombing** (ID: 3649) - Collected by Internet Archive Global Events since April 2013, containing 318 URIs including news articles, blogs, social media, and organizational websites related to the bombing and its aftermath.

3. **Boston Marathon Bombing: Twitter and RSS feeds** (ID: 3645) - Collected by Virginia Tech's Crisis, Tragedy, and Recovery Network since April 2013, containing 9,394 URIs harvested from Twitter feeds, Google news, and Reddit using Virginia Tech's URL harvesting tool.

These collections provide different perspectives and information sources about the event, with a total of 9,713 archived URIs.

## Collecting URIs from a specific Archive-It Collection

To collect the seed URIs from this collection, I used the [`aiu`](https://github.com/oduwsdl/aiu) Python library, which provides an `ArchiveItCollection` class that interfaces with the Archive-It API. This class allows for the extraction of metadata and URIs using methods such as `list_seed_uris()` or `return_all_metadata_dict()`.

During the process, I encountered an issue when calling these methods: the script raised a `KeyError: 'Seed URL'`. This error suggests that the CSV seed report returned by the API did not include the expected `"Seed URL"` column. As a result, the seed URIs could not be retrieved using the library.

This issue might be due to changes in the API, limitations in access, or discrepancies in the returned data format. Further debugging or alternative methods may be necessary to extract the URIs successfully.

---

While attempting to use the `list_seed_uris()` method, I encountered an error due to a missing "Seed URL" column in the Archive-It seed report CSV. As a result, the seed URIs could not be retrieved using the library. The issue appears to stem from changes or inconsistencies in the API response format.

For reference, the collection details are:

- **Collection ID:** 3649  
- **Collection Name:** 2013 Boston Marathon Bombing  
- **Collection URL:** [https://archive-it.org/collections/3649](https://archive-it.org/collections/3649)

Here is the full error message for debugging purposes:

```
Traceback (most recent call last):
  File "/Users/brianllinas/Library/CloudStorage/OneDrive-OldDominionUniversity/VMASC/Projects/archive-collections/code/test.py", line 30, in <module>
    print(aic.return_all_metadata_dict())
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/brianllinas/miniforge3/lib/python3.11/site-packages/aiu/archiveit_collection.py", line 575, in return_all_metadata_dict
    self.load_seed_metadata()
  File "/Users/brianllinas/miniforge3/lib/python3.11/site-packages/aiu/archiveit_collection.py", line 376, in load_seed_metadata
    seed_report_metadata = get_seed_metadata_from_seed_report(self.collection_id, self.session)
                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/brianllinas/miniforge3/lib/python3.11/site-packages/aiu/archiveit_collection.py", line 274, in get_seed_metadata_from_seed_report
    seed_metadata[ row["Seed URL"] ] = {}
                   ~~~^^^^^^^^^^^^
KeyError: 'Seed URL'
```
