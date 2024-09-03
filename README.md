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

### Techstack
- Python
- FastAPI
- MongoDB 
