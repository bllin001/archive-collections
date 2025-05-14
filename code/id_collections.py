import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import re
import json
import os


def search_archive_collections(query, save_to_file=True, output_dir="../output", verbose=True):
    """
    Search Archive-It for collections based on a query and extract collection information.
    
    Parameters:
    - query (str): The search query to use
    - save_to_file (bool): Whether to save results to a JSON file
    - output_dir (str): Directory to save the output file
    - verbose (bool): Whether to print detailed information during execution
    
    Returns:
    - dict: A dictionary containing:
        - collections_data: The complete collections data dictionary
        - count: Number of collections found
        - search_url: The URL used for searching
        - filepath: Path to the saved JSON file (if saved)
    """
    if verbose:
        print(f"Searching for collections with query: '{query}'")
    
    # Get each token in the query
    tokens = query.split(" ")
    
    # Create the url for searching in archive-it
    query_param = "+".join(tokens)
    search_url = f"https://archive-it.org/explore?q={query_param}&show=Collections"
    
    if verbose:
        print(f"Using search URL: {search_url}")
    
    try:
        # Extract the collection id for each result
        response = requests.get(search_url)
        response.raise_for_status()  # Will raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find all collection links
        collection_links = soup.find_all("a", href=re.compile(r"/collections/"))
        
        # Create a data structure to store the collection information
        collections_data = {
            "query": query,
            "search_url": search_url,
            "collections": []
        }
        
        # Extract the collection ids from the links
        for link in collection_links:
            href = link.get("href")
            if href:
                # Extract the collection id from the URL
                match = re.search(r"/collections/(\d+)", href)
                if match:
                    collection_id = match.group(1)
                    collection_name = link.text.strip()
                    collection_url = f"https://archive-it.org{href}"
                    
                    # Add the collection information to our data structure
                    collections_data["collections"].append({
                        "id": collection_id,
                        "name": collection_name,
                        "url": collection_url
                    })
                    
                    # Print for debugging/viewing purposes if verbose
                    if verbose:
                        print(f"Collection ID: {collection_id}")
                        print(f"Collection Name: {collection_name}")
                        print(f"Collection URL: {collection_url}")
        
        # Count collections found
        collection_count = len(collections_data["collections"])
        if verbose:
            print(f"\nTotal collections found: {collection_count}")
        
        # Save to file if requested
        filepath = None
        if save_to_file:
            # Create the output directory if it doesn't exist
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                if verbose:
                    print(f"Created output directory: {output_dir}")
            
            # Create a filename based on the query
            filename = f"{query.replace(' ', '_')}_collections.json"
            filepath = os.path.join(output_dir, filename)
            
            # Save the data to a JSON file
            with open(filepath, "w") as f:
                json.dump(collections_data, f, indent=4)
            
            if verbose:
                print(f"Data saved to {filepath}")
        
        # Return a dictionary with all the relevant information
        return {
            "collections_data": collections_data,
            "count": collection_count,
            "search_url": search_url,
            "filepath": filepath
        }
        
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return {
            "error": str(e),
            "collections_data": None,
            "count": 0,
            "search_url": search_url,
            "filepath": None
        }
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {
            "error": str(e),
            "collections_data": None,
            "count": 0,
            "search_url": search_url,
            "filepath": None
        }


# Example usage
if __name__ == "__main__":
    # Example with default parameters
    result = search_archive_collections("boston marathon")
    
    # Example with custom parameters
    # result = search_archive_collections(
    #     query="covid-19", 
    #     save_to_file=True, 
    #     output_dir="./data",
    #     verbose=True
    # )
    
    # Access returned data
    if "error" not in result:
        print(f"\nSearch complete: Found {result['count']} collections")
    else:
        print(f"\nSearch failed with error: {result['error']}")
