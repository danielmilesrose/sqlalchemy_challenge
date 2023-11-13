# sqlalchemy_challenge
Module 10 SQLAlchemy Challenge -- UC Berkeley Data Analysis
\
\
In this challenge, we have used Python and SQLAlchemy to analyze climate data from Honolulu, HI in preparation for a vacation.
We have also used Pandas and Matplotlib to analyze various data points from the set.  We looked at precipitation over the past
year and created a graph to visualize this data.\
\
We also analyzed the data we had from all the different weather stations around Honolulu, finding the most active station to
determine the lowest, average, and highest temperatures recorded at that station in the past year.  From there, we have
created a histogram to visualize the frequency of observed temperatures at that station in the past year.\
\
Once that was complete, we created a Climate Analysis app using Flask.  On that app, we have created a number of pages that
return JSON data to the user.  We created a page that shows the precipitation data from the past year, another that shows all
of the weather stations in the area, a page that has the temperature observation data from our most active station from the past
year, and finally, two pages that show the minimum, average, and high temperatures; one from a specified start-date through the
end of the data, and another that gives values from a specified start-date to a specified end-date.\
\
References:\
DateTime reference -- https://www.nbshare.io/notebook/510557327/Strftime-and-Strptime-In-Python/
