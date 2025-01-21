# SPA project 🗨️

<a id="readme-top"></a>

![Django DRF Logo](logos/django-rest.jpg)
![Redis Logo](logos/redis-image.svg)
![Prometheus Logo](logos/prometheus.png)
![Grafana Logo](logos/grafana.png)


This is a Django REST Framework (DRF) powered API for managing a Single Page Application (SPA) project. The API facilitates key functionalities of a social platform, including user accounts and comments. The project also incorporates JWT authentication for secure access, efficient database queries using Django ORM, and integrations with Prometheus and Grafana for performance monitoring. 


## Run service on your machine

1. Clone repository  
```shell
git clone https://github.com/dimak20/spa_project.git
cd group_api_project
```
2. Then, create and activate .venv environment  
```shell
cd backend
```
```shell
python -m venv venv
```
For Unix system
```shell
source venv/bin/activate
```

For Windows system

```shell
venv\Scripts\activate
```

3. Install requirements.txt by the command below  


```shell
pip install -r requirements.txt
```

4. Create a .env file with the required fields


5. Apply database migrations 
```shell
python manage.py migrate
```

6. Create superuser and run server

```shell
python manage.py createsuperuser
python manage.py runserver # http://127.0.0.1:8000/
```
7. Go to frontend directory

```shell
cd ../frontend
```
8. Install requirements

```shell
npm install
```

9. Create a .env file with the required fields


10. Run frontend server

```shell
npm run dev # http://127.0.0.1:5173/
```

## Run with Docker (simple version)

1. Clone repository  
```shell
git clone https://github.com/dimak20/spa_project.git
cd spa_project
```

2. Create .env files and set up environment variables in backend and frontend directories


3. Build and run docker containers 


```shell
docker-compose up --build
```


5. Access the API at http://localhost

<p align="right">(<a href="#readme-top">back to top</a>)</p>


6. Monitoring
```shell
Prometheus: http://localhost:9090
Grafana: http://localhost:3000
Redis-command: http://localhost:8081
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Project configuration

Your project needs to have this structure


```plaintext
Project
├── backend
│   ├── accounts
│   ├── comments
│   ├── files
│   ├── management_utils
│   ├── media
│   ├── spa_app
│   ├── static
│   ├── staticfiles
│   ├── .dockerignore
|   ├── .env.sample
|   ├── Dockerfile
|   ├── manage.py
│   └── requirements.txt
|
├── frontend
│   ├── public
│   └── src
│   ├── .dockerignore
|   ├── .env.sample
|   ├── Dockerfile
│   ├── index.html
|   ├── jsconfig.json
|   ├── package.json
|   ├── package-lock.json
│   ├── README.md
│   └── vite.config.js   
│   
├── logos
│   
├── nginx
|
│
│
├── .gitignore
│
├── docker-compose.yaml
│
├── prometheus.yml
|
└── README.md
```


## Usage
* Library Endpoints: Manage books.
* Checkout Endpoints: Create and manage checkouts/borrowings, make payments.
* User Endpoints: User registration, login, and token authentication.
* Payements Endpoints: Manually create payments or retrieve payment session details.
* Hint - use http://localhost:8000/api/v1/doc/swagger/ to see all the endpoints

## Features
* JWT Authentication
* Creating comments, users
* Filtering and ordering models by username, date, text etc.
* Redis usage for caching
* Prometheus usage for service monitoring
* Grafana for visualizing server usage
* Admin panel /admin/

<p align="right">(<a href="#readme-top">back to top</a>)</p>
