#Contributions

If you would like to contribute to the repository or use the repository for your own scientific reasons:

-   Fork the repository & clone the repository to your local computer

-   (OPTIONAL) Install virtual environment `pip install virtualenv`

-   (OPTIONAL) Create a virtualenv `virtualenv -p python3 env`

-   (OPTIONAL) Activate the virtualenv `source env/bin/activate`

-   Install the necessary python libraries `pip install -r requirements.txt`

-   Export the database url: `export DATABASE_URL="postgresql://user:password@localhost/database"`

-   Change directory to flaskapp `cd flaskapp`

-   Initialize the database `python manage.py db init`

-   Migrate the database `python manage.py db migrate`

-   Upgrade the database `python manage.py db upgrade`

-   Go back to home directory `cd ..`

-   Add cameras to the database: `cd csv_data` THEN `python csvtopostgres.py`
		(If that does not work, use setup.txt and copy the command to directly add cameras: `psql -c "\copy cameras FROM '/your/full/path/to/data.csv' delimiter ',' csv header"`)

-   Go back to home directory `cd ..`

-   Run imagedownloader to capture images `cd flaskapp` THEN `python imagedownload.py`

-   Run the flask app and visit the url `python manage.py runserver` THEN visit the [url](http://localhost:5000/)