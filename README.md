# Backend

### Setup

1. Download [Python 3.9+](https://www.python.org/downloads/)

2. Create a [virtual environment](https://docs.python.org/3/library/venv.html) and activate it

    _Note: This will ensure all the required packages are not installed globally, but only in the environment_

3. Navigate (```cd```) to the ```Not2BeScammed``` directory. We will install the necessary dependencies using the ```requirements.txt``` file in the ```/backend``` directory by running the following:

        ```cd backend && pip install -r requirements.txt```

    _Note: This only needs to be done once after creating the virtual environment_

### Run

1. Ensure the virtual environment is activated [See Setup #2]. Navigate (```cd```) to the ```Not2BeScammed``` directory and run the following:

        ```cd backend && python app.py```

### Code Structure

- ```/model```
    - Contains the pickle files to our ML model

- ```app.py```
    - Contains all API endpoints
    - ```analyze()``` takes in an email message and returns the chance of being spam
    - ```simulate()``` takes in how many ham and spam the model should recieve. It then tests the model's abilities and returns the model's score.

- ```requirements.txt```
    - Contains all Python packages installed with pip to run the backend


# Frontend

### Setup

1. Install [node.js](https://nodejs.org/en/download)

2. Navigate (```cd```) to the ```Not2BeScammed``` directory and install the necessary dependencies by running the following:

        ```cd frontend && npm install```

### Run

1. Navigate (```cd```) to the ```Not2BeScammed``` directory and run the following:

        ```npm run dev```

    _Note: This script will ensure any changes to the frontend UI are automatically reflected on reload of the webpage_

2. Click the link that appears in the terminal ([localhost:5173](http://localhost:5173))

### Code Structure

- ```/public```
    - Contains all images to be displayed under ```/images```
    - Contains Fisher the robot under ```/fisher/source```
    - Contains all fonts used under ```/fonts```

- ```/src```
    - Contains all global styling under ```/assets```
    - Contains all routes and corresponding display components under ```/router```
    - Contains all pages views under ```/views```
    - Main app is displayed by ```App.vue``` and ```main.ts```

- The rest of the files under ```/frontend``` contain configurations necessary for imports and running the frontend.

