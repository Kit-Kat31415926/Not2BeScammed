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