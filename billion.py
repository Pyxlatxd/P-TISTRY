from pyzotero import zotero
import requests
import xml.etree.ElementTree as ET

# Replace with your actual Zotero user ID and API key
ZOTERO_USER_ID = '16253015'  # Replace with your actual user ID
ZOTERO_API_KEY = 'RkvNxbPOBgF9LHgCZ8NJRQLL'  # Replace with your actual API key

# Function to fetch data from PubMed by PMID
def fetch_pubmed_data(pmid):
    url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={pmid}&retmode=xml'
    response = requests.get(url)
    if response.status_code == 200:
        return response.text  # XML response
    else:
        print(f"Error fetching data from PubMed: {response.status_code}")
        return None

# Function to fetch data from CrossRef by DOI
def fetch_crossref_data(doi):
    url = f'https://api.crossref.org/works/{doi}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # JSON response
    else:
        print(f"Error fetching data from CrossRef: {response.status_code}")
        return None

# Function to parse PubMed XML data
def parse_pubmed_data(xml_data, pmid):
    root = ET.fromstring(xml_data)
    docsum = root.find('DocSum')
    
    # Extract metadata fields
    title = docsum.find("Item[@Name='Title']").text
    authors = docsum.find("Item[@Name='AuthorList']").text  # This can be a list of authors or None
    journal = docsum.find("Item[@Name='Source']").text
    pub_date = docsum.find("Item[@Name='PubDate']").text

    # Clean up the author list and handle cases where authors are not separated by commas
    authors_list = []
    if authors:
        authors_list = [author.strip() for author in authors.split(',')]

    # Prepare the Zotero item data
    return {
        'itemType': 'journalArticle',
        'title': title,
        'creators': [{'creatorType': 'author', 'name': author} for author in authors_list],  # Handle authors list
        'publicationTitle': journal,
        'date': pub_date,
        'url': f'https://pubmed.ncbi.nlm.nih.gov/{pmid}/'  # Proper URL to PubMed article
    }

# Function to parse CrossRef JSON data
def parse_crossref_data(json_data):
    title = json_data['message']['title'][0]
    authors = ', '.join([author['given'] + ' ' + author['family'] for author in json_data['message']['author']])
    journal = json_data['message']['container-title'][0]
    date = json_data['message']['published-print']['date-parts'][0][0]
    doi = json_data['message']['DOI']
    
    # Prepare data in Zotero item format
    return {
        'itemType': 'journalArticle',
        'title': title,
        'creators': [{'creatorType': 'author', 'firstName': author.split(' ')[0], 'lastName': author.split(' ')[1]} for author in authors.split(', ')],
        'publicationTitle': journal,
        'date': date,
        'url': f'https://doi.org/{doi}'
    }

# Function to add item to Zotero
def add_item_to_zotero(item_data):
    # Initialize the Zotero client with correct credentials
    zot = zotero.Zotero(ZOTERO_USER_ID, 'user', ZOTERO_API_KEY)  # Pass your actual user ID and API key
    
    # Create the item and add to Zotero
    response = zot.create_items([item_data])
    return response

# Main function to handle importing based on data source
def import_to_zotero(identifier, source='pubmed', identifier_type='pmid'):
    if source == 'pubmed' and identifier_type == 'pmid':
        # Fetch PubMed data
        xml_data = fetch_pubmed_data(identifier)
        if xml_data:
            # Ensure pmid is passed correctly here
            item_data = parse_pubmed_data(xml_data, identifier)  # Pass identifier (PMID) to the function
            response = add_item_to_zotero(item_data)
            print("Item added to Zotero from PubMed:", response)

    elif source == 'crossref' and identifier_type == 'doi':
        # Fetch CrossRef data
        json_data = fetch_crossref_data(identifier)
        if json_data:
            item_data = parse_crossref_data(json_data)
            response = add_item_to_zotero(item_data)
            print("Item added to Zotero from CrossRef:", response)

# Example usage:
# 1. Import from PubMed using PMID
import_to_zotero('31596188', source='pubmed', identifier_type='pmid')

# 2. Import from CrossRef using DOI
import_to_zotero('10.1109/ACCESS.2020.2980056', source='crossref', identifier_type='doi')
