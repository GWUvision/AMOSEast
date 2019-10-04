# AMOS - The Archive of Many Outdoor Scenes

## What is AMOS?

-   A collection of long-term time lapse imagery from publicly accessible outdoor web cams around the world
-   Explore how to use these images to learn about the world around us
-   Understanding changes in natural environments and understanding how people use public spaces

## How does AMOS work?

-   This dataset is unique in that it contains images from significantly more scenes than in previous work
-   Images from each camera are captured several times per hour using a custom web crawler
-   We use the format **yyyymmdd_hhmmss.jpg** (4 digits for year, and 2 digits each for month, day, hour minute, and second)


## Setup

Python version python3.6.6

-   pip install -r requirements.txt
-   Download Postgres (here)["https://www.postgresql.org/download/"]
    +   Installer - all default settings
    +   Choose admin password
-   Export database url on terminal
    +   `export DATABASE_URL="postgressql://postgres:password@localhost/postgres"`
-   Create tables for database
    +   `python manage.py db init`
    +   `python manage.py db migrate`
    +   `python manage.py db upgrade`
-   Run the server locally
    +   `python app.py`
    +   visit `localhost:5000`

