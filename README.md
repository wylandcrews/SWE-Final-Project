Sprint 1 Link: https://swe-final-project-004.herokuapp.com/
# Map It! by G-Recs
The Team: Wyland Crews, Fameda Hossain, Joseph Esfandiari, and Swarna Bharathi<br>
Industry Mentor: Manav Singhal
## What is Map It! ?
We have seen recommendation and map apps, but nothing bridges the gap between the two. What Map It! aims to do is recommend destination locations to visitors of our site using the weather at their current location. We hope users will enjoy our activities recommendation platform and have implemented the option for users to save their searched location to their profile. Users can do so by first registering to our app and then logging in.
## How We Built It
### APIs
- Google Places, Geocoding and Geolocation APIs
- Weather API
### Tools & Platforms
- Google Cloud
- Heroku
- GitHub
### Languages & Technologies
- Flask, SQLAlchemy
- PostgreSQL
- JavaScript, Python, HTML
- Bootstrap
### Linting
The following errors/warnings were disabled for reasons listed below:
- ```invalid-name```: The variable names in our files are either readable or self-explanatory.
- ```broad-except```: These are the same try-except blocks we saw in Milestone 2.
- ```invalid-envvar-default```: Only appears in app.run() line of app.py, which we have used in all previous Milestones.
- ```too-many-boolean-expressions```: Our program checks multiple fields of the payload to ensure that key fields are not empty, so multiple boolean expressions are needed.
- ```line-too-long```: Triggered only by lines containing URLs necessary for API calls. This is ignored because these URLs are necessary for their respective API calls.
- ```no-else-return```: In the get_photo() function of recommendation.py, there is a return statement where *None* is returned. This prevents a broken image from being displayed.
- ```consider-using-with```: Only seen in get_photo() when writing/overwriting placeImage.jpg. The current implementation works well and is relatively concise.
- ```consider-using-f-string```: Only seen in auth.py. The current implementation works properly and the change is not necessary.
- ```no-member```: Only seen in the classes used for our database. The logic is the same we have used for all previous milestones, so this warning is ignored.
- ```too-few-public-methods```: Only seen in the classes used for our database if only the self method is declared. There is no need to have more than 1 method in certain classes.
- ```unnecessary-pass```: Pass is needed in the event that the user is already logged in.
- ```unused-argument```: Argument is needed for use in another module.
## Challenges We Encountered
- The method used to encrypt the password for the registration and login page caused some difficulty in terms of how I was validating the user's inputted password on the login page and the encrypted password that was located in the database. The types of both passwords were different and there wasn't a clear cut solution to solve how to validate that they were equal. The method was later changed to hashing which proved to be a much more safe and easier way to extract and validate information as it was now methods defined in the user model.
- 
## Areas to be Improved
- Show more results to the user so that it can be saved to their profile. 
- Add more User Interface through React.
- Allow users to add an avatar to their profile page.
- Allow users to choose a date in the future to explore results for.
- Improve our Facebook and Google login capabilities.

