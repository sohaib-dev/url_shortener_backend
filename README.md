# url_shortener_backend
Implemented URL shortener using Python

### Dependencies

Install the Project dependencies

    pip install -r requirements.txt

### Run Project
- To run the project, Go to the short_link folder and run the following command.

  
    cd short_link/
    python manage.py runserver

### Encode/Decode API

- Encode API convert the URL to short-url link and will return into the response. 
    
  - Method: POST
  - Endpoint: /shorturl/encode/
  - Payload: {'original_url': 'google.com'}


- Decode API convert the short-url link back to the URL. 
  - Method: POST
  - Endpoint: /shorturl/decode/
  - Payload: {'short_url': 'short_url_string'}

### Run Test

- To run the test cases use the following command


    python manage.py test
    