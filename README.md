# Readme for stock practice project
## Part 1:

1. ```git clone https://github.com/ohadkorenok/stock_quote_project```

2. ```cd stock_quote_project```

3. ```docker-compose build --no-cache```. If you don't have docker compose installed, you can install it through: ```pip install docker-compose``` or through [docker-compose official website](https://docs.docker.com/compose/install/) 

4. ``docker-compose up``

### Optional - Use postman to test the API easily:
5. open Postman and import `stocks_collection.json` file


## Part 2:

in a different folder: 
* ```git clone -b rate_limiter https://github.com/ohadkorenok/stock_quote_project.git```

* Same as steps 2-5 in Part 1



## Routes:

1. URL - `stocks/SYMBOL`: This route gets a stock symbol (for example `QQQ`) and returns a JSON object representing the stock data from Yahoo API

2. URL - `stocks/total_cost`: This route gets a GET request and returns the total cost of the queries to the 3rd part service since last reset. 

3. URL - `stocks/reset_cost`: This route gets a GET request and reset the cost counter correspondingly.


### Enjoy 

