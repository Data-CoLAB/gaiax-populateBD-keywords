import requests
import json
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

logging.basicConfig(level=logging.INFO)

docs_resulting = {}
service_links = []

def fetch_service(cred):
    """Function to fetch service data."""
    service_id = cred.get('id', "")
    if not service_id:
        return None

    try:
        resp = requests.get(service_id, timeout=3)
        if resp.status_code == 200:
            return resp.json()
        else:
            return None
    except requests.RequestException as e:
        return None
    
def fetch_source(source):
    """Function to fetch source."""
    try:
        resp = requests.get(source, timeout=3)
        if resp.status_code == 200:
            return resp.json()
        else:
            return None
    except requests.RequestException as e:
        return None

def fetch_service_with_fallback(cred, source):
    """Function to fetch service with a fallback to source."""
    service_data = fetch_service(cred)
    if service_data is None:
        service_data = fetch_source(source)
    return service_data

def scrap_from_url(url: str):
    """Scrape from CES endpoint URL

    Parameters
    ----------
    url : str
        URL from CES endpoint
    """
    
    json_file = requests.get(url).json()

    credentials_to_fetch = []
    for doc in json_file:
        vc_id = doc.get('data', {}).get('id', "")
        source = doc.get('source', "")
        data = doc.get('data', {})
        if not isinstance(data, dict):
            continue

        credentials = data.get('credentialSubject', [])
        if not isinstance(credentials, list):
            continue

        for cred in credentials:
            if not isinstance(cred, dict):
                continue

            if cred.get('gx:type', "") == 'gx:ServiceOffering':
                credentials_to_fetch.append((cred, source, vc_id))

    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_cred = {executor.submit(fetch_service_with_fallback, cred, source): (cred, source, cred.get('id', ""), vc_id) for cred, source, vc_id in credentials_to_fetch}
        for future in as_completed(future_to_cred):
            cred, source, cred_id, vc_id = future_to_cred[future]
            try:
                result = future.result()
                if result:
                    results.append((vc_id,cred_id,result))
            except Exception as e:
                logging.error(f"Error fetching service for credential: {cred_id} with source: {source}, error: {e}")

    return results