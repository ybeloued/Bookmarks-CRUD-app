from flask import Flask, render_template, request, json, jsonify
from bs4 import BeautifulSoup
from urllib2 import urlopen
import pymongo

app = Flask(__name__)

# MongoDB info stored in constants
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'client-database'
COLLECTION_NAME = 'webpage_data'

def mongo_connect():
    errors = []
    try:
        connection = pymongo.MongoClient('localhost', 27017)
        print "Mongo is connected!"
        return connection
    except:
        error = "Could not connect to MongoDB"
        print error
        errors.append(error)
        return {'error': errors}

def add_db_document(url):
    errors = []
    try:
        html_text = urlopen(url).read()
    except:
        error = "Unable to get URL. Make sure it's valid and try again."
        print error
        errors.append(error)
        return {'error': errors}

    # after successful url read, scrape urls for data:
    if html_text:
        soup = BeautifulSoup(html_text, "lxml")
        site_title = soup.title.string
        site_description = soup.html.head.find("meta", attrs={"name":"description"})
        # need to create new dicionary for each new item/iteration to be able to append to list later
        data = {
            'url': url,
            'description': site_description['content'] if site_description else "No description given",
            'title': site_title if site_title else "No title given"
        }
        
        # insert data to database
        try:
            connection = mongo_connect() #connect to MongoDB
            db = connection[DBS_NAME] # db name
            collection = db.webpage_data # db collectinon name
            # add record to collection if it doesn't already exist
            if collection.find_one({"url": url}) < 0:
                collection.save(data) # insert scraped data to db
                success = "Record Successfully Added!"
                print success
                return {'success': success}
            else:
                error = "Record already exists in database!"
                print error
                errors.append(error)
                return {'error': errors}
        except:
            error = "Unable to add record to database due to unrecognized error."
            print error
            errors.append(error)
            return {'error': errors}

def update_db_document(url, title, description):
    errors = []
    # update data to database
    try:
        connection = mongo_connect() #connect to MongoDB
        db = connection['client-database'] # db name
        collection = db.webpage_data # db collectinon name
        # check if document exist

        collection.update_one({"url": { "$eq": url }},{ '$set': {'title': title, 'description': description}  }) # update db document for which 'url' equals given url
        success = "Updated Successfully!"
        print success
        return {'success': success}

    except:
        error = "Unable to update due to unrecognized error."
        print error
        errors.append(error)
        return {'error': errors}


def remove_db_document(url):
    errors = []
    # insert data to database
    try:
        connection = mongo_connect() #connect to MongoDB
        db = connection['client-database'] # db name
        collection = db.webpage_data # db collectinon name
        # check if document exist

        collection.delete_one({"url": { "$eq": url }}) # delete db document for which 'url' equals given url
        success = "Removed Successfully!"
        print success
        return {'success': success}

    except:
        error = "Unable to remove from database due to unrecognized error."
        print error
        errors.append(error)
        return {'error': errors}

# Flask routes:
@app.route('/',)
def index():
    return render_template('index.html')

@app.route('/add_card', methods=['POST'])
def addCard():
    results = []
    # get form input data from jquery ajax request
    input_url = request.form.get('add-card')
    print "input: %s" % input_url
    results = add_db_document(input_url)
    return jsonify(results=results)

@app.route('/update_card', methods=['POST'])
def updateCard():
    results = []
    # get the json data from jquery ajax request
    input_url = request.json['url']
    title = request.json['title']
    description = request.json['description']
    print input_url
    print title
    print description
    results = update_db_document(input_url, title, description)
    return jsonify(results=results)

@app.route('/remove_card', methods=['POST'])
def removeCard():
    results = []
    # get the json data from jquery ajax request
    input_url = request.json
    print input_url
    results = remove_db_document(input_url)
    return jsonify(results=results)

@app.route("/webpage_data", methods=['GET'])
def webpage_data():
    """
    A Flask view to serve project data from
    MongoDB in JSON format.
    """

    # A constant (uppercase) that defines the record fields that we wish to retrieve
    FIELDS = {
        '_id': False, 'url': True, 'title': True,
        'description': True
    }

    # Open a connection to MongoDB using a 'with' statement such that the
    # connection will be closed as soon as we exit the 'with' statement
    with pymongo.MongoClient(MONGODB_HOST, MONGODB_PORT) as connection:
        # Define which collection we wish to access
        collection = connection[DBS_NAME][COLLECTION_NAME]
        # Retrieve a result set only with the fields defined in FIELDS
        # and limit the output results to 250
        webpage_data = collection.find(projection=FIELDS, limit=250)
        # Convert projects to a list in a JSON object and return the JSON data
        return json.dumps(list(webpage_data))
        


if __name__ == '__main__':
    app.run(debug='true')