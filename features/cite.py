def format_author_names(authors):  
    """  
    Convert full author names to APA style with initials.  
    """  
    formatted_authors = []  
    for author in authors.split(' and '):  
        parts = author.split(', ')  
        last_name = parts[0]  
        first_names = parts[1].split() if len(parts) > 1 else []  
        initials = ' '.join(f"{name[0]}." for name in first_names)  
        formatted_authors.append(f"{last_name}, {initials}")  
    return ' & '.join(formatted_authors)  
  
def format_apa_citation(entry):  
    # Format author names  
    authors = format_author_names(entry.get('author', 'No author'))  
      
    # Extract year, default to "n.d." (no date) if missing  
    year = entry.get('year', 'n.d.')  
      
    # Extract title, default to "Untitled" if missing  
    title = entry.get('title', 'Untitled')  
      
    # Extract journal, default to "No Journal" if missing  
    journal = entry.get('journal', 'No Journal')  
      
    # Extract volume and number, providing default empty strings  
    volume = entry.get('volume', '')  
    number = entry.get('number', '')  
      
    # Extract pages, default to "pp. unknown"  
    pages = entry.get('pages', 'pp. unknown')  
      
    # Construct the citation  
    citation = f"{authors} ({year}). {title}. {journal}"  
      
    # Add volume and number if present  
    if volume:  
        citation += f", {volume}"  
        if number:  
            citation += f"({number})"  
      
    # Add pages  
    citation += f", {pages}."  
      
    return citation  
  
# Example usage with author initials  
entry = {  
    'author': 'Doe, John and Smith, Jane',  
    'year': '2023',  
    'title': 'Sample Title',  
    'journal': 'Journal of Examples',  
    'volume': '10',  
    'number': '2',  
    'pages': '123-234'  
}  
  
# Generate the APA citation  
print(format_apa_citation(entry))  
