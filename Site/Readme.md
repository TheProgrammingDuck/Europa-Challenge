# The Site
We opted to use Django as our webframework. As our model was made in python, integration was easy. Read WebWorldWindDocs.ipynb for details. All children of this folder and its contents fall under the MIT software license unless otherwise specified.

## Files to look out for

The most important files in this directory are: <br/>
1.) WPSsite/views.py, this file controls backend integration of our model with the site <br/>
2.) WPSsite/app.html. This file is where the magic happens. Most of our WebWorldWind code is in here. <br/>
3.) The WPSsite/static/js folder. The WebWorldWind code for our site is in here. We have also made minor alterations to LayerManager.js 
so that we have a search bar that meets our needs.


## Using this site locally

Using this site locally should be as simple as installing Django and adding the WebWorldWind src folder to
WPSsite/static/js/. To update to the most recent predictions simply run call_daily.py in /WPSsite/. Bear in mind
that if you are running this server locally you will have to do this everytime you wish to use the app as it won't update
automatically. If you are getting any bugs let us know and/or feel free to make pull requests!
