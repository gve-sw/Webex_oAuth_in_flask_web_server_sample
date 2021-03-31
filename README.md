# Webex oAuth in flask web server sample
Sample to let a user authenticate on a Flask based web site for it to perform operations on it's behalf such as scheduling a meeting using the Webex REST API 


## Contacts
* Gerardo Chaves (gchaves@cisco.com)

## Solution Components
* Webex

## Installation/Configuration


   1. Copy the config_default.py file to config.py  

   2. Recommended: Setup a virtual environment (https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

   3. Load up the required libraries from the requirements.txt file:  
    ```pip install -r requirements.txt```

   4. Register a Webex Teams OAuth integration per the steps here: 

        https://developer.webex.com/docs/integrations
  
        Set the Redirect URL to: http://0.0.0.0:5000/callback

        Select the 'spark:all' scope

   5. Place the integration client_id and client_secret values into the corresponding variables in config.py

 

## Usage


   1. Start the flask application:
    ```python App.py```

   2. Open a browser and navigate to:  https://0.0.0.0:5000

  The application will start the OAuth2 flow, then redirect to the /started URL to display the  
  target user's Webex display name and ID and the access_token be stored in ```session['oauth_token']``` to be used  
  in the rest of your code as you can see in lines 126 and 127 (if using the Webex Teams Python SDK)


### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
