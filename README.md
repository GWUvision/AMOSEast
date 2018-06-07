# AMOS - The Archive of Many Outdoor Scenes

### What is AMOS?

-   A collection of long-term time lapse imagery from publicly accessible outdoor web cams around the world
-   Explore how to use these images to learn about the world around us
-   Understanding changes in natural environments and understanding how people use public spaces

### How does AMOS work?

-   This dataset is unique in that it contains images from significantly more scenes than in previous work
-   Images from each camera are captured several times per hour using a custom web crawler
-   We use the format **yyyymmdd_hhmmss.jpg** (4 digits for year, and 2 digits each for month, day, hour minute, and second), and the time stamp is in **GMT**

### AMOS Beginnings

-   Began in March 2006 and is maintained by [Robert Pless](http://research.engineering.wustl.edu/~pless) at Washington University and now at the George Washington University
-   For more information visit the [old website](http://amos.cse.wustl.edu/) while the new one gets built!

### To Use:

-   Currently working on a flask app integrating the database and the python program for the website

### Future Goals:

-   Integrate with [Google Vision API](https://cloud.google.com/vision/)
-   Able to rate images on _wow factor_
-   MD5 Hash for images
-   Take webcams with already stored data and link to them
