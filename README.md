# AMOS - The Archive of Many Outdoor Scenes

### What is AMOS?

-   A collection of long-term time lapse imagery from publicly accessible outdoor web cams around the world
-   Explore how to use these images to learn about the world around us
-   Understanding changes in natural environments and understanding how people use public spaces

### How does AMOS work?

-   This dataset is unique in that it contains images from significantly more scenes than in previous work
-   Images from each camera are captured several times per hour using a custom web crawler
-   We use the format **yyyymmdd_hhmmss.jpg** (4 digits for year, and 2 digits each for month, day, hour minute, and second)

### AMOS Beginnings

-   Began in March 2006 and is maintained by [Robert Pless](http://research.engineering.wustl.edu/~pless) at Washington University and now at the George Washington University
-   For more information visit the [old website](http://amos.cse.wustl.edu/) while the new one gets built!

### Comments and Updates

If you would like to contribute to the repository:

-   Fork the repository
-   Install virtualenv `pip install virtualenv`
-   Create a virtualenv `virtualenv -p python3 env`
-   Activate the virtualenv `source env/bin/activate`
-   Install the necessary python libraries `pip install -r requirements.txt`
-   Export the database url: `export DATABASE_URL="postgresql://user:password@localhost/database"`
-   Change directory to flaskapp `cd flaskapp`
-   Initalize the database `python manage.py db init`
-   Migrate the database `python manage.py db migrate`
-   Upgrade the database `python manage.py db upgrade`

-   Go back to home directory `cd ..`
-   Add cameras to the database: `cd csv_data` & `python csvtopostgres.py`
-   If that does not work, use setup.txt and copy the command to directly add cameras: `psql -c "\copy cameras FROM '/your/full/path/to/data.csv' delimiter ',' csv header"`

-   Go back to home directory `cd ..`
-   Run imagedownloader to capture images: `cd flaskapp` & `python imagedownload.py`

-   Run the flask app and visit the url: `python manage.py runserver` & visit the [url](localhost:5000)

    ### Future Goals:

-   Integrate with [Google Vision API](https://cloud.google.com/vision/)
-   Able to rate images on _wow factor_
-   Take webcams with already stored data and link to them
