# e-commerce-data-aggregator

Small project using microservice architecture for uploading a file containing sales records in one service
and send this information to another service to store it and show the aggregated information when the user send a request to
this second service.


# How to use

It's necessary to have docker installed in your computer, in the root of the project run the
following command.

    docker-compose up --build

In order to generate a csv file for test the api, you can use the script csv_generator.py, be sure to have the datetime
library installed, and run the python command like this

    python csv_generator.py

# APIS

POST | /sales | Send the csv file to the server

Response
{
    'message': 'File successfully uploaded and its being processed',
}

Curl example

    curl -X POST -F 'file=@files.csv' http://localhost:5002/sales

GET | /monthly_sales | Gets the sales aggregated by month

Response
[
    {
        "date": "10/2024",
        "price": 1900.00
    }
]

Curl example
    
    curl -X GET http://localhost:5003/monthly_sales
