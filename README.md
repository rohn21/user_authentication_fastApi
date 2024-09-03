# user_authentication_fastApi

## Objective
  APIs for user registration, login, linking an ID, and implementing joins and chain delete functionality using Python, FastAPI and MongoDB.

### Framework and Libraries
- Utilized FastAPI for the web framework.
- Used PyMongo for interacting with MongoDB anlongwith Pydantic library for data validation.

### API Endpoints and Functionalities
- **Registration API**: Endpoint to register a new user with addition to password hash security.
- **Login API**: Endpoint to authenticate an existing user.Credentials are Email and Password.
- **Linking ID API**: Endpoint to link an ID to a user's account.The ID linked to the user_id will associated with that user.ID represents Subscription_ID, Membership_ID, etc. 
- **Joins**: Implemented functionality to join data from multiple collections.Used Aggregate method to filter data froom two collections , User and Prodcuts.
- **Chain Delete**: Implemented functionality to delete a user and all associated data across collections.

### Database
- MongoDB to store user information.


## Setup and Installation

  To clone the repo paste this code in terminal at your project directory
  ```bash
    git clone https://github.com/rohn21/user_authentication_fastApi.git
  ```

  go to project directory
  ```bash
    cd user_authentication_fastAPi
  ```
  For installation first setup virtual environment then install the requirements

  To install requirements

  ```bash
    pip install -r requirements.txt
  ```

  For Database Setup

  To setup locally install try MongoDB from [MongoDB Community Server](https://www.mongodb.com/try/download/community) or you can setup mongoDB compass at [MongoDB Atlas Cloud Database](https://www.mongodb.com/try) for Cloud database by creating cluster.
  - after completing this steps change credentials in `.env` file.

  ```bash
    DB_NAME=<database_name>
  ```
  for database connection paste your MongoDB Cloud Database cluster_string

  ```bash
    MONGODB_CONNECTION_URI=<provided_connection_string>
  ```
  OR for the localhost server

  ```bash
    MONGODB_CONNECTION_URI=mongodb://localhost:27017
  ```
## To start the server

  FastApi server with ASGI implementation
  ```bash
    fastapi run main.py
  ```


## Useful Api endpoints
  
  API docs (fastApi Swagger UI) for better GUI interface
  ```bash
    http://127.0.0.1:8000/docs
  ```
  API documentation with OpenApi
  ```bash
    http://127.0.0.1:8000/redoc
  ```


### Techstack
- Python
- FastAPI
- MongoDB