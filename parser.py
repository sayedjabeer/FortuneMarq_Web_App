from bs4 import BeautifulSoup

def parse_semrush_html(html_content):
    # Parse the HTML content provided by the file upload
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove script and style elements to clean the text
    for element in soup(["script", "style", "nav", "footer"]):
        element.decompose()

    # Extract clean text from the body
    text = soup.get_text(separator=' ', strip=True)
    
    # We take a significant chunk of text for the AI to analyze
    # Focusing on the first 10,000 characters to keep it within token limits
    return text[:10000]

if __name__ == "__main__":
    print("Parser logic ready.")
