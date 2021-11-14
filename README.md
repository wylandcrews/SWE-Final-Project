# Map It! by G-Recs
The Team: Fameda Hossain, Joseph Esfandiari, Swarna Bharathi, and Wyland Crews<br>
Industry Mentor: Manav Singhal<br>
Check out the app: https://swe-final-project-004.herokuapp.com/
## What is Map It! ?
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
## Challenges We Encountered
## Areas to be Improved
