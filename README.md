The repository is divided into three different microservices.
1. User authentication
2. Product management
3. Order processing
4. Task management

Things to do after taking pull of this repository:

1. Install python3 to the system.

2. Make an virtual environment in the repository with the command `python3 -m venv my_env`

3. Activate the virtual environment by the command `source my_env/bin/activate`

4. Install the required dependencies by `pip install -r requirements.txt`

5. A .env file has to made outside all the folders of the microservices. It will have `DATABASE_URL` in the format `postgresql://{username}:{password}@{ip_address}:{port}/{database_name}`

6. Run the microservices. They can be run in 4 seperate shells or in a sequential manner. To run use the commands, 
`python3 auth/main.py`, `python3 products/main.py`, `python3 orders/main.py`, `python3 tasks/main.py`.

7. Generate a secret key using the command `openssl rand -hex 32` outside of the path where servers might be running. Copy the ouput and replace it in the `config.py` file in all 3 microservices.

8. When the auth microservice is running, you will need to signup using an email, username and password in the `signup` endpoint. The password is stored as a hash, no worries there.

9. Once sign up is complete use the `login` endpoint by giving the username and password. Once the password is verified the reponse will be a token which has to be used for other microservices. 

Assumption:
- For requests to other microservices the auth token provided should be provided in the Authorization header as `Authorization: bearer YOUR_TOKEN`.
- All three microservices have been given different ports on the same address to run. If there is a need to change those it can be done from the `config.py` file in each of the folders represnting a microservice.

Once this is given then the endpoints will start working for a given user. 
A microservices-based system that manages a simple e-commerce application has been completed.

## Application specifics

The system handles user authentication, product management, and order processing. It ensures concurrency control.

The application includes functionailty for updating order status and deleting products.

There is feature implemented for filtering of orders based on their order status and sorting of orders based on their price or status of the orders.

A very detailed detailed and thorough error handling and validation checks have been put in place enhancing the robustness of the application.

Product creation has checks that title and description of product are atleast of a certain length after being trimmed of any extra whitespaces and valid errors are thrown to handle this.

Feature implemented to have sorting of products based on either their name or their price in ascending or descending order based on the user input.

Form provided to add a new task that includes fields for title, description, and status.

Functionality provided for updating task status and deleting tasks.

Task sorting based on status and Task filtering based on different status has been implemented.

API Rate Limiting and validation checks have been implemented for preventing abuse.

The application ensures that user interactions are smooth and responsive across all platforms.