from django.http import JsonResponse
import requests
from treeDetails.models import TreeSpeciesDetail

def get_tree_details(request, title, circumference):
    # Construct the Wikipedia API URL
    wikipedia_api_url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&titles={title}&prop=extracts&exintro&explaintext"
    
    # Make a GET request to the Wikipedia API
    response = requests.get(wikipedia_api_url)
    data = response.json()

    # Extract page details from the API response
    page_id = next(iter(data['query']['pages']))
    page_details = data['query']['pages'][page_id]

    try:
        # Try to fetch the tree species detail from the database
        tree_species = TreeSpeciesDetail.objects.get(specie_name=title)
        growth_factor = tree_species.specie_growth_factor
    except TreeSpeciesDetail.DoesNotExist:
        # If tree species detail not found, use default growth factor
        growth_factor = 1.0  

    # Calculate the age of the tree based on its circumference and growth factor
    circumference = float(circumference)
    age = round((circumference/3.14), 2)  # Assuming circumference is in inches
    age = age * float(growth_factor)

    # Format the response
    formatted_response = {
        "title": page_details['title'],
        "description": page_details['extract'],
        "tree age": str(round(age, 2))  # Format age to 2 decimal places
    }

    # Return the formatted response as JSON
    return JsonResponse(formatted_response)



