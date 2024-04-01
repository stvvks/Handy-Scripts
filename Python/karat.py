import requests

def download_file(url, save_path):
    # Send a GET request to the URL to download the file
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        # Save the contents of the response to a file
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print("File downloaded successfully.")
    else:
        print("Failed to download file.")

def read_books_and_pages(file_path):
    total_books = 0
    total_pages = 0
    
    # Open the file and read its contents
    with open(file_path, 'r') as file:
        for line in file:
            # Split each line into book title and number of pages
            book_title, pages_str = line.strip().split(',')
            # Convert pages_str to an integer
            pages = int(pages_str)
            # Increment total books and total pages
            total_books += 1
            total_pages += pages
            
    return total_books, total_pages

if __name__ == "__main__":
    # Define the URL of the file
    file_url = 'https://public.karat.io/content/test/test_file.txt'
    # Define the local file path to save the downloaded file
    local_file_path = 'test_file.txt'

    # Download the file from the URL
    download_file(file_url, local_file_path)

    # Read books and pages
    total_books, total_pages = read_books_and_pages(local_file_path)

    # Output the total number of books read and total number of pages read
    print("Total number of books read:", total_books)
    print("Total number of pages read:", total_pages)
