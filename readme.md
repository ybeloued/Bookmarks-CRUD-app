## Bookmark CRUD App

This is a bookmarking app for storing useful urls in a card format with the webpage's title and description. The user has the ability to open the link in a new tab. Also, any card can have it's title and description then edited, or the card can be removed from the list.

The app uses async HTTP requests to communicate with the server for adding, removing, and saving of cards as well as scraping the webpage's information for its title and description and then saving the information in a database.

Initial data was obtained and stored in MongoDB using my python webpage scraper available [here](https://github.com/sebam2k4/webpage-scraper) it takes a csv file with urls and scrapes each for title and description. It then saves the results in a MongoDB collection.

### Tech Used:
Flask
Urllib
Pymongo
jQuery 3.2.1
Bootstrap 3.3.7
Beautiful Soup 4

### ToDo:
- look into jquery ajax error handling
- see if flask/python error handling can be improved
- figure out how to revert edited card title and/or description text back to original on edit cancel
- Read more about HTTP responses: GET, POST, PUT, DELETE
- Security?

### Features to Add:
- tags and filtering - for starters could just do text input field search
- set a limit to amount of documents that can be stored in db
- Find a way to prevent or minimize inappropriate urls from being stored in db and displayed in front-end
- User accounts and an instance of coding resource bookmarks collection.

### Bugs:
- When addings a card, some urls do not work returning 'invalid url' error. This may be due to text encoding. Needs further investigation

### used help from these pages:

https://stackoverflow.com/questions/10434599/how-to-get-data-received-in-flask-request
https://stackoverflow.com/questions/19794695/flask-python-buttons