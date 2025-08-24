import requests
from langchain_core.tools import tool

@tool
def get_country_info(country_name: str) -> dict:
    """
    Retrieves detailed information about a country using its full name.
    Returns data like capital, neighboring countries (by their code), and currencies.
    """
    url = f"https://restcountries.com/v3.1/name/{country_name}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
         
        country_data = response.json()[0]
        
        return {
            "name": country_data.get("name", {}).get("common"),
            "capital": country_data.get("capital", [None])[0],
            "borders": country_data.get("borders", []),
            "currencies": country_data.get("currencies", {})
        }
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP Error: Country '{country_name}' was not found or the API returned an error."
    except Exception as e:
        return f"An unexpected error occurred: {e}"


@tool
def get_country_by_code(country_code: str) -> dict:
    """
    Retrieves information about a country using its alpha code (e.g., 'FRA', 'CHE').
    Very useful for finding details about neighboring countries.
    """
    url = f"https://restcountries.com/v3.1/alpha/{country_code}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        country_data = response.json()[0]
        
        return {
            "name": country_data.get("name", {}).get("common"),
            "capital": country_data.get("capital", [None])[0],
            "currencies": country_data.get("currencies", {})
        }
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP Error: Country code '{country_code}' is invalid or the API returned an error."
    except Exception as e:
        return f"An unexpected error occurred: {e}"