# Anime Recommender System (ARecSys)

#### Configure and Start Project
* Requirements:
    * Postgres==9.6 
* Create [conda](https://docs.conda.io/projects/conda/en/latest/index.html) Environment `conda create -n ARecSys python=3.6`
* Install Requirements `pip install -r requirements.txt`
* Create `ARecSys/local_settings.py` based on `ARecSys/local_settings.py.sample`
* Setup Postgres [Database](#Setting-up Database)
* `./manage.py makemigrations && ./manage.py migrate`
* `./manage.py runserver`
* Navigate to `http://localhost:8000`

#### Setting-up Database
* Start postgres `sudo -su postgres`
* Start PSQL `psql`
* `CREATE USER anime WITH PASSWORD 'anime@2020';`
* `CREATE DATABASE animeinfo;`
* `GRANT ALL PRIVILEGES ON DATABASE animeinfo TO anime;`

#### Accessing Admin Panel
* `./manage.py createsuperuser`
* `./manage.py runserver`
* Navigate to `http://localhost:8000/admin`

#### Creating New APPS
* `mkdir apps/name_of_app`
* `./manage.py startapp name_of_app apps/name_of_app`
* Register the app in ARecSys/settings.py file under `INSTALLED_APPS`