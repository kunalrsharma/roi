# ROI App

Description:
- This App processes the ROI data for online advertising. 
- For each ad-camppaign, given by a key, it computes the 'point of diminishing retuns'(podr), i.e. the points after which the   revenue growth starts decreasing. 
- On the backend, for data processing, it automates the data smoothening using signal processing and then predicts the podr along with the estiamte of probability distribution of the podr values across campagins. 

On the functional side, this app uses Django for Python backend which then is deployed on the cloud platform Heroku.  

## Run this app

 -  __Please note that this app is in progress and uses ReactJS for the front end__
 - `$ python3 manage.py runserver`
 
 
