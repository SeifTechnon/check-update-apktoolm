import requests
from bs4 import BeautifulSoup
import re

# Define the URL
url = "https://maximoff.su/apktool/?lang=en"

# Add User-Agent header to simulate a real browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

# Local HTML file
html_file_path = "test.html"

# Send request to the website with the headers
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Use BeautifulSoup to parse the HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the <a> element that contains the version number
    version_link = soup.find('a', id='load_link')  # Based on the 'load_link' ID
    
    if version_link:
        # Extract the text containing the version number
        version_text = version_link.text.strip()
        # Use regular expression to extract the pattern "v?.?.?"
        match = re.search(r'\d+\.\d+\.\d+', version_text)
        if match:
            formatted_version = match.group(0)
            
            # Read the local HTML file
            with open(html_file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
            
            # Parse the local HTML content using BeautifulSoup
            local_soup = BeautifulSoup(html_content, 'html.parser')
            
            # Find the element that contains the text "Version:"
            version_div = local_soup.find('div', class_='app-version')
            
            if version_div and 'Version:' in version_div.text:
                # Update the text inside the element
                version_div.string = f"Version: {formatted_version}"  # Remove 'v'
                
                # Write the changes to the same file
                with open(html_file_path, 'w', encoding='utf-8') as file:
                    file.write(str(local_soup))
                
                print(f"Version updated to: {formatted_version}")
            else:
                print("The element containing the text 'Version:' was not found.")
        else:
            print("The version number in the required format was not found.")
    else:
        print("The version link was not found.")
else:
    print(f"Failed to access the website. Status code: {response.status_code}")
