<p align="center"><img src="https://raw.githubusercontent.com/gwcvl/AMOSEast/master/flaskapp/static/logo.png" width="128px"><p>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
![Python](https://img.shields.io/badge/python-v3.6-blue.svg)
![Dependencies](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)
[![GitHub Issues](https://img.shields.io/github/issues/anfederico/flaskex.svg)](https://github.com/gwcvl/AMOSEast/flaskex/issues)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

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

### Future Goals:

-   Integrate with [Google Vision API](https://cloud.google.com/vision/)
-   Able to rate images on _wow factor_
-   Take webcams with already stored data and link to them
- 	Able to map and cluster all the stored webcams
